import argparse
import tensorflow as tf

def run():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Model trainer')
    parser.add_argument('--representation-dir', '-d', help='directory containing dataset sequences')
    parser.add_argument('--representation-type', '-t', help='type of representation')
    args=parser.parse_args()
    
    run(args)

