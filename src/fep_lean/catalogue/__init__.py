"""Catalogue data model, roster seal, and canonical Lean body registry.

The exact roster count is derived from the packaged schema-2 seal.

Public API
----------
    TopicEntry          — single theorem row (frozen dataclass)
    FEPTopicCatalogue   — in-memory catalogue loaded from config/topics.yaml
"""

from fep_lean.catalogue.novelty import (
    FormalismNoveltyLedger,
    FormalismNoveltyRecord,
    NoveltyValidationError,
    load_formalism_novelty,
)
from fep_lean.catalogue.registry import (
    BODIES,
    BODY_MODULE_MANIFEST,
    LATEX_EQUATIONS,
    THEOREM_LATEX,
    BodyModule,
    RegistryValidationError,
    validate_body_family_ownership,
)
from fep_lean.catalogue.relations import (
    CapabilityNode,
    CapabilityStatus,
    EdgeKind,
    FormalismEdge,
    FormalismGraph,
    load_formalism_graph,
)
from fep_lean.catalogue.schema import (
    CatalogueMetadata,
    CatalogueMetadataManifest,
    RosterSeal,
    load_catalogue_metadata,
)
from fep_lean.catalogue.semantics import (
    SemanticDisposition,
    SemanticValidationError,
    TheoremMaturityAudit,
    TheoremMaturityRecord,
    load_theorem_maturity,
)
from fep_lean.catalogue.topics import (
    CatalogueValidationError,
    FEPTopicCatalogue,
    TopicEntry,
)

__all__ = [
    "BODIES",
    "BODY_MODULE_MANIFEST",
    "LATEX_EQUATIONS",
    "THEOREM_LATEX",
    "BodyModule",
    "CapabilityNode",
    "CapabilityStatus",
    "CatalogueMetadata",
    "CatalogueMetadataManifest",
    "CatalogueValidationError",
    "EdgeKind",
    "FEPTopicCatalogue",
    "FormalismEdge",
    "FormalismGraph",
    "FormalismNoveltyLedger",
    "FormalismNoveltyRecord",
    "NoveltyValidationError",
    "RegistryValidationError",
    "RosterSeal",
    "SemanticDisposition",
    "SemanticValidationError",
    "TheoremMaturityAudit",
    "TheoremMaturityRecord",
    "TopicEntry",
    "load_catalogue_metadata",
    "load_formalism_graph",
    "load_formalism_novelty",
    "load_theorem_maturity",
    "validate_body_family_ownership",
]
