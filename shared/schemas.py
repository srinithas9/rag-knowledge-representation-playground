from dataclasses import dataclass, field
from typing import Any


@dataclass
class Evidence:
    """
    Standard evidence returned by every retrieval component.
    """

    content: str
    source_id: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)