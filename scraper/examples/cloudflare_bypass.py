#!/usr/bin/env python3
"""
Cloudflare Bypass Example
=========================

Shows how to scrape Cloudflare-protected sites.
"""

import asyncio
import sys
sys.path.insert(0, '../..')

from scraper import DockerPydollFusion, FusionConfig


async def main():
    """Cloudflare bypass example"""
    
    print("=" * 50)
    print("Cloudflare Bypass Example")
    print("=" * 50)
    
    # Configure with Cloudflare bypass enabled
    config = FusionConfig(
        enable_cloudflare_bypass=True,
        page_load_wait=5.0,  # Wait longer for Cloudflare
    )
    
    # Sites to test
    sites = [
        ("Indeed", "https://www.indeed.com/"),
        ("Booking", "https://www.booking.com/"),
        ("eBay", "https://www.ebay.com/"),
    ]
    
    async with DockerPydollFusion(config) as browser:
        
        for name, url in sites:
            print(f"\n>>> Testing {name}...")
            
            await browser.navigate(url, wait=5)
            
            # Wait for Cloudflare to pass
            passed = await browser.wait_for_cloudflare(timeout=10)
            
            current_url = await browser.get_current_url()
            content = await browser.get_page_source()
            
            print(f"    URL: {current_url[:60]}...")
            print(f"    Size: {len(content)} bytes")
            print(f"    Status: {'✅ PASSED' if passed else '⚠️ CHALLENGE'}")
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
