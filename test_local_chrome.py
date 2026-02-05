import asyncio
from pydoll.browser import Chrome

async def main():
    url = "https://www.scrapingcourse.com/antibot-challenge"
    print(f"Testing local Chrome with Pydoll: {url}")
    
    # Use headless=True if you are in a Docker/Server environment 
    # but for local debugging headless=False is fine.
    async with Chrome() as browser:
        tab = await browser.start(headless=False)
        
        await tab.go_to(url)
        # It's better to wait for a specific element than a hard sleep
        await asyncio.sleep(5) 
        
        content = await tab.page_source
        print(f"Content size: {len(content)} bytes")
        
        # Correct way to save a screenshot in Pydoll
        # Note: Ensure the 'tab' is still active here
        try:
            await tab.take_screenshot("local_result.png")
            print("Screenshot saved to: local_result.png")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

if __name__ == "__main__":
    asyncio.run(main())