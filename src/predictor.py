import numbers
import os
from pkg_resources import working_set
from sklearn.metrics import classification_report

from sympy import sequence
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import argparse

import numpy as np
import tensorflow as tf

from yacos.essential import IO
from yacos.essential import Sequence
from sklearn.preprocessing import MinMaxScaler

from extractors import *

def run(args):
    model_file=args.model_file
    benchmark_dir = args.benchmark_dir
    sequence = args.sequence
    only_predict = args.only_predict
    working_set = args.working_set
    output_file = args.output_file
    number_runs = args.number_runs
    answer_file = args.answer_file
    answer_key = args.answer_key

    sequence_file = args.sequence_file
    if answer_file != None and (answer_key == None or sequence_file==None):
        sys.stderr.write('You must use an answer key when using an answer file and a sequence file!')
        exit(0)

    if sequence_file != None:
        compiled_sequences = IO.load_yaml(sequence_file)
        sequence = Sequence.name_pass_to_string(compiled_sequences[answer_key])

    output = {}
    
    model_data = IO.load_pickle_or_fail(model_file)
    baseline = model_data['baseline']
    classification_model_data=model_data['classification']
    representation_type = classification_model_data['representation']
    class_model = classification_model_data['model']
    scalerX_class = classification_model_data['scalerX']
    encoderY_class = classification_model_data['encoderY']

    extractor = None
    if representation_type == 'ir2vec':
        extractor = IR2vecExtractor
    elif representation_type == 'histogram':
        extractor = HistogramExtractor
    
    output['info'] = {}
    output['info']['representation_type'] = representation_type
    output['info']['baseline']=baseline

    #extract representation from test program for classification
    representation = extractor.extract_representation(benchmark_dir,baseline)
    #normalize representation for classification
    representation_clasification = scalerX_class.transform([representation])
    #get probability of each class
    prob_class = class_model.predict([representation_clasification])
    #get the real class
    output['result']={}
    output['result']['probability_class'] = list([float(x) for x in prob_class[0]])
    
    print('probablilty of classes:',list(prob_class[0]))
    max_prob = max(prob_class[0])
    predicted_class = np.where(prob_class[0] == max_prob)[0][0]

    output['result']['predicted_class']=int(predicted_class)

    cluster_file_id = encoderY_class.inverse_transform([predicted_class])
    print('predicted class:',predicted_class)
    print('cluster: ', cluster_file_id)

    output['result']['cluster_file_id'] = int(cluster_file_id[0])

    #select the regression model
    regression_model_data = model_data['regression'][predicted_class]
    representation_type = regression_model_data['representation_type']
    target = regression_model_data['values_label']
    model = regression_model_data['model']
    scalerX = regression_model_data['scalerX']
    print('representation (X):',regression_model_data['representation_type'])
    print('target (y):',regression_model_data['values_label'])

    
    #extract representation from test program for regression
    representation = extractor.extract_representation(benchmark_dir,sequence)
    #normalize representation for regression
    representation_regression = scalerX.transform([representation])
    real_target = None

    #predict the regression value
    pred_target = model.predict(representation_regression)

    print('program:',benchmark_dir)
    out_str = f'predicted value:{pred_target[0][0]}'

    output['result']['predicted_value'] = float(pred_target[0][0])

    if not only_predict:
        if answer_file == None:
            if target == 'speedup':
                SpeedupExtractor.set_baseline(baseline)
                real_target = SpeedupExtractor.get_sepeedup(benchmark_dir,
                                            sequence,
                                            working_set)
            elif target == 'cycles':
                ExecutionGoalExtractor.set_goal(['cycles'],['1'])
                ExecutionGoalExtractor.set_number_runs(number_runs)
                real_target = ExecutionGoalExtractor.get_execution_goal(
                                                        benchmark_dir,
                                                        sequence,
                                                        working_set)
            elif target == 'runtime':
                ExecutionGoalExtractor.set_goal(['runtime'],['1'])
                ExecutionGoalExtractor.set_number_runs(number_runs)
                real_target = ExecutionGoalExtractor.get_execution_goal(
                                                        benchmark_dir,
                                                        sequence,
                                                        working_set)
        else:
            ans = IO.load_yaml_or_fail(answer_file)
            real_target = ans['data'][answer_key]
        
        out_str += f'-> real value:{real_target}'
        output['result']['real_value']=real_target
    IO.dump_yaml(output,output_file)
    print(out_str)

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('predict speedup',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('benchmark_dir',
                        help='directory containing benchmark')
    parser.add_argument('--output', '-o',
                        default='output.yaml',
                        dest='output_file',
                        help='filename to store the output')
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
    parser.add_argument('--number-runs', '-r',
                        dest='number_runs',
                        default=1,
                        type=int,
                        help='number of runs to collect real value (only used when only predict is disabled)')
    parser.add_argument('--answer-file','-a',
                        dest='answer_file',
                        default=None,
                        help='yaml file that contain the real speedup for the program (created by' 
                              + 'speedup_collector.py)\nIf not used, the program will be executed')
    parser.add_argument('--answer-key','-k',
                        dest='answer_key',
                        default=None,
                        help='key used for the answer (this argumment is used only with --answer-file\n'+
                        'if this argument is used, the --sequence argumment is ignored.)')
    parser.add_argument('--sequence-file','-sf',
                        dest='sequence_file',
                        default=None,
                        help='file containing sequeces passes of answer file')

    args=parser.parse_args()
    
    run(args)
