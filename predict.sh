benchmarks=('automotive-basicmath-small' 'automotive-bitcount' 'automotive-qsort-large')

mkdir -p ignore/results -m 777

for b in ${benchmarks[@]}
do
    echo $b
    mkdir -p ignore/results/$b -m 777
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/speedup_ir2vec_model.pck -s="-O2" -o ignore/results/$b/ir2vec_speedup.yaml
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/speedup_hist_model.pck -s="-O2" -o ignore/results/$b/hist_speedup.yaml
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/runtime_ir2vec_model.pck -s="-O2" -o ignore/results/$b/ir2vec_runtime.yaml
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/runtime_hist_model.pck -s="-O2" -o ignore/results/$b/hist_runtime.yaml
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/cycles_ir2vec_model.pck -s="-O2" -o ignore/results/$b/ir2vec_cycles.yaml
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/cycles_hist_model.pck -s="-O2" -o ignore/results/$b/hist_cycles.yaml
done