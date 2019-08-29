~/Documents/Demo/log-synth/target/log-synth -count 1000 -schema contact.json -format json > contact_sample_data.json
python3 convert.py contact_sample_data.json contact_sample_data.csv

