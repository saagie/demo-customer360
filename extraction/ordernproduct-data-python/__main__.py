import csv
import smart_open
import psycopg2
import sys
import os
import io

AWS_REGION = os.environ['AWS_REGION']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_S3_BUCKET_NAME = os.environ['AWS_S3_BUCKET_NAME']
AWS_S3_BUCKET_PATH = os.environ['AWS_S3_BUCKET_PATH']

POSTGRES_SCHEMA = os.environ['POSTGRES_SCHEMA']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PWD = os.environ['POSTGRES_PWD']

tables = ['tblclickstream', 'tblorder', 'tblproduct', 'tblproductcategory']

def fetch_and_upload(schema, table):
    cursor = None
    conn = None
    buffer = None
    s3 = None

    try:

        # print('AWS_REGION = ' + AWS_REGION)
        # print('AWS_ACCESS_KEY_ID = ' + AWS_ACCESS_KEY_ID)
        # print('AWS_SECRET_ACCESS_KEY = ' + AWS_SECRET_ACCESS_KEY)
        # print('AWS_S3_BUCKET_NAME = ' + AWS_S3_BUCKET_NAME)
        # print('AWS_S3_BUCKET_PATH = ' + AWS_S3_BUCKET_PATH)

        s3_bucket = "s3://" + AWS_ACCESS_KEY_ID + ":" + AWS_SECRET_ACCESS_KEY \
                    + "@" + AWS_S3_BUCKET_NAME + "/" + AWS_S3_BUCKET_PATH \
                    + "/" + table + ".csv"

        # print("S3 bucket: " + s3_bucket)
        print('Connecting to S3...')
        s3 = smart_open.smart_open(s3_bucket, 'wb')
        print('Successfully connected to S3...')

        print('Connecting to PG...')
        print('dbname = ' + POSTGRES_DB)
        print('user = ' + POSTGRES_USER)
        print('host = ' + POSTGRES_HOST)
        print('port = ' + POSTGRES_PORT)
        conn = psycopg2.connect(dbname=POSTGRES_DB,
                                user=POSTGRES_USER,
                                host=POSTGRES_HOST,
                                port=POSTGRES_PORT,
                                password=POSTGRES_PWD)
        print('Successfully connected to PG...')

        cursor = conn.cursor(name='customer360')
        query = "select * from " + schema + "." + table
        print('Query: ' + query)
        cursor.execute(query)

        # Fetch the first batch
        records = cursor.fetchmany(size=2000)

        # Retrieve the names of the columns
        field_names = [desc.name for desc in cursor.description]

        # Prepare a buffer in memory to write to
        buffer = io.StringIO()

        # Add the column names to the buffer
        csv_writer = csv.writer(buffer, delimiter=',')
        csv_writer.writerow(field_names)

        # Iterate on the result set from PostgreSQL
        while records:
            for r in records:
                csv_writer.writerow(r)

            # Upload to S3
            s3.write(buffer.getvalue().encode())
            s3.flush()

            # Reset the buffer
            buffer.seek(0)
            buffer.truncate(0)

            # Next batch
            records = cursor.fetchmany(size=2000)

    except (Exception, psycopg2.Error) as error:
        print("Error: ", error)

    finally:
        if s3:
            s3.close()
        if buffer:
            buffer.close()
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    # logger = logging.getLogger("customer-360")
    # logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

    print(sys.version)

    for t in tables:
        print("Processing " + POSTGRES_SCHEMA + "." + t)
        fetch_and_upload(POSTGRES_SCHEMA, t)

    print("Done")
