REPRESENTATIONS = {}
RETRIEVERS = {}


def register_representation(name: str, representation):
    REPRESENTATIONS[name] = representation


def register_retriever(name: str, retriever):
    RETRIEVERS[name] = retriever


def get_representation(name: str):
    return REPRESENTATIONS[name]


def get_retriever(name: str):
    return RETRIEVERS[name]