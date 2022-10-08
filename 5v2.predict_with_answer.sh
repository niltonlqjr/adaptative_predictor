source vars.sh

for b in ${bench_test[@]}
do
    
    mkdir -p ignore/results/$b -m 777
    #predict values
    python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/speedup_ir2vec_model.pck -k="S1" -a ignore/speedups_test/$b.yaml -sf config_files/$sequence_filename -o ignore/results/$b/speedup_ir2vec.yaml
    python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/speedup_hist_model.pck -k="S1" -a ignore/speedups_test/$b.yaml -sf config_files/$sequence_filename -o ignore/results/$b/speedup_hist.yaml
    python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/runtime_ir2vec_model.pck -k="S1" -a ignore/runtime_test/$b.yaml -sf config_files/$sequence_filename -o ignore/results/$b/runtime_ir2vec.yaml
    python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/runtime_hist_model.pck -k="S1" -a ignore/runtime_test/$b.yaml -sf config_files/$sequence_filename -o ignore/results/$b/runtime_hist.yaml
    #python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/cycles_ir2vec_model.pck -s="-O2" -o ignore/results/$b/cycles_ir2vec.yaml
    #python3 src/predictor.py benchmarks_test/$b/src -m ignore/models/cycles_hist_model.pck -s="-O2" -o ignore/results/$b/cycles_hist.yaml

done