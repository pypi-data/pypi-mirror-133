from datetime import datetime

class PicselliaElasticDocument():

    def __init__(self, metric_type : str, service : str, data : dict) -> None:
        self.metric_type = metric_type
        self.service = service
        self.timestamp = datetime.now()
        self.data = data

    def set_client_source(self, client_source):
        self.client_source = client_source

    def toBody(self):
        body = dict()
        body["service"] = self.service
        body["metric.type"] = self.metric_type
        body["timestamp"] = self.timestamp

        for key in self.data:
            body_key = "data.{}".format(key)
            body[body_key] = self.data[key]
       
        if self.client_source != None:
            body["client.source"] = self.client_source

        return body