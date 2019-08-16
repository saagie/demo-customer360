from elasticsearch import Elasticsearch, RequestsHttpConnection
import json
import os
import getopt
import logging
import sys
from requests_aws4auth import AWS4Auth
from sqlalchemy import create_engine
import urllib.parse
import pandas as pd

AWS_REGION = os.environ['AWS_REGION']
AWS_SERVICE = 'es'
AWS_AUTH = AWS4Auth(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], AWS_REGION, AWS_SERVICE)

ES_HOST = os.environ['ES_HOST']
ES_INDEX = 'customer360'

REDSHIFT_SCHEMA = "customer360"
REDSHIFT_DB = "customer360"
REDSHIFT_HOST = os.environ['REDSHIFT_HOST']
REDSHIFT_PORT = "5439"
REDSHIFT_USER = os.environ['REDSHIFT_USER']
REDSHIFT_PWD = os.environ['REDSHIFT_PWD']

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

es = Elasticsearch(
    hosts=[{'host': ES_HOST, 'port': 443}],
    http_auth=AWS_AUTH,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def get_all():
    res = es.search(index=ES_INDEX, body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


def load_redshift():
    connection_string = """postgresql://{}:{}@{}:5439/{}""".format(REDSHIFT_USER,
                                                                   urllib.parse.quote_plus(REDSHIFT_PWD),
                                                                   REDSHIFT_HOST,
                                                                   REDSHIFT_DB)
    engine = create_engine(connection_string)
    data_frame = pd.read_sql_query(
        'select * from customer360.tblaccount a, customer360.tblchurn b where a.accountnumber=b.id_account', engine)
    result = json.loads(data_frame.to_json(orient='records'))

    for line in result:
        line["billingstate"] = str.upper(line["billingstate"])
        line["upsell"] = 0.0  # FIXME temporary
        res = es.index(index=ES_INDEX, doc_type='customers', id=line["id"], body=line)
        print(res['result'])


def flush_index():
    res = es.indices.delete(index=ES_INDEX, ignore=[400, 404])
    print(res)


def main(argv):
    task = ""
    usage = "__main__.py -t <flush_index|get_all|load_redshift>"
    try:
        opts, args = getopt.getopt(argv, "ht:")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(usage)
            sys.exit()
        elif opt in "-t":
            task = arg
    if task == "flush_index":
        flush_index()
    elif task == "get_all":
        get_all()
    elif task == "load_redshift":
        load_redshift()
    else:
        print("Task not valid")
        print(usage)
        sys.exit()


if __name__ == "__main__":
    logger = logging.getLogger("customer-360")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    main(sys.argv[1:])
