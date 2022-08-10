benchmarks=('automotive-basicmath-small' 'automotive-bitcount' 'automotive-qsort-large')


#Train deep learning model
python3 src/model_train.py ignore/ir2vec/ ignore/speedups/ -t ir2vec -l speedup -o ignore/models/speedup_ir2vec_model.pck --predict-train --clusters-file=config_files/clusters.yaml
#Predict value
#python3 src/predictor.py benchmarks_train/automotive-basicmath-small/ -m ignore/models/speedup_ir2vec_model.pck -s="-O0"
