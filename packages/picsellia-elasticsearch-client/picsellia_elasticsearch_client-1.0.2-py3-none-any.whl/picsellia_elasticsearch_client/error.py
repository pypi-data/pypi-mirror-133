from .elastic_document import PicselliaElasticDocument

class PicselliaError(PicselliaElasticDocument):

    def __init__(self, service: str, data: dict) -> None:
        super().__init__('error', service, data)