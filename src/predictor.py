import os
from pkg_resources import working_set

from sympy import sequence
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import argparse

import numpy as np
import tensorflow as tf

from yacos.essential import IO
from sklearn.preprocessing import MinMaxScaler

from extractors import *

def run(args):
    model_file=args.model_file
    benchmark_dir = args.benchmark_dir
    sequence = args.sequence
    only_predict = args.only_predict
    working_set = args.working_set

    model_data = IO.load_pickle_or_fail(model_file)
    representation_type = model_data['representation_type']
    target = model_data['values_label']
    baseline = model_data['baseline']
    model = model_data['model']
    scalerX = model_data['scalerX']
    print('representation (X):',model_data['representation_type'])
    print('target (y):',model_data['values_label'])
    

    extractor = None
    if representation_type == 'ir2vec':
        extractor = IR2vecExtractor
    elif representation_type == 'histogram':
        extractor = HistogramExtractor
    
    representation = extractor.extract_representation(benchmark_dir,sequence)
    representation = scalerX.transform([representation])
    real_target = None
    pred_target = model.predict(representation)

    out_str = f'predicted value:{pred_target}'

    if not only_predict:
        if target == 'speedup':
            SpeedupExtractor.set_baseline(baseline)
            real_target = SpeedupExtractor.get_sepeedup(benchmark_dir,
                                          sequence,
                                          working_set)
        out_str += f'-> real value:{real_target}'
    
    print(out_str)

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('predict speedup/runtime',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('benchmark_dir',
                        help='directory containing benchmark')
    parser.add_argument('--output', '-o',
                        default='model.pck',
                        dest='output',
                        help='filename to store the NN model (pickle format)')
    parser.add_argument('--model-file', '-m',
                        default='model.pck',
                        type=str,
                        dest='model_file',
                        help='model file (pickle format)')
    parser.add_argument('--only-predict','-p',
                        action='store_true',
                        dest='only_predict',
                        help='predict execution time and do not execute the benchmark')
    parser.add_argument('--sequence','-s',
                        dest='sequence',
                        default='-O1',
                        help='optimization sequence')
    parser.add_argument('--working-set','-w',
                        dest='working_set',
                        default='0',
                        help='benchmark working set')
    args=parser.parse_args()
    
    run(args)
