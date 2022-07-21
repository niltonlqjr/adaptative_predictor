import argparse
#import tensorflow as tf
import os
import glob
import numpy as np


from pathlib import Path

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

    dataset = read_dataset(representation_dir,
                           values_dir,
                           representation_ext,
                           values_ext)
    
    for e in dataset:
        print(e)
        print(dataset[e]['repr'][::60], '->', dataset[e]['value'])
        print('======')

    if validation_samples != None:
        print("validation not implemented yet")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Model trainer')
    parser.add_argument('representation_dir',
                        help='directory containing dataset sequences')
    parser.add_argument('values_dir',
                        help='directory containing the tharget values for each dataset item')
    parser.add_argument('--representation-type', '-t',
                        default='ir2vec',
                        dest='representation_type',
                        help='type of representation')
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

    args=parser.parse_args()
    
    run(args)

