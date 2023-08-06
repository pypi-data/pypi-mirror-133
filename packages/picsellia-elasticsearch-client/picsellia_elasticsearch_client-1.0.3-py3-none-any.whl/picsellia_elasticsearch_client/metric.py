from .elastic_document import PicselliaElasticDocument

class PicselliaMetric(PicselliaElasticDocument):

    def __init__(self, service: str, data: dict) -> None:
        super().__init__('metric', service, data)