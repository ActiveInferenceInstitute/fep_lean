"""catalogue — FEP topic catalogue data model.

Provides the canonical YAML-backed catalogue of 50 FEP theorems.

Public API
----------
    TopicEntry          — single theorem row (frozen dataclass)
    FEPTopicCatalogue   — in-memory catalogue loaded from config/topics.yaml
"""

from catalogue.topics import FEPTopicCatalogue, TopicEntry

__all__ = ["TopicEntry", "FEPTopicCatalogue"]
