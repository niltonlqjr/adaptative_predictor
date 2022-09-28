sequence_filename='sequences_test.yaml'
pass_filename='passes_test.yaml'
benchmarks=('basicmath-small' 'bitcount' 'qsort-large')

python3 src/random_sequences.py config_files/$pass_filename -o config_files/$sequence_filename -u -z --max-len 15 -n 10 > /dev/null

for b in ${benchmarks[@]}
do
    echo $b
    #Collect program repersentations
    python3 src/feature_extractor.py benchmarks_train/$b/src $b -r histogram -s config_files/$sequence_filename -o ignore/hist  > /dev/null
    python3 src/feature_extractor.py benchmarks_train/$b/src $b -r ir2vec -s config_files/$sequence_filename -o ignore/ir2vec  > /dev/null
    #Collect program speedup 
    python3 src/speedup_collector.py benchmarks_train/$b/src $b -s config_files/$sequence_filename -o ignore/speedups/  > /dev/null
    #collect program runtime
    python3 src/runtime_collector.py benchmarks_train/$b/src $b -s config_files/$sequence_filename -o ignore/runtime  > /dev/null
    #collect number of cycles
    #python3 src/cycles_collector.py benchmarks_train/$b/src $b -s config_files/$sequence_filename -o ignore/cycles > /dev/null

done

#create output dir with rwx permissions
mkdir -p ignore -m 777

#cluster the train programs
python3 src/clustering.py ignore/ir2vec/ -n 3 -o ignore/clusters_ir2vec.yaml
python3 src/clustering.py ignore/hist/ -n 3 -o ignore/clusters_histogram.yaml 

#Train deep learning model
python3 src/model_train.py ignore/ir2vec/ ignore/speedups/ -t ir2vec -l speedup -o ignore/models/speedup_ir2vec_model.pck -c ignore/clusters_ir2vec.yaml  > /dev/null
python3 src/model_train.py ignore/hist/ ignore/speedups/ -t histogram -l speedup -o ignore/models/speedup_hist_model.pck  -c ignore/clusters_histogram.yaml  > /dev/null
python3 src/model_train.py ignore/ir2vec/ ignore/runtime/ -t ir2vec -l runtime -o ignore/models/runtime_ir2vec_model.pck  -c ignore/clusters_ir2vec.yaml  > /dev/null
python3 src/model_train.py ignore/hist/ ignore/runtime/ -t histogram -l runtime -o ignore/models/runtime_hist_model.pck -c ignore/clusters_histogram.yaml  > /dev/null
#python3 src/model_train.py ignore/ir2vec/ ignore/cycles/ -t ir2vec -l cycles -o ignore/models/cycles_ir2vec_model.pck -c ignore/clusters_ir2vec.yaml  > /dev/null
#python3 src/model_train.py ignore/hist/ ignore/cycles/ -t histogram -l cycles -o ignore/models/cycles_hist_model.pck -c ignore/clusters_histogram.yaml  > /dev/null


bench_test=('susan-c')


for b in ${bench_test[@]}
do
    mkdir -p ignore/results/$b -m 777
    #predict values
    python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/speedup_ir2vec_model.pck -s="-O2" -o ignore/results/$b/speedup_ir2vec.yaml
    python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/speedup_hist_model.pck -s="-O2" -o ignore/results/$b/speedup_hist.yaml
    python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/runtime_ir2vec_model.pck -s="-O2" -o ignore/results/$b/runtime_ir2vec.yaml
    python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/runtime_hist_model.pck -s="-O2" -o ignore/results/$b/runtime_hist.yaml
    #python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/cycles_ir2vec_model.pck -s="-O2" -o ignore/results/$b/cycles_ir2vec.yaml
    #python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/cycles_hist_model.pck -s="-O2" -o ignore/results/$b/cycles_hist.yaml

done