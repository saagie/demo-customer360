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
        logging.info(" Start Order Analytics ")
        cur.execute(" set search_path to %s;" % REDSHIFT_SCHEMA)
        cur.execute("truncate tblCustomerOrderAnalytics;")
        cur.execute("insert into  tblCustomerOrderAnalytics select acctid, date_part(y,orderdate), date_part(qtr,orderdate) , count(*) , sum(amount) , avg(discount) from tblorder group by 1,2,3 order by 1,2,3;")
        logging.info(" Completed Order Analytics ")

        logging.info(" Start Order Status Analytics ")
        cur.execute("truncate tblCustomerOrderStatusAnalytics;")
        cur.execute(" insert into tblCustomerOrderStatusAnalytics select acctid, date_part(y,orderdate), date_part(qtr,orderdate) , status, count(*) from tblorder group by 1,2,3,4 order by 1,2,3,4;")
        logging.info(" Completed Order Status Analytics ")

        logging.info(" Start Clickstream Analytics ")
        cur.execute("truncate tblCustomerClickStreamAnalytics")
        cur.execute(" insert into tblCustomerClickStreamAnalytics  select acctid,trunc(\"datetime\"),product,count(*) from tblclickstreamwithacctidmatch group by 1,2,3;")
        logging.info(" Completed Clickstream Analytics ")


        logging.info("Completed Customer Analytics")
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
