from datetime import datetime

class PicselliaESDocument():

    def __init__(self, metric_type : str, data : dict) -> None:
        self.metric_type = metric_type
        self.service = 'unknown'
        self.timestamp = datetime.now()
        self.data = data

    def toBody(self):
        body = dict()
        body["service"] = self.service
        body["type"] = self.metric_type
        body["timestamp"] = self.timestamp

        for key, value in self.data:
            body[key] = value
       
        return body