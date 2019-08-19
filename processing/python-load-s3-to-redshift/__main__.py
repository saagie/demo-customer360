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
                 "tblaccount": "/customer360_demo_rawdata/account.csv",
                 "tblcontact": "/customer360_demo_rawdata/contact.csv",
                 "tblorder": "/customer360_demo_rawdata/order_sample_data.csv",
                 "tblclickstream": "/customer360_demo_rawdata/clickstream_sample_data.csv"
                 }


def main():
    conn_string = "dbname='{}' port='{}' user='{}' password='{}' host='{}'" \
        .format(REDSHIFT_DB, REDSHIFT_PORT, REDSHIFT_USER, REDSHIFT_PWD,
                REDSHIFT_HOST)
    try:
        con = psycopg2.connect(conn_string)
        logging.info("Connect to Redshift @ %s ", REDSHIFT_HOST)
    except psycopg2 as e:
        logging.error(e)
        logging.error("Error connecting to redshift. Exiting")
        return 1

    for table, file in files_to_load.items():
        truncate_table_sql = """truncate table {}.{}""".format(REDSHIFT_SCHEMA, table)
        load_table_sql = """copy {}.{} from '{}'\
            credentials 'aws_access_key_id={};aws_secret_access_key={}' \
            DELIMITER ',' IGNOREHEADER AS 1 ACCEPTINVCHARS ACCEPTANYDATE EMPTYASNULL csv quote as '"';commit;""" \
            .format(REDSHIFT_SCHEMA,
                    table,
                    S3_BUCKET + file,
                    AWS_ACCESS_KEY_ID,
                    AWS_SECRET_ACCESS_KEY)

        cur = con.cursor()
        try:
            logging.info("Clean up old data from table %s", table)
            cur.execute(truncate_table_sql)
            logging.info("Load data to  table %s", table)
            cur.execute(load_table_sql)
            logging.info("Succesful loading data to table %s", table)
        except psycopg2.Error as e:
            logging.error(e)
            logging.error("Error loading data to table %s", table)
    con.close()


if __name__ == "__main__":
    logger = logging.getLogger("customer-360")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    main()
