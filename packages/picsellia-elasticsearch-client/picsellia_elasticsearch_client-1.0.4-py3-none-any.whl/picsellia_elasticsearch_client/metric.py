from .document import PicselliaESDocument

class PicselliaESMetric(PicselliaESDocument):

    def __init__(self, **kwargs) -> None:
        super().__init__('metric', kwargs.items())