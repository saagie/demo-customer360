import logging
import psycopg2
import os

REDSHIFT_SCHEMA: str = "customer360"
REDSHIFT_DB = "customer360"
REDSHIFT_HOST = os.environ['REDSHIFT_HOST']
REDSHIFT_PORT = "5439"
REDSHIFT_USER = os.environ['REDSHIFT_USER']
REDSHIFT_PWD = os.environ['REDSHIFT_PWD']

def main():
    conn_string = "dbname='{}' port='{}' user='{}' password='{}' host='{}'" \
        .format(REDSHIFT_DB, REDSHIFT_PORT, REDSHIFT_USER, REDSHIFT_PWD,
                REDSHIFT_HOST)
    try:
        con = psycopg2.connect(conn_string)
        logging.info("Connect to Redshift @ %s ", REDSHIFT_HOST)
        cur = con.cursor()
        clickstream_table = "tblClickStreamWithAcctIDMatch"
        truncate_table_sql = """truncate table {}.{}""".format(REDSHIFT_SCHEMA, clickstream_table)
        logging.info(" Clean up old data from table %s", clickstream_table)
        cur.execute(truncate_table_sql)
        logging.info("Wrangle Data for ClickStream. ID Mapping logic execution.....")
        clickstream_idmap_sql = """insert into {}.{} select webid,cast(split_part(webid,'_',2) as integer),
        "datetime",os,browser,response_time_ms,product,url from {}.{}; """.format(REDSHIFT_SCHEMA,
                                                                                             clickstream_table, 
                                                                                  REDSHIFT_SCHEMA, "tblClickStream")
        cur.execute(clickstream_idmap_sql)
        logging.info("Completed ID Sync....")
        con.commit()

    except psycopg2 as e:
        logging.error(e)
        logging.error("Error Processing... Exiting")
        return 1

    con.close()


if __name__ == "__main__":
    logger = logging.getLogger("customer-360")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    main()
