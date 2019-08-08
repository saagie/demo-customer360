import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
import json
import os
import getopt
import logging
import sys
from requests_aws4auth import AWS4Auth

region = os.environ['AWS_REGION']
service = 'es'
awsauth = AWS4Auth(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], region, service)
bucket = "saagiedemo-customer360"

host = os.environ['ES_HOST']
index = 'customer360'

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def get_all():
    res = es.search(index=index, body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


def index_customers():
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key="customer/input/customers.json")
    body = obj['Body'].read().decode('utf-8')
    lines = body.splitlines()

    for line in lines:
        parsed_line = json.loads(line)
        parsed_line["churn_probability"] = 0.0
        parsed_line["upsell"] = 0.0
        res = es.index(index=index, doc_type='customers', id=parsed_line["id"], body=parsed_line)
        print(res['result'])


def flush_index():
    res = es.indices.delete(index=index, ignore=[400, 404])
    print(res)


def main(argv):
    task = ""
    usage = "__main__.py -t <flush_index|get_all|index_customers>"
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
    elif task == "index_customers":
        index_customers()
    else:
        print("Task not valid")
        print(usage)
        sys.exit()


if __name__ == "__main__":
    logger = logging.getLogger("customer-360")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    main(sys.argv[1:])
