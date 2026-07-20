"""gauss — OpenGauss integration layer.

Provides the OpenGauss CLI connector, the SQLite session client, and the
orchestrator that binds the LLM and verification layers.

Public API
----------
    check_gauss_cli       — runs `gauss doctor`
    OpenGaussClient       — SQLite database client for topics/turns/logs
    SessionRecord         — data structure for an open session
    GaussRunner           — orchestrator running topics through LLM then Lean
    TopicRunResult        — outcome of a formalization run
"""

from gauss.cli import check_gauss_cli
from gauss.client import OpenGaussClient, SessionRecord
from gauss.runner import GaussRunner, TopicRunResult

__all__ = [
    "check_gauss_cli",
    "OpenGaussClient",
    "SessionRecord",
    "GaussRunner",
    "TopicRunResult",
]
