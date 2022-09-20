import argparse
import random

from yacos.essential import IO
from yacos.essential import Sequence

def create_sequence(passes,min,max,update,sanitize):
    seq_len=random.randint(min,max)
    num_passes=len(passes)
    seq=[]
    for i in range(seq_len):
        pass_id = random.randint(0,num_passes-1)
        seq.append(passes[pass_id])
    print(seq)
    if update:
        print('update')
        seq=Sequence.update(seq)
    if sanitize:
        print('sanitize')
        seq=Sequence.sanitize(seq)
    return seq


parser=argparse.ArgumentParser('Random Sequence Generator',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('pass_file',
                    help='YAML file containing a list of passes that will be used')
parser.add_argument('--output','-o',
                    dest='output_file',
                    default='sequences.yaml',
                    help='output filename')
parser.add_argument('--min-length','-s',
                    dest='min_length',
                    default=1,
                    type=int,
                    help='minimum sequence length')
parser.add_argument('--max-length','-g',
                    dest='max_length',
                    default=200,
                    type=int,
                    help='maximum sequence length')
parser.add_argument('--update','-u',
                    dest='update',
                    action='store_true',
                    help='update sequence according to llvm manual suggestions')
parser.add_argument('--sanitize','-z',
                    dest='sanitize',
                    action='store_true',
                    help='remove the same sequence when it apperas consecutively')
parser.add_argument('--number-sequences','-n',
                    dest='number_sequences',
                    default=10,
                    type=int,
                    help='number of sequences to create')
args=parser.parse_args()

pass_file=args.pass_file
out_file=args.output_file
min_len=args.min_length
max_len=args.max_length
update_seq=args.update
sanitize_seq=args.sanitize
n=args.number_sequences

sequences={}

print(args)

passes = IO.load_yaml_or_fail(pass_file)

for i in range(n):
    idx='S'+str(i)
    sequences[idx]=create_sequence(passes,
                                    min_len,
                                    max_len,
                                    update_seq,
                                    sanitize_seq)
    print(sequences[idx])
    print('================')

IO.dump_yaml(sequences,out_file)