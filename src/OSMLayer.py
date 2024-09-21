from  .Layer import Layer

class OSMLayer(Layer):
    def __init__(self, postgres_url: str) -> None:
        super().__init__(postgres_url)