from elasticsearch import Elasticsearch
from constants.constants import ElasticsearchSettings
from constants.json_constants import JsonBaseModelKeys


def connect_elasticsearch():
    _es_host = [{'host': ElasticsearchSettings.HOST,
                 'port': ElasticsearchSettings.PORT,
                 'scheme': ElasticsearchSettings.SCHEME}]
    _es_connection = Elasticsearch(hosts=_es_host,
                                   http_auth=('elastic', '2DYh1mXUV+62ftcXuBRE'),
                                   ssl_assert_fingerprint='2741f77b595a1598066cb2676f6e774974d3ee98530e1539bbe4fe4b5ec18644')
    if _es_connection.ping():
        print('pong')
    else:
        print('did not connect')
    return _es_connection


def process_es_data(index_data, routing=None):
    es_data_queue.append(index_data)
    dequeued_data = es_data_queue.pop(0)
    if routing:
        es_connection.index(index='plan',
                            id=dequeued_data.get(JsonBaseModelKeys.OBJECT_ID),
                            body=dequeued_data,
                            routing=routing,
                            request_timeout=30)
    else:
        es_connection.index(index='plan',
                            id=dequeued_data.get(JsonBaseModelKeys.OBJECT_ID),
                            body=dequeued_data,
                            request_timeout=30)


es_connection = connect_elasticsearch()
es_data_queue = []

