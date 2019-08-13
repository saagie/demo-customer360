from elasticsearch import Elasticsearch, RequestsHttpConnection
import os
import logging
from requests_aws4auth import AWS4Auth
import random

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


def churn_detection():
    res = es.search(index=index, body={"size": 1000, "query": {"match_all": {}}})
    for hit in res['hits']['hits']:
        customer = hit['_source']
        customer["churn_probability"] = predict_churn(customer["id"])
        res = es.index(index=index, doc_type='customers', id=customer["id"], body=customer)
        print(res['result'])


def predict_churn(id):
    return random.random()


if __name__ == "__main__":
    logger = logging.getLogger("customer-360-churn")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    churn_detection()
