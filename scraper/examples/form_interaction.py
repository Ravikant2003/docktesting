#!/usr/bin/env python3
"""
Form Interaction Example
========================

Shows how to fill forms and interact with elements.
"""

import asyncio
import sys
sys.path.insert(0, '../..')

from scraper import DockerPydollFusion


async def main():
    """Form interaction example"""
    
    print("=" * 50)
    print("Form Interaction Example")
    print("=" * 50)
    
    async with DockerPydollFusion() as browser:
        
        # Go to a form page
        await browser.navigate("https://httpbin.org/forms/post")
        
        print("\nFilling out form...")
        
        # Type in form fields
        await browser.type_text("name", "custname", "John Doe")
        await browser.type_text("name", "custtel", "555-1234")
        await browser.type_text("name", "custemail", "john@example.com")
        
        print("Form filled!")
        
        # Take a screenshot
        await browser.screenshot("/tmp/form_filled.png")
        print("Screenshot saved to /tmp/form_filled.png")
        
        # Click submit (if needed)
        # await browser.click("css", "button[type='submit']")
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
