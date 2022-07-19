import argparse
import os

import numpy as np

from pathlib import Path

from extractors import SpeedupExtractor
from yacos.essential import Sequence
from yacos.essential import IO

def extract_speedup(benchmark_dir, sequence_dict):
    speedups={}
    for s_name in sequence_dict:
        sequence_str = Sequence.name_pass_to_string(sequence_dict[s_name])
        print(sequence_str)
        speedups[s_name] = SpeedupExtractor.get_sepeedup(bench_dir=benchmark_dir,
                                  sequence_str=sequence_str)
    return speedups

def run(args):
    bench_dir = args.program_dir
    sequences_file = args.sequences_file
    output_dir = args.output_dir

    sequence_dict = IO.load_yaml_or_fail(sequences_file)

    speedups = extract_speedup(bench_dir,sequence_dict)
    
    os.makedirs(output_dir,exist_ok=True)
    print(f'saving files into:{output_dir}')
    for s_name in speedups:
        outfile=str(s_name)+'_'+Path(bench_dir).stem
        outfile=os.path.join(output_dir,outfile)
        np.savez_compressed(outfile,
                            values=speedups[s_name])


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Speedup collector',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('program_dir',
                        help='directory of the program source, compile.sh, execute.sh and makefile.opt (compatible with yacos)')
    parser.add_argument('--sequeces-file', '-s', 
                        dest='sequences_file',
                        default='config_files/sequences.yaml',
                        help='yaml file containing a dictionary of sequences (each sequence is a list of optimizations)')
    parser.add_argument('--output-dir','-o', dest='output_dir',
                        default='representations',
                        help='output directory of repersentation files')
    args=parser.parse_args()

    run(args)