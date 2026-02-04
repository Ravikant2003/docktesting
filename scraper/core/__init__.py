"""
Core module - Main browser automation components
"""

from .browser import DockerPydollFusion, FusionConfig
from .cdp import CDPClient, CDPConfig

__all__ = [
    "DockerPydollFusion",
    "FusionConfig",
    "CDPClient", 
    "CDPConfig",
]
