import logging
import psycopg2
import os

S3_BUCKET = "s3://saagiedemo-customer360"
REDSHIFT_SCHEMA = "customer360"
REDSHIFT_DB = "customer360"
REDSHIFT_HOST = os.environ['REDSHIFT_HOST']
REDSHIFT_PORT = "5439"
REDSHIFT_USER = os.environ['REDSHIFT_USER']
REDSHIFT_PWD = os.environ['REDSHIFT_PWD']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

files_to_load = {"tblproduct": "/customer360_demo_rawdata/product.csv",
                 "tblproductcategory": "/customer360_demo_rawdata/product_category.csv",
                 "tblaccount": "/customer360_demo_rawdata/account_sample_data.csv",
                 "tblcontact": "/customer360_demo_rawdata/contact_sample_data.csv",
                 # "tblorder": "",
                 # "tblsupportticket": "",
                 "tblclickstream": "/customer360_demo_rawdata/clickstream_sample_data.csv",
                 }


def main():
    conn_string = "dbname='{}' port='{}' user='{}' password='{}' host='{}'" \
        .format(REDSHIFT_DB, REDSHIFT_PORT, REDSHIFT_USER, REDSHIFT_PWD,
                REDSHIFT_HOST)
    try:
        con = psycopg2.connect(conn_string)
        print("Connection Successful!")
    except:
        print("Unable to connect to Redshift")
    for table, file in files_to_load.items():
        truncate_table_sql = """truncate table {}.{}""".format(REDSHIFT_SCHEMA, table)
        load_table_sql = """copy {}.{} from '{}'\
            credentials 'aws_access_key_id={};aws_secret_access_key={}' \
            DELIMITER ',' IGNOREHEADER AS 1 ACCEPTINVCHARS EMPTYASNULL ESCAPE COMPUPDATE OFF;commit;""" \
            .format(REDSHIFT_SCHEMA,
                    table,
                    S3_BUCKET + file,
                    AWS_ACCESS_KEY_ID,
                    AWS_SECRET_ACCESS_KEY)

        cur = con.cursor()
        try:
            cur.execute(truncate_table_sql)
            cur.execute(load_table_sql)
            print("Copy Command executed successfully")
        except:
            print("Failed to execute copy command")
    con.close()


if __name__ == "__main__":
    logger = logging.getLogger("customer-360")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    main()
