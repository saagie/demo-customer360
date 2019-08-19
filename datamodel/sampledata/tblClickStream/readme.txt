~/Documents/Demo/log-synth/target/log-synth -count 1000 -schema clickstream.json  -format json > clickstream_sample_data.json
python3 convert.py clickstream_sample_data.json clickstream_sample_data.csv
To load to psql
tail +2 clickstream_sample_data.csv | psql -h customer-360.cflge37g0yl6.us-east-1.rds.amazonaws.com -p 5432 -U customer360_usr -d postgres -c "copy customer360.tblClickstream from STDIN with delimiter as ','"

