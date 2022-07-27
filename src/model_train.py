import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import glob
import argparse

import numpy as np
import tensorflow as tf

from yacos.essential import IO
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, MaxPool1D, Dropout, Flatten
from tensorflow.keras.layers import Bidirectional, Input, MaxPooling1D, LSTM, concatenate
from tensorflow.keras.callbacks import EarlyStopping

from pathlib import Path

def build_model_dense(input_shape):
    model = Sequential([
        Dense(64, activation="relu", input_shape=[input_shape]),
        Dense(32, activation="relu"),
        Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss="mse",
                  optimizer=optimizer,
                  metrics=["mae", "mse"])

    return model

def read_dataset(representation_dir,
                 values_dir,
                 representation_ext,
                 values_ext):
    ret = {}

    files=glob.glob(os.path.join(representation_dir,'*.'+representation_ext))

    for filename in files:
        pf = Path(filename)
        file_no_ext = pf.stem
        ret[file_no_ext]={}
        ret[file_no_ext]['repr'] = np.load(filename)['values']
        value_filename = os.path.join(values_dir,file_no_ext+'.'+values_ext)
        ret[file_no_ext]['value'] = np.load(value_filename)['values']

    return ret

def run(args):
    representation_dir = args.representation_dir
    values_dir = args.values_dir
    representation_type = args.representation_type
    validation_samples = args.validation_samples
    representation_ext = args.representation_ext
    values_ext = args.values_ext
    epochs = args.epochs
    output = args.output
    predict_train = args.predict_train

    dataset = read_dataset(representation_dir,
                           values_dir,
                           representation_ext,
                           values_ext)
    
    if validation_samples != None:
        raise Exception("Validation support not implemented yet")

    x=[]
    y=[]
    for e in dataset:
        #print(e)
        #print(dataset[e]['repr'][::60], '->', dataset[e]['value'])
        #print('======')
        x.append(dataset[e]['repr'])
        y.append(dataset[e]['value'])
    
    for i in range(len(x)):
        print(x[i][::60],'--',y[i])
    
    x = np.array(x)
    y = np.array(y)

    scalerX = MinMaxScaler()
    scalerX.fit(x)
    x = scalerX.transform(x)

    model = build_model_dense(x.shape[1])

    model.fit(x,y,epochs=epochs)

    output_path,filename = os.path.split(output)

    os.makedirs(output_path,exist_ok=True)

    IO.dump_pickle(model,output)

    if predict_train:
        p = model.predict(x)

        for i in range(len(p)):
            print('predicted:',p[i],'-> real:',y[i])


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Model trainer',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('representation_dir',
                        help='directory containing dataset sequences')
    parser.add_argument('values_dir',
                        help='directory containing the tharget values for each dataset item')
    parser.add_argument('--representation-type', '-t',
                        default='ir2vec',
                        dest='representation_type',
                        help='type of representation')
    parser.add_argument('--output', '-o',
                        default='model.pck',
                        dest='output',
                        help='filename to store the NN model (pickle format)')
    parser.add_argument('--validation-sample', '-v',
                        default=None,
                        type=str,
                        dest='validation_samples',
                        help='list of validation samples')
    parser.add_argument('--representation-ext',
                        dest='representation_ext',
                        default='npz',
                        help='extension of representation files')
    parser.add_argument('--values-ext',
                        dest='values_ext',
                        default='npz',
                        help='extension of values files')
    parser.add_argument('--epochs','-e',
                        type=int,
                        dest='epochs',
                        default=10,
                        help='eppchs of NN training')
    parser.add_argument('--predict-train',
                        dest='predict_train',
                        action='store_true',
                        help='Use this flag to predict the train dataset and print real vs predicted in stdout')

    args=parser.parse_args()
    
    run(args)

