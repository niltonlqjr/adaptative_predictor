benchmarks=('automotive-basicmath-small' 'automotive-bitcount' 'automotive-qsort-large')

for b in ${benchmarks[@]}
do
    echo $b
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/speedup_ir2vec_model.pck -s="-O2"
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/speedup_hist_model.pck -s="-O2"
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/runtimes_ir2vec_model.pck -s="-O2"
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/runtime_hist_model.pck -s="-O2"
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/cycles_ir2vec_model.pck -s="-O2"
    python3 src/predictor.py benchmarks_train/$b/ -m ignore/models/cycles_hist_model.pck -s="-O2"
done