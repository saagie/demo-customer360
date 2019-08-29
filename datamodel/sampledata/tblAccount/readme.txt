To Generate a mix of active and in active accounts and show customer churn etc , use the following process....
~/Documents/Demo/log-synth/target/log-synth -count 100 -schema active_account.json -format json > account_sample_data.json
~/Documents/Demo/log-synth/target/log-synth -count 100 -schema inactive_account.json -format json >> account_sample_data.json
python3 convert.py account_sample_data.json account_sample_data.csv

