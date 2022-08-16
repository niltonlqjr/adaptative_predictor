import argparse
import os

import numpy as np

from pathlib import Path

from extractors import ExecutionGoalExtractor
from yacos.essential import Sequence
from yacos.essential import IO

def extract_cycles(benchmark_dir,
                    sequence_dict,
                    working_set,
                    runs):
    cycles={}
    ExecutionGoalExtractor.set_goal(['cycles'],['1'])
    ExecutionGoalExtractor.set_number_runs(runs)
    for s_name in sequence_dict:
        sequence_str = Sequence.name_pass_to_string(sequence_dict[s_name])
        print(sequence_str)
        cycles[s_name] = ExecutionGoalExtractor.get_execution_goal(bench_dir=benchmark_dir,
                                                                     sequence_str=sequence_str,
                                                                     working_set=working_set)
    return cycles

def run(args):
    bench_dir = args.program_dir
    sequences_file = args.sequences_file
    output_dir = args.output_dir
    runs = args.runs
    working_set=args.working_set

    sequence_dict = IO.load_yaml_or_fail(sequences_file)

    cycles = extract_cycles(bench_dir,sequence_dict, working_set, runs)
    
    os.makedirs(output_dir,exist_ok=True)
    print(f'saving files into:{output_dir}')
    '''for s_name in runtimes:
        outfile=str(s_name)+'_'+Path(bench_dir).stem
        outfile=os.path.join(output_dir,outfile)
        print(s_name,runtimes[s_name])'''
    bench_name=Path(bench_dir).stem
    outfile=os.path.join(output_dir,bench_name)
    outfile+='.yaml'
    data={}
    data['label'] = 'cycles'
    data['data'] = cycles
    data['baseline'] = '-O0'
    IO.dump_yaml(data=data,
                 filename=outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Speedup collector',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('program_dir',
                        help='directory of the program source, compile.sh, execute.sh and makefile.opt (compatible with yacos)')
    parser.add_argument('--sequeces-file', '-s', 
                        dest='sequences_file',
                        default='config_files/sequences.yaml',
                        help='yaml file containing a dictionary of sequences (each sequence is a list of optimizations)')
    parser.add_argument('--runs', '-r',
                        dest='runs',
                        type=int,
                        default=5)
    parser.add_argument('--output-dir','-o', dest='output_dir',
                        default='representations',
                        help='output directory of repersentation files')
    parser.add_argument('--working-set','-w',
                        dest='working_set',
                        default='0',
                        help='benchmark working set')
    args=parser.parse_args()
    print('Running cycles collection requires Perf working',
          "(don't forget to set perf_event_paranoid)")
    run(args)