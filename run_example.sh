benchmarks=('automotive-basicmath-small' 'automotive-bitcount')

for b in ${benchmarks[@]}
do
    echo $b
    #Collect program repersentations
    python3 src/feature_extractor.py -r histogram /home/nilton/adaptative_predictor/benchmakrs_test/$b/ -s config_files/sequences.yaml -o ignore/hist
    python3 src/feature_extractor.py -r ir2vec /home/nilton/adaptative_predictor/benchmakrs_test/$b/ -s config_files/sequences.yaml -o ignore/ir2vec
    #Collect program speedup 
    python3 src/speedup_collector.py benchmakrs_test/$b/ -s config_files/sequences.yaml -o ignore/speedups/
    #collect program runtime
    python3 src/runtime_collector.py benchmakrs_test/$b/ -s config_files/sequences.yaml -o ignore/runtimes
done

#Train deep learning model
python3 src/model_train.py ignore/ir2vec/ ignore/speedups/ -t ir2vec -l speedup -o ignore/models/speedup_ir2vec_model.pck --predict-train
python3 src/model_train.py ignore/hist/ ignore/speedups/ -t histogram -l speedup -o ignore/models/speedup_hist_model.pck --predict-train
python3 src/model_train.py ignore/ir2vec/ ignore/runtimes/ -t ir2vec -l runtime -o ignore/models/runtimes_ir2vec_model.pck --predict-train
python3 src/model_train.py ignore/hist/ ignore/runtimes/ -t histogram -l runtime -o ignore/models/runtime_hist_model.pck --predict-train