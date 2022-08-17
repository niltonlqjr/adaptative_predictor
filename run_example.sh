benchmarks=('automotive-basicmath-small' 'automotive-bitcount' 'automotive-qsort-large')

for b in ${benchmarks[@]}
do
    echo $b
    #Collect program repersentations
    python3 src/feature_extractor.py -r histogram /home/nilton/adaptative_predictor/benchmarks_train/$b/ -s config_files/sequences.yaml -o ignore/hist
    python3 src/feature_extractor.py -r ir2vec /home/nilton/adaptative_predictor/benchmarks_train/$b/ -s config_files/sequences.yaml -o ignore/ir2vec
    #Collect program speedup 
    python3 src/speedup_collector.py benchmarks_train/$b/ -s config_files/sequences.yaml -o ignore/speedups/
    #collect program runtime
    python3 src/runtime_collector.py benchmarks_train/$b/ -s config_files/sequences.yaml -o ignore/runtimes
    #collect number of cycles
    python3 src/cycles_collector.py benchmarks_train/$b/ -s config_files/sequences.yaml -o ignore/cycles

done

#cluster the train programs
python3 src/clustering.py ignore/ir2vec/ -n 3 -o ignore/clusters_ir2vec.yaml
python3 src/clustering.py ignore/hist/ -n 3 -o ignore/clusters_histogram.yaml 

#Train deep learning model
python3 src/model_train.py ignore/ir2vec/ ignore/speedups/ -t ir2vec -l speedup -o ignore/models/speedup_ir2vec_model.pck --predict-train -c ignore/clusters_ir2vec.yaml
python3 src/model_train.py ignore/hist/ ignore/speedups/ -t histogram -l speedup -o ignore/models/speedup_hist_model.pck --predict-train -c ignore/clusters_histogram.yaml 
python3 src/model_train.py ignore/ir2vec/ ignore/runtimes/ -t ir2vec -l runtime -o ignore/models/runtimes_ir2vec_model.pck --predict-train -c ignore/clusters_ir2vec.yaml
python3 src/model_train.py ignore/hist/ ignore/runtimes/ -t histogram -l runtime -o ignore/models/runtime_hist_model.pck --predict-train -c ignore/clusters_histogram.yaml 
python3 src/model_train.py ignore/ir2vec/ ignore/cycles/ -t ir2vec -l cycles -o ignore/models/cycles_ir2vec_model.pck --predict-train -c ignore/clusters_ir2vec.yaml
python3 src/model_train.py ignore/hist/ ignore/cycles/ -t histogram -l cycles -o ignore/models/cycles_hist_model.pck --predict-train -c ignore/clusters_histogram.yaml 

#predict values
python3 src/predictor.py benchmarks_test/automotive-susan-c/ -m ignore/models/speedup_ir2vec_model.pck -s="-O2"
python3 src/predictor.py benchmarks_test/automotive-susan-c/ -m ignore/models/speedup_hist_model.pck -s="-O2"
python3 src/predictor.py benchmarks_test/automotive-susan-c/ -m ignore/models/runtimes_ir2vec_model.pck -s="-O2"
python3 src/predictor.py benchmarks_test/automotive-susan-c/ -m ignore/models/runtime_hist_model.pck -s="-O2"
python3 src/predictor.py benchmarks_test/automotive-susan-c/ -m ignore/models/cycles_ir2vec_model.pck -s="-O2"
python3 src/predictor.py benchmarks_test/automotive-susan-c/ -m ignore/models/cycles_hist_model.pck -s="-O2"