import elasticsearch
from .model.elastic_document import PicselliaElasticDocument
from .abstract_client import AbstractPicselliaESClient
import logging

class PicselliaESClient(AbstractPicselliaESClient):

    def __init__(self, es_host: str, es_port : int, client_source: str) -> None:
        self.elasticsearch_client = elasticsearch.Elasticsearch(hosts=[{ 'host' : es_host, 'port' : es_port}])
        self.client_source = client_source

        logging.debug('Connected to ES at {}:{}'.format(es_host, es_port))

    def push(self, index : str, document : PicselliaElasticDocument) -> str:

        document.set_client_source(self.client_source)
        
        object = self.elasticsearch_client.index(index=index, body=document.toBody())

        id = object.get('_id')

        logging.debug('Pushed object with id {} to ES'.format(id))

        return id

    def read(self, index : str, id : str) -> dict:

        object = self.elasticsearch_client.get(index=index, id=id)

        return object.get('_source')