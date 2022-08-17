import argparse
import glob
import os
import numpy as np
import yaml as yl
from pathlib import Path

from yacos.essential import IO
from sklearn.cluster import KMeans


def run(args):
    data_dir=args.data_dir
    file_list=args.files_list
    cluster_number = args.cluster_number
    output_file = args.output_file

    if file_list==None:
        glob_exp=os.path.join(data_dir,'*.yaml')
        files=glob.glob(glob_exp)
    
    data={}
    i=0
    for fn in files:
        data[i] = {}
        path_fn = Path(fn)
        bench_name = path_fn.stem
        data[i]['name'] = bench_name
        f_data = IO.load_yaml(fn)
        data[i]['feat']=f_data['baseline_features']
        i+=1

    X=[None for i in range(len(data))]
    for i in data:
        X[i] = data[i]['feat']
    
    kmeans_model = KMeans(n_clusters=cluster_number,
                          random_state=0)
    kmeans = kmeans_model.fit(X)
    labels = kmeans.labels_

    for i in range(len(labels)):
        data[i]['label'] = int(labels[i])
    
    for i in data:
        print(data[i]['name'],data[i]['label'])

    clusters = {}
    for i in data:
        c = data[i]['label']
        if not (c in clusters):
            clusters[c]=[]
        clusters[c].append(data[i]['name'])
    
    IO.dump_yaml(clusters,output_file)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Clustering',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('data_dir',
                        help='directory containing the data of all programs that will be clustered')
    parser.add_argument('--output-file','-o',
                        dest='output_file',
                        default='clusters.yaml',
                        help='filename of output')
    parser.add_argument('--files-list', '-f',
                        dest='files_list',
                        type=str,
                        default=None,
                        help='YAML file containig a list of all files that will be clustered'
                             +'(without this argument, all files in data_dir will be processed')
    parser.add_argument('--cluster-number','-n',
                        type=int,
                        dest='cluster_number',
                        default=2,
                        help='number of clusters')
    args=parser.parse_args()

    run(args)