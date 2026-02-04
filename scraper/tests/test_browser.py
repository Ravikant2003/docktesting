#!/usr/bin/env python3
"""
Integration Tests for Browser
==============================

These tests require Docker Chrome to be running.
Run with: python -m pytest scraper/tests/test_browser.py -v
"""

import asyncio
import pytest
import sys
sys.path.insert(0, '../..')


@pytest.fixture
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestDockerPydollFusion:
    """Integration tests for DockerPydollFusion"""
    
    @pytest.mark.asyncio
    async def test_connect(self):
        """Test connection to Docker Chrome"""
        from scraper import DockerPydollFusion
        
        browser = DockerPydollFusion()
        connected = await browser.connect()
        
        assert connected == True
        await browser.close()
    
    @pytest.mark.asyncio
    async def test_navigate(self):
        """Test navigation to a URL"""
        from scraper import DockerPydollFusion
        
        async with DockerPydollFusion() as browser:
            success = await browser.navigate("https://httpbin.org/html")
            
            assert success == True
            
            url = await browser.get_current_url()
            assert "httpbin.org" in url
    
    @pytest.mark.asyncio
    async def test_get_page_source(self):
        """Test getting page source"""
        from scraper import DockerPydollFusion
        
        async with DockerPydollFusion() as browser:
            await browser.navigate("https://httpbin.org/html")
            
            source = await browser.get_page_source()
            
            assert len(source) > 0
            assert "<html" in source.lower()
    
    @pytest.mark.asyncio
    async def test_execute_script(self):
        """Test JavaScript execution"""
        from scraper import DockerPydollFusion
        
        async with DockerPydollFusion() as browser:
            await browser.navigate("https://example.com")
            
            title = await browser.execute_script("return document.title")
            
            assert title is not None
    
    @pytest.mark.asyncio
    async def test_screenshot(self):
        """Test taking screenshots"""
        import os
        from scraper import DockerPydollFusion
        
        async with DockerPydollFusion() as browser:
            await browser.navigate("https://example.com")
            
            path = "/tmp/test_screenshot.png"
            success = await browser.screenshot(path)
            
            assert success == True
            assert os.path.exists(path)
            
            # Cleanup
            os.remove(path)
    
    @pytest.mark.asyncio
    async def test_stealth_user_agent(self):
        """Test that stealth User-Agent is applied"""
        from scraper import DockerPydollFusion
        
        async with DockerPydollFusion() as browser:
            await browser.navigate("https://httpbin.org/headers")
            
            source = await browser.get_page_source()
            
            # Should NOT contain "HeadlessChrome"
            assert "HeadlessChrome" not in source
            # Should contain our custom Chrome UA
            assert "Chrome/120" in source


class TestCDPClient:
    """Integration tests for CDPClient"""
    
    @pytest.mark.asyncio
    async def test_connect(self):
        """Test CDP connection"""
        from scraper.core.cdp import CDPClient
        
        cdp = CDPClient()
        connected = await cdp.connect()
        
        assert connected == True
        await cdp.close()
    
    @pytest.mark.asyncio
    async def test_navigate_and_get_html(self):
        """Test CDP navigation and HTML retrieval"""
        from scraper.core.cdp import CDPClient
        
        async with CDPClient() as cdp:
            await cdp.navigate("https://example.com")
            
            html = await cdp.get_html()
            
            assert len(html) > 0
            assert "Example Domain" in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
