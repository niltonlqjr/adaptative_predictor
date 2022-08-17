from gettext import find
import os

from regex import B
from sklearn.metrics import classification_report
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import glob
import argparse

import numpy as np
import tensorflow as tf

from yacos.essential import IO
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

from keras.utils import np_utils

from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, MaxPool1D, Dropout, Flatten
from tensorflow.keras.layers import Bidirectional, Input, MaxPooling1D, LSTM, concatenate
from tensorflow.keras.callbacks import EarlyStopping

from pathlib import Path

def read_dataset(representation_dir,
                 representation_ext,
                 representation_type,
                 values_dir,
                 values_ext,
                 values_label,
                 values_baseline):
    ''' 
        Output description
        -------------------
        Read the dataset and store it into a dict
        dataset keys are the benchmark name and its values is a dict
            dataset[bench_name] keys are the sequeces and its values is a dict
                dataset[bench_name][seq] is a dict with keys x and y
                    x value is the bench_name features when compiled with seq
                    y is the speedup of bench_name when compiled with seq
    '''
    files=glob.glob(os.path.join(representation_dir,'*.'+representation_ext))
    ret={}
    ret_x_baseline={}
    for filename in files:
        print(filename)
        bench_name = Path(filename).stem
        x = IO.load_yaml_or_fail(filename)
        x_data = x['data']
        x_baseline_feat = x['baseline_features']
        x_baseline = x['baseline_name']
        if x_baseline != values_baseline:
            raise Exception(f'invalid baseline  at file:{filename}.'+
                            f'Expected:{values_baseline}. Get:{x_baseline}')
        x_representation = x['represetntation_type']
        if x_representation != representation_type:
            raise Exception(f'invalid representation type at file: {filename}'+
                            f'Expected:{representation_type}. Get:{x_representation}')
        
        value_filename = os.path.join(values_dir,bench_name+'.'+values_ext)
        y = IO.load_yaml_or_fail(value_filename)
        y_data = y['data']
        y_label = y['label']
        if y_label != values_label:
            raise Exception(f'invalid values label at file:{filename}.'+
                            f'Expected:{values_label}. Get:{y_label}')
        y_baseline = y['baseline']
        if y_baseline != values_baseline:
            raise Exception(f'invalid baseline  at file:{filename}.'+
                            f'Expected:{values_baseline}. Get:{y_baseline}')
        
        ret_x_baseline[bench_name] = x_baseline_feat
        ret[bench_name] = {}
        for seq in x_data:
            ret[bench_name][seq] = {}
            ret[bench_name][seq]['x'] = x_data[seq]
            ret[bench_name][seq]['y'] = y_data[seq]
    return ret,ret_x_baseline

def label_dataset_to_clusters(dataset,
                              clusters):
    reverse_list={}
    
    for k_id in clusters:
        for p in clusters[k_id]:
            reverse_list[p]=k_id
    
    ret = {}
    for bench_name in dataset:
        ret[bench_name]={}
        ret[bench_name]['x']=dataset[bench_name]
        ret[bench_name]['y']=reverse_list[bench_name]
        #for seq in dataset[bench_name]:
        #    ret[bench_name][seq]=reverse_list[bench_name]
    return ret

def build_classification_model_dense(input_shape,
                                     n_classes):
    model = Sequential([
        Dense(64, activation="relu", input_shape=[input_shape]),
        Dense(32, activation="relu"),
        Dense(16, activation="relu"),
        Dense(32, activation="relu"),
        Dense(n_classes, activation="softmax")
    ])
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

def build_regression_model_dense(input_shape):
    model = Sequential([
        Dense(64, activation="relu", input_shape=[input_shape]),
        Dense(32, activation="relu"),
        Dense(16, activation="relu"),
        Dense(32, activation="relu"),
        Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss="mse",
                  optimizer=optimizer,
                  metrics=["mae", "mse"])

    return model

def train_classification(dataset,
                         epochs):
    x=[]
    y=[]
    for bench_name in dataset:
        x.append(dataset[bench_name]['x'])
        y.append(dataset[bench_name]['y'])
    
    scalerX = MinMaxScaler()
    scalerX.fit(x)
    x = scalerX.transform(x)
    encoderY = LabelEncoder()
    encoderY.fit(y)
    y = encoderY.transform(y)
    cat_y = np_utils.to_categorical(y)
    
    model=build_classification_model_dense(x.shape[1],
                                           cat_y.shape[1])

    model.fit(x,cat_y,epochs=epochs,verbose=0)

    p=model.predict(x)
    for i in range(len(p)):
        max_val=max(p[i])
        print('predicted:',np.where(p[i]==max_val)[0][0],'-> real:',y[i])

    return model,scalerX,encoderY

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

    model = build_regression_model_dense(x.shape[1])

    model.fit(x,y,epochs=epochs,verbose=0)

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
    clusters_file = args.clusters_file

    dataset,dataset_baselines_features = read_dataset(representation_dir,
                           representation_ext,
                           representation_type,
                           values_dir,
                           values_ext,
                           values_label,
                           values_baseline)
    
    if validation_samples != None:
        raise Exception("Validation support not implemented yet")


    try:
        clusters = IO.load_yaml(clusters_file)     
    except:
        clusters={'default':list(dataset.keys())}
    
    print(clusters)
    for f_ in dataset_baselines_features:
        print(f_)
    labeled_dataset = label_dataset_to_clusters(dataset_baselines_features,
                                                clusters)

    class_model, scalerX_class, encoderY_class = train_classification(
                                                    labeled_dataset,
                                                    epochs
                                                )
    classification_model_data={}
    classification_model_data['model']=class_model
    classification_model_data['scalerX']=scalerX_class
    classification_model_data['encoderY']=encoderY_class
    classification_model_data['representation']=representation_type

    regression_model_data={}
    for k_id in clusters:
        encoded_k_id=encoderY_class.transform([k_id])[0]
        cluster_dataset = filter_dataset_cluster(dataset,
                                                 clusters[k_id])
        print(cluster_dataset.keys())
        regression_model, scalerX_model = train_regression(cluster_dataset,
                                                           epochs,
                                                           predict_train)

        regression_model_data[encoded_k_id]={}
        regression_model_data[encoded_k_id]['model'] = regression_model
        regression_model_data[encoded_k_id]['values_label'] = values_label
        regression_model_data[encoded_k_id]['representation_type'] = representation_type
        regression_model_data[encoded_k_id]['scalerX'] = scalerX_model

    output_path,filename = os.path.split(output)
    if output_path != '':
        os.makedirs(output_path, exist_ok=True)
    model_data={}
    model_data['baseline'] = values_baseline
    model_data['regression']=regression_model_data
    model_data['classification']=classification_model_data
    IO.dump_pickle(model_data, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Model trainer',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('representation_dir',
                        help='directory containing dataset sequences')
    parser.add_argument('values_dir',
                        help='directory containing the tharget values for each dataset item')
    parser.add_argument('--representation-type', '-t',
                        default='ir2vec',
                        choices=['ir2vec','inst2vec','histogram'],
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
                        choices=['runtime','speedup','cycles'],
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
    parser.add_argument('--clusters-file', '-c',
                        dest='clusters_file',
                        default=None,
                        type=str)
    args=parser.parse_args()
    
    run(args)

