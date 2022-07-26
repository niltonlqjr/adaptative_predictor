#Collect program repersentations
python3 src/feature_extractor.py -r histogram /home/nilton/adaptative_predictor/benchmakrs_test/automotive-basicmath-small/ -o ignore/hist
python3 src/feature_extractor.py -r ir2vec /home/nilton/adaptative_predictor/benchmakrs_test/automotive-basicmath-small/ -o ignore/ir2vec

#Collect program speedup 
python3 src/speedup_collector.py benchmakrs_test/automotive-basicmath-small/ -s config_files/sequences.yaml -o ignore/speedups/

#Train deep learning model
python3 src/model_train.py ignore/ir2vec/ ignore/speedups/
python3 src/model_train.py ignore/hist/ ignore/speedups/
