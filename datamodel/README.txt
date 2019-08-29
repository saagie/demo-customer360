# Create a dir to store all virtual environments
mkdir ~/.virtualenvs

# Create a new virtual environment
python3 -m venv ~/.virtualenvs/3.5.2

# Make it active
source ~/.virtualenvs/3.5.2/bin/activate

# Check the version in use
python --version

# Deactivate the environment
deactivate

------------------------------------------------------------------------

PIP:
----

pip install --upgrade pip

pip -V

pip install boto
pip install boto3

pip install smart_open

pip install psycopg2-binary

------------------------------------------------------------------------

PostgreSQL:
----------
# On a Mac, assuming you have PostgreSQL installed on your machine:

# 1. Add this to ~/.bash_profile:

# PostgreSQL, path to binaries
echo "export PATH=/Applications/Postgres.app/Contents/Versions/11/bin/:${PATH}" >> ~/.bash_profile
source ~/.bash_profile

# 2. Create a .pgpass file:

vim ~/.pgpass

# Content:
##########

#hostname:port:database:username:password
127.0.0.1:5432:AAAA:XXXX

# Save it, then:

chmod 600 ~/.pgpass

# Try it:

psql

# You should be automatically connected, try a simple command:

\dn

# It should show all the schemas currently in your database

# 3. Create the schema and tables for the customer 360 demo
# If you are not connected yet, connect to psql

psql

# Then, import the DDL, replacing the path with yours:

\i ~/Code/saagie/demo-customer360/datamodel/sql/dbschema.sql

# Check the result

\dn

# There should now be a customer360 schema

\d

# It should show all the tables in the customer360 schema

                 List of relations
   Schema    |        Name        | Type  | Owner
-------------+--------------------+-------+--------
 customer360 | tblaccount         | table | pborne
 customer360 | tblclickstream     | table | pborne
 customer360 | tblcontact         | table | pborne
 customer360 | tblorder           | table | pborne
 customer360 | tblproduct         | table | pborne
 customer360 | tblproductcategory | table | pborne
 customer360 | tblsupportticket   | table | pborne
(7 rows)

# Load data into the tables

truncate table customer360.tblproductcategory;
\copy customer360.tblproductcategory from 'sampledata/tblProductCategory/product_category.csv' with DELIMITER ',' csv header;
select count(1) from customer360.tblproductcategory;

truncate table customer360.tblproduct;
\copy customer360.tblproduct from 'sampledata/tblProduct/product.csv' with DELIMITER ',' csv header;
select count(1) from customer360.tblproduct;

truncate table customer360.tblAccount;
\copy customer360.tblAccount from 'sampledata/tblAccount/account_sample_data.csv' with DELIMITER ',' csv header;
select count(1) from customer360.tblAccount;

truncate table customer360.tblContact;
\copy customer360.tblContact from 'sampledata/tblContact/contact_sample_data.csv' with DELIMITER ',' csv header;
select count(1) from customer360.tblContact;

truncate table customer360.tblOrder;
\copy customer360.tblOrder from 'sampledata/tblOrder/order_sample_data.csv' with DELIMITER ',' csv header;
select count(1) from customer360.tblOrder;

truncate table customer360.tblClickStream;
\copy customer360.tblClickStream from 'sampledata/tblClickStream/clickstream_sample_data.csv' with DELIMITER ',' csv header;
select count(1) from customer360.tblClickStream;

# Connect to the instance in AWS RDS:
# Options for psql:

#  -h, --host=HOSTNAME      database server host or socket directory (default: "local socket")
#  -p, --port=PORT          database server port (default: "5432")
#  -U, --username=USERNAME  database user name (default: "pborne")
#  -w, --no-password        never prompt for password
#  -W, --password           force password prompt

psql --host=customer-360.cflge37g0yl6.us-east-1.rds.amazonaws.com --port=5432 --username=customer360_usr --dbname=postgres

# Password: Get it from LastPass
