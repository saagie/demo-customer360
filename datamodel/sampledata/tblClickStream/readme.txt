~/Documents/Demo/log-synth/target/log-synth -count 1000 -schema clickstream.json  -format json > clickstream_sample_data.json
python3 convert.py clickstream_sample_data.json clickstream_sample_data.csv

