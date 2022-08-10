benchmarks=('automotive-basicmath-small' 'automotive-bitcount' 'automotive-qsort-large')

for b in ${benchmarks[@]}
do
    echo $b
    #Collect program repersentations
    python3 src/feature_extractor.py -r ir2vec /home/nilton/adaptative_predictor/benchmarks_train/$b/ -s config_files/sequences.yaml -o ignore/ir2vec
    #Collect program speedup 
    python3 src/speedup_collector.py benchmarks_train/$b/ -s config_files/sequences.yaml -o ignore/speedups/
done

#Train deep learning model
python3 src/model_train.py ignore/ir2vec/ ignore/speedups/ -t ir2vec -l speedup -o ignore/models/speedup_ir2vec_model.pck --clusters-file=config_files/clusters.yaml
#Predict value
python3 src/predictor.py benchmarks_test/automotive-susan-c/ -m ignore/models/speedup_ir2vec_model.pck -s="-O2"