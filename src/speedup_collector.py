import argparse
import os

import numpy as np

from pathlib import Path

from pkg_resources import working_set

from extractors import SpeedupExtractor
from yacos.essential import Sequence
from yacos.essential import IO

def extract_speedup(benchmark_dir,
                    sequence_dict,
                    baseline,
                    working_set,
                    runs):
    speedups={}
    SpeedupExtractor.set_number_runs(runs)
    SpeedupExtractor.set_baseline(baseline)
    
    for s_name in sequence_dict:
        sequence_str = Sequence.name_pass_to_string(sequence_dict[s_name])
        print(sequence_str)
        speedup_s_name = SpeedupExtractor.get_sepeedup(bench_dir=benchmark_dir,
                                                         sequence_str=sequence_str,
                                                         working_set=working_set)
        if speedup_s_name != None:
            speedups[s_name] = speedup_s_name
    return speedups

def run(args):
    bench_dir = args.program_dir
    sequences_file = args.sequences_file
    output_dir = args.output_dir
    baseline = args.baseline
    runs = args.runs
    working_set=args.working_set
    bench_name=args.bench_name

    sequence_dict = IO.load_yaml_or_fail(sequences_file)

    speedups = extract_speedup(bench_dir,sequence_dict, baseline, working_set,runs)
    
    os.makedirs(output_dir,exist_ok=True)
    print(f'saving files into:{output_dir}')
    '''for s_name in speedups:
        outfile=str(s_name)+'_'+Path(bench_dir).stem
        outfile=os.path.join(output_dir,outfile)'''
    #bench_name=Path(bench_dir).stem
    outfile=os.path.join(output_dir,bench_name)
    outfile+='.yaml'
    data={}
    data['label'] = 'speedup'
    data['data'] = speedups
    data['baseline'] = baseline
    IO.dump_yaml(data=data,
                 filename=outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Speedup collector',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('program_dir',
                        help='directory of the program source, compile.sh, execute.sh and makefile.opt (compatible with yacos)')
    parser.add_argument('bench_name',
                        help='benchmark name(used as prefix to output files)')
    parser.add_argument('--sequeces-file', '-s', 
                        dest='sequences_file',
                        default='config_files/sequences.yaml',
                        help='yaml file containing a dictionary of sequences (each sequence is a list of optimizations)')
    parser.add_argument('--runs', '-r',
                        dest='runs',
                        type=int,
                        default=3)
    parser.add_argument('--baseline','-b',
                        dest='baseline',
                        default='-O0',
                        help='Compiler optimization level to use as baseline ')
    parser.add_argument('--output-dir','-o',
                        dest='output_dir',
                        default='representations',
                        help='output directory of repersentation files')
    parser.add_argument('--working-set','-w',
                        dest='working_set',
                        default='0',
                        help='benchmark working set')
    args=parser.parse_args()

    run(args)