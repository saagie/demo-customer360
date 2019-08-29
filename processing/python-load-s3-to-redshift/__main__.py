import logging
import psycopg2
import os


REDSHIFT_SCHEMA = os.environ["REDSHIFT_SCHEMA"]
REDSHIFT_DB = os.environ["REDSHIFT_DB"]
REDSHIFT_HOST = os.environ['REDSHIFT_HOST']
REDSHIFT_PORT = os.environ['REDSHIFT_PORT']
REDSHIFT_USER = os.environ['REDSHIFT_USER']
REDSHIFT_PWD = os.environ['REDSHIFT_PWD']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
S3_BUCKET = os.environ['AWS_S3_BUCKET_NAME']
S3_PATH = os.environ['AWS_S3_BUCKET_PATH']

files_to_load = {"tblproduct": S3_PATH+"/tblproduct.csv",
                 "tblproductcategory": S3_PATH+"/tblproductcategory.csv",
                 "tblaccount": S3_PATH+"/account.csv",
                 "tblcontact": S3_PATH+"/contact.csv",
                 "tblorder": S3_PATH+"/tblorder.csv",
                 "tblclickstream": S3_PATH+"/tblclickstream.csv"
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
                    's3://'+S3_BUCKET + '/' + file,
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
