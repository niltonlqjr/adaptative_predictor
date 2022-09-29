source vars.sh
#cluster the train programs
python3 src/clustering.py ignore/ir2vec/ -n 3 -o ignore/clusters_ir2vec.yaml
python3 src/clustering.py ignore/hist/ -n 3 -o ignore/clusters_histogram.yaml 

