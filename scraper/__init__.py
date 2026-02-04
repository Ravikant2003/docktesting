"""
Docker + Pydoll Fusion Scraper
==============================

A modular web scraping framework that fuses Pydoll with Docker Chrome
for stealthy, scalable web automation.

Quick Start:
    from scraper import DockerPydollFusion
    
    async with DockerPydollFusion() as browser:
        await browser.navigate("https://example.com")
        content = await browser.get_page_source()

Modules:
    - core: Main browser client (DockerPydollFusion)
    - utils: Helper utilities (captcha detection, proxy management)
    - examples: Usage examples
    - tests: Test suite
"""

from .core.browser import DockerPydollFusion, FusionConfig
from .core.cdp import CDPClient, CDPConfig

__version__ = "1.0.0"
__author__ = "Ravikant Saraf"

__all__ = [
    "DockerPydollFusion",
    "FusionConfig", 
    "CDPClient",
    "CDPConfig",
]
