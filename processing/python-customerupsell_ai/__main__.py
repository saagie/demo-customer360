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
        logging.info(" Start AI Algo to compute UpSell  ")
        cur.execute(" set search_path to %s;" % REDSHIFT_SCHEMA)
        cur.execute("truncate tblCustomerUpSell;")
        cur.execute("insert into tblCustomerUpSell select acctid,product from tblcustomerclickstreamanalytics where (acctid,visits) in ( select acctid,max(visits) from tblcustomerclickstreamanalytics group by acctid);")
        logging.info("Completed Customer Upsell predictions...")
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
