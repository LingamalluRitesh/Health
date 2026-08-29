"""
HealthPulse AI — Vector Store and Clinical Knowledge RAG Indexer.
Provides cosine similarity embeddings search over medical literature, clinical guidelines, and CDS evidence.
"""

import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ClinicalDocumentChunk:
    doc_id: str
    chunk_index: int
    title: str
    content: str
    metadata: Dict[str, Any]
    embedding: List[float]


class ClinicalVectorStore:
    """In-memory vector database for clinical guideline RAG and semantic retrieval."""

    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.chunks: List[ClinicalDocumentChunk] = []

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        if len(vec_a) != len(vec_b):
            return 0.0
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot / (norm_a * norm_b)

    def add_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        chunk = ClinicalDocumentChunk(
            doc_id=doc_id,
            chunk_index=len(self.chunks),
            title=title,
            content=content,
            metadata=metadata or {},
            embedding=embedding,
        )
        self.chunks.append(chunk)

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        min_similarity: float = 0.5,
    ) -> List[Tuple[ClinicalDocumentChunk, float]]:
        scores = []
        for chunk in self.chunks:
            sim = self._cosine_similarity(query_embedding, chunk.embedding)
            if sim >= min_similarity:
                scores.append((chunk, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def count(self) -> int:
        return len(self.chunks)


vector_index = ClinicalVectorStore()
