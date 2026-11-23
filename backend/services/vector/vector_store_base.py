"""
Vector Store Base Interface for SahyogSetu
Defines the standard contract for vector database backends.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import numpy as np

class VectorStoreBase(ABC):
    """Abstract interface for vector database storage and retrieval."""

    @abstractmethod
    def initialize(self) -> None:
        """Initializes storage structures, tables, and indices."""
        pass

    @abstractmethod
    def insert_chunks(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: List[np.ndarray],
    ) -> int:
        """Stores chunk records with their corresponding dense vectors."""
        pass

    @abstractmethod
    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Performs cosine similarity search with metadata filtering."""
        pass

    @abstractmethod
    def get_chunk(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single chunk by chunk_id."""
        pass

    @abstractmethod
    def delete_document(self, doc_id: str) -> int:
        """Deletes all chunks associated with a document ID."""
        pass

    @abstractmethod
    def count_vectors(self) -> int:
        """Returns the total number of indexed vector chunks."""
        pass

    @abstractmethod
    def get_indexed_doc_ids(self) -> List[str]:
        """Returns the list of indexed document IDs."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Removes all indexed chunks and documents."""
        pass
