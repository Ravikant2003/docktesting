#!/usr/bin/env python3
"""
Docker + Pydoll Fusion Scraper
==============================

Main entry point for running the scraper.

Usage:
    python3 main.py                     # Run demo
    python3 main.py --url https://...   # Scrape a URL
    python3 main.py --test              # Run tests
"""

import asyncio
import argparse
import logging
import sys

from scraper import DockerPydollFusion, FusionConfig


async def demo():
    """Run a demo scraping session"""
    print("=" * 60)
    print("Docker + Pydoll Fusion Scraper - Demo")
    print("=" * 60)
    print()
    
    sites = [
        ("Indeed", "https://www.indeed.com/"),
        ("Booking", "https://www.booking.com/"),
        ("eBay", "https://www.ebay.com/"),
    ]
    
    async with DockerPydollFusion() as browser:
        for name, url in sites:
            print(f">>> Scraping {name}...")
            
            await browser.navigate(url, wait=5)
            passed = await browser.wait_for_cloudflare(timeout=10)
            
            current_url = await browser.get_current_url()
            content = await browser.get_page_source()
            
            status = "PASSED" if passed else "CHALLENGE"
            print(f"    [{status}] | {len(content)} bytes | {current_url[:50]}...")
    
    print()
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)


async def scrape_url(url: str, output: str = None, screenshot: str = None):
    """Scrape a single URL"""
    print(f"Scraping: {url}")
    
    async with DockerPydollFusion() as browser:
        await browser.navigate(url, wait=5)
        await browser.wait_for_cloudflare()
        
        content = await browser.get_page_source()
        final_url = await browser.get_current_url()
        
        print(f"Final URL: {final_url}")
        print(f"Content size: {len(content)} bytes")
        
        if output:
            with open(output, 'w') as f:
                f.write(content)
            print(f"Saved to: {output}")
        
        if screenshot:
            await browser.screenshot(screenshot)
            print(f"Screenshot saved to: {screenshot}")
        else:
            print("\nContent preview:")
            print(content[:500])


def run_tests():
    """Run the test suite"""
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "scraper/tests/", "-v"],
        cwd="."
    )
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Docker + Pydoll Fusion Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                          # Run demo
    python main.py --url https://google.com # Scrape URL
    python main.py --url https://... -o page.html  # Save to file
    python main.py --test                   # Run tests
        """
    )
    
    parser.add_argument(
        "--url", "-u",
        help="URL to scrape"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    parser.add_argument(
        "--screenshot", "-s",
        help="Screenshot file path (e.g., result.png)"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run tests"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Suppress noisy loggers
    logging.getLogger("websockets").setLevel(logging.WARNING)
    logging.getLogger("pydoll").setLevel(logging.WARNING)
    
    if args.test:
        sys.exit(run_tests())
    elif args.url:
        asyncio.run(scrape_url(args.url, args.output, args.screenshot))
    else:
        asyncio.run(demo())


if __name__ == "__main__":
    main()
