import os

from regex import B
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
                 representation_ext,
                 representation_type,
                 values_dir,
                 values_ext,
                 values_label,
                 values_baseline):

    files=glob.glob(os.path.join(representation_dir,'*.'+representation_ext))
    ret={}

    for filename in files:
        print(filename)
        bench_name = Path(filename).stem
        x = IO.load_yaml_or_fail(filename)
        x_data = x['data']
        x_representation = x['represetntation_type']
        if x_representation != representation_type:
            raise Exception(f'invalid representation type at file: {filename}'+
                            'Expected:{representation_type}. Get:{x_representation}')
        
        value_filename = os.path.join(values_dir,bench_name+'.'+values_ext)
        y = IO.load_yaml_or_fail(value_filename)
        y_data = y['data']
        y_label = y['label']
        if y_label != values_label:
            raise Exception(f'invalid values label at file:{filename}.'+
                            'Expected:{values_label}. Get:{y_label}')
        y_baseline = y['baseline']
        if y_baseline != values_baseline:
            raise Exception(f'invalid baseline  at file:{filename}.'+
                            'Expected:{values_baseline}. Get:{y_baseline}')
        ret[bench_name] = {}
        for seq in x_data:
            ret[bench_name][seq] = {}
            ret[bench_name][seq]['x'] = x_data[seq]
            ret[bench_name][seq]['y'] = y_data[seq]
    return ret

def train_regression(dataset,
                     epochs,
                     predict_train):
    x=[]
    y=[]
    for bench_name in dataset:
        for seq in dataset[bench_name]:
            x.append(dataset[bench_name][seq]['x'])
            y.append(dataset[bench_name][seq]['y'])
      
    x = np.array(x)
    y = np.array(y)

    scalerX = MinMaxScaler()
    scalerX.fit(x)
    x = scalerX.transform(x)

    model = build_model_dense(x.shape[1])

    model.fit(x,y,epochs=epochs)

    if predict_train:
        p = model.predict(x)

        for i in range(len(p)):
            print('predicted:',p[i],'-> real:',y[i])

    return model,scalerX

def filter_dataset_cluster(dataset,
                           program_list):
    ret={}
    for p in program_list:
        if p in dataset:
            ret[p] = dataset[p]
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
    values_label = args.values_label
    values_baseline = args.values_baseline
    cluster_file = args.cluster_file

    dataset = read_dataset(representation_dir,
                           representation_ext,
                           representation_type,
                           values_dir,
                           values_ext,
                           values_label,
                           values_baseline)
    
    if validation_samples != None:
        raise Exception("Validation support not implemented yet")

    if cluster_file == None:
        clusters={'default':list(dataset.keys())}
    

    regression_model_data={}
    for k_id in clusters:
        cluster_dataset = filter_dataset_cluster(dataset,
                                                 clusters[k_id])
        print(cluster_dataset.keys())
        regression_model, scalerX_model = train_regression(cluster_dataset,
                                                           epochs,
                                                           predict_train)

        regression_model_data[k_id]={}
        regression_model_data[k_id]['model'] = regression_model
        regression_model_data[k_id]['values_label'] = values_label
        regression_model_data[k_id]['representation_type'] = representation_type
        regression_model_data[k_id]['baseline'] = values_baseline
        regression_model_data[k_id]['scalerX'] = scalerX_model

    output_path,filename = os.path.split(output)
    if output_path != '':
        os.makedirs(output_path,exist_ok=True)
    model_data={}
    model_data['regression']=regression_model_data
    IO.dump_pickle(model_data,output)


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
                        default='yaml',
                        help='extension of representation files')
    parser.add_argument('--values-ext',
                        dest='values_ext',
                        default='yaml',
                        help='extension of values files')
    parser.add_argument('--values-label', '-l',
                        dest='values_label',
                        choices=['runtime','speedup'],
                        default='speedup')
    parser.add_argument('--values-baseline', '-b',
                        default='-O0',
                        dest='values_baseline',
                        help='baseline used to extract y metric')
    parser.add_argument('--epochs','-e',
                        type=int,
                        dest='epochs',
                        default=10,
                        help='eppchs of NN training')
    parser.add_argument('--predict-train',
                        dest='predict_train',
                        action='store_true',
                        help='Use this flag to predict the train dataset and print real vs predicted in stdout')
    parser.add_argument('--cluster-file', '-c',
                        dest='cluster_file',
                        default=None,
                        type=str)
    args=parser.parse_args()
    
    run(args)

