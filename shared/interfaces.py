from abc import ABC, abstractmethod

from .schemas import Evidence


class KnowledgeRepresentation(ABC):
    @abstractmethod
    def build(self, documents):
        """
        Build the knowledge representation from source documents.
        """
        pass


class Retriever(ABC):
    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[Evidence]:
        """
        Retrieve relevant evidence for a user query.
        """
        pass