source vars.sh

python3 src/random_sequences.py config_files/$pass_filename -o config_files/$sequence_filename -u -z --max-len 15 -n 10 > /dev/null