import argparse
import sys
import os

import numpy as np

from pathlib import Path
from pkg_resources import working_set

from yacos.essential import Engine
from yacos.essential import IO
from yacos.essential import Sequence

from yacos.info.ncc import Inst2Vec
from yacos.info import compy
from yacos.info.compy.extractors import LLVMDriver

from extractors import *

def extract_representations_sequences(bench_dir, sequence_dict, 
                                      representation, baseline):
    """
    extract the representation of one benchmark with a collection of sequences
    bench_dir: str
        directory of one benchmark ready to compile with Yacos (with makefile and configure.sh)
    sequence_dict: dict
        a dictionary where the keys are the sequence name and the values are
        a list with compiler passes
    baseline: string
        default optimization compiler level used as baseline
    representation: str
        a string with the representation that will be extracted
        valid values:
            ir2vec
            histogram
            inst2vec
    """
    extractor = None
    if representation == 'ir2vec':
        extractor = IR2vecExtractor
    elif representation == 'histogram':
        extractor = HistogramExtractor
    elif representation == 'inst2vec':
        extractor = Inst2Vec

    representations={}

    baseline_representation = extractor.extract_representation(bench_dir,
                                                     baseline)

    for s_name in sequence_dict:
        sequence_str = Sequence.name_pass_to_string(sequence_dict[s_name])
        print(sequence_str)
        representations[s_name] = extractor.extract_representation(bench_dir,
                                    sequence_str)
    return representations,baseline_representation

def run(args):
    bench_dir = args.program_dir
    sequence_file=args.sequences_file
    representation=args.representation
    output_dir=args.output_dir
    baseline = args.baseline
    bench_name=args.bench_name

    sequence_dict = IO.load_yaml_or_fail(sequence_file)
    representations={}
    if 'baseline' in sequence_dict:
        print('invalide sequence name: baseline',file=sys.stderr)
        exit(0)

    print('extrcting representations')

    representations,baseline_repr=extract_representations_sequences(bench_dir,
                                                      sequence_dict,
                                                      representation,
                                                      baseline)

    os.makedirs(output_dir,exist_ok=True)

    print(f'saving files into:{output_dir}')
    '''for s_name in representations:
        outfile=str(s_name)+'_'+Path(bench_dir).stem
        outfile=os.path.join(output_dir,outfile)'''
    #bench_name=Path(bench_dir).stem
    outfile=os.path.join(output_dir,bench_name)
    outfile+='.yaml'
    data={}
    data['data'] = representations
    data['baseline_features']=baseline_repr
    data['baseline_name'] = baseline
    data['represetntation_type'] = representation
    IO.dump_yaml(data=data,
                 filename=outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Feature extractor',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('program_dir',
                        help='directory of the program source, compile.sh and makefile.opt (compatible with yacos)')
    parser.add_argument('bench_name',
                        help='benchmark name (used as prefix to output files)')
    parser.add_argument('--sequeces-file', '-s', 
                        dest='sequences_file',
                        default='config_files/sequences.yaml',
                        help='yaml file containing a dictionary of sequences (each sequence is a list of optimizations)')
    parser.add_argument('--representation', '-r', dest='representation',
                        choices=['ir2vec','inst2vec','histogram'],
                        default='ir2vec',
                        help='representation to be extracted')
    parser.add_argument('--baseline','-b',
                        dest='baseline',
                        default='-O0',
                        help='Compiler optimization level to use as baseline ')
    parser.add_argument('--output-dir','-o', dest='output_dir',
                        default='representations',
                        help='output directory of repersentation files')
    args=parser.parse_args()

    run(args)

