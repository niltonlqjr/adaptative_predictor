benchmarks=('automotive-basicmath-small' 'automotive-bitcount')


for b in ${benchmarks[@]}
do
    echo $b
    #Collect program repersentations
    python3 src/feature_extractor.py -r ir2vec /home/nilton/adaptative_predictor/benchmakrs_test/$b/ -o ignore/ir2vec
    #Collect program speedup 
    python3 src/speedup_collector.py benchmakrs_test/automotive-basicmath-small/ -s config_files/sequences.yaml -o ignore/speedups/

done

#Train deep learning model
python3 src/model_train.py ignore/ir2vec/ ignore/speedups/ -o ignore/models/speedup_ir2vec_model.pck --predict-train
