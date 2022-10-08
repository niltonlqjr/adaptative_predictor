source vars.sh


#create output dir with rwx permissions
mkdir -p ignore -m 777

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

for b in ${bench_test[@]}
do
    echo $b
    #python3 src/feature_extractor.py benchmarks_test/$b/src $b -r histogram -s config_files/$sequence_filename -o ignore/hist_test  > /dev/null
    #python3 src/feature_extractor.py benchmarks_test/$b/src $b -r ir2vec -s config_files/$sequence_filename -o ignore/ir2vec_test  > /dev/null
    #Collect program speedup 
    python3 src/speedup_collector.py benchmarks_test/$b/src $b -s config_files/$sequence_filename -o ignore/speedups_test  > /dev/null
    #collect program runtime
    python3 src/runtime_collector.py benchmarks_test/$b/src $b -s config_files/$sequence_filename -o ignore/runtime_test  > /dev/null
done