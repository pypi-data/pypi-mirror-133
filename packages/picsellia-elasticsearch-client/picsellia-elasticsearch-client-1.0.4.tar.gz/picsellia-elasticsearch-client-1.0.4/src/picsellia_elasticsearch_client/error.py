from .document import PicselliaESDocument

class PicselliaESError(PicselliaESDocument):

    def __init__(self, **kwargs) -> None:
        super().__init__('error', kwargs.items())