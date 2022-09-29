source vars.sh
#Train deep learning model
python3 src/model_train.py ignore/ir2vec/ ignore/speedups/ -t ir2vec -l speedup -o ignore/models/speedup_ir2vec_model.pck -c ignore/clusters_ir2vec.yaml  > /dev/null
python3 src/model_train.py ignore/hist/ ignore/speedups/ -t histogram -l speedup -o ignore/models/speedup_hist_model.pck  -c ignore/clusters_histogram.yaml  > /dev/null
python3 src/model_train.py ignore/ir2vec/ ignore/runtime/ -t ir2vec -l runtime -o ignore/models/runtime_ir2vec_model.pck  -c ignore/clusters_ir2vec.yaml  > /dev/null
python3 src/model_train.py ignore/hist/ ignore/runtime/ -t histogram -l runtime -o ignore/models/runtime_hist_model.pck -c ignore/clusters_histogram.yaml  > /dev/null
#python3 src/model_train.py ignore/ir2vec/ ignore/cycles/ -t ir2vec -l cycles -o ignore/models/cycles_ir2vec_model.pck -c ignore/clusters_ir2vec.yaml  > /dev/null
#python3 src/model_train.py ignore/hist/ ignore/cycles/ -t histogram -l cycles -o ignore/models/cycles_hist_model.pck -c ignore/clusters_histogram.yaml  > /dev/null
