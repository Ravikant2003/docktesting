#!/usr/bin/env python3
"""
Basic Usage Example
===================

Shows the simplest way to use the scraper.
"""

import asyncio
import sys
sys.path.insert(0, '../..')

from scraper import DockerPydollFusion


async def main():
    """Basic scraping example"""
    
    print("=" * 50)
    print("Basic Scraping Example")
    print("=" * 50)
    
    # Method 1: Using context manager (recommended)
    async with DockerPydollFusion() as browser:
        
        # Navigate to a page
        await browser.navigate("https://httpbin.org/headers")
        
        # Get page content
        content = await browser.get_page_source()
        print(f"\nPage content ({len(content)} bytes):")
        print(content[:500])
        
        # Get current URL
        url = await browser.get_current_url()
        print(f"\nCurrent URL: {url}")
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
