# Docker + Pydoll Fusion - Complete Guide

## What We Built

We successfully **fused Pydoll with Docker Chrome** to create the ultimate stealth web scraping solution.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR PYTHON CODE                         │
│                DockerPydollFusion()                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    PYDOLL LIBRARY                           │
│  • Cloudflare Turnstile Auto-Bypass                         │
│  • Human-like Click/Type                                    │
│  • Element Finding                                          │
│  • Event Handling                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ WebSocket (ws://localhost:3000)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              DOCKER browserless/chrome                      │
│  • Headless Chrome                                          │
│  • Isolated Environment                                     │
│  • Scalable (multiple containers)                           │
│  • No local Chrome needed                                   │
└─────────────────────────────────────────────────────────────┘
```

## Test Results

| Site | Status | Notes |
|------|--------|-------|
| Indeed.com | PASSED | Loaded job search page |
| Booking.com | PASSED | Full content loaded |
| eBay.com | PASSED | Full content loaded |
| httpbin.org | PASSED | Headers show stealth UA |

## Quick Start

### 1. Start Docker Chrome
```bash
docker run -d -p 3000:3000 browserless/chrome
```

### 2. Use the Fusion Client
```python
import asyncio
from src.docker_pydoll_fusion import DockerPydollFusion

async def scrape():
    async with DockerPydollFusion() as browser:
        # Navigate with stealth
        await browser.navigate("https://example.com")
        
        # Get page content
        source = await browser.get_page_source()
        print(f"Got {len(source)} bytes")
        
        # Find and click elements
        await browser.click("css", "button.submit")
        
        # Type in forms
        await browser.type_text("name", "email", "test@example.com")
        
        # Take screenshots
        await browser.screenshot("/tmp/page.png")

asyncio.run(scrape())
```

## Key Features

### 1. Automatic Stealth Patches
- **User-Agent**: Overridden from "HeadlessChrome" to real Chrome
- **navigator.webdriver**: Removed (undefined)
- **window.chrome**: Added fake chrome object
- **navigator.plugins**: Faked
- **WebGL Vendor/Renderer**: Spoofed to Intel

### 2. Cloudflare Bypass
```python
# Automatically enabled!
await browser.navigate("https://cloudflare-protected-site.com")

# Wait for Cloudflare challenge to pass
bypassed = await browser.wait_for_cloudflare(timeout=15)
```

### 3. Human-like Interaction
```python
# Type with random delays (30-120ms per character)
await browser.type_text("name", "search", "query")

# Smooth scrolling with random variations
await browser.scroll_down(500)
```

## Files

| File | Description |
|------|-------------|
| `src/docker_pydoll_fusion.py` | **Main fusion module** |
| `src/cdp_client.py` | Raw CDP client |
| `src/pydoll_client.py` | Legacy Pydoll wrapper |
| `src/captcha_detector.py` | CAPTCHA type detection |
| `src/proxy_manager.py` | IP rotation |
| `src/vlm_solver.py` | Vision LLM CAPTCHA solver |
| `pydoll_docker_fusion_demo.py` | Demo script |

## Limitations

1. **Datacenter IP**: Docker runs on datacenter IPs which some sites block
   - Solution: Use residential proxy with Docker

2. **Hard Cloudflare Challenges**: Sites like nowsecure.nl have enhanced detection
   - Solution: Use local Pydoll (non-Docker) for hardest sites

3. **Headless Detection**: Some sites detect headless mode
   - Solution: Use headful Docker Chrome or Xvfb

## Configuration

```python
from src.docker_pydoll_fusion import DockerPydollFusion, FusionConfig

config = FusionConfig(
    docker_host="localhost",
    docker_port=3000,
    
    # Stealth settings
    user_agent="Mozilla/5.0 (Macintosh...",
    platform="macOS",
    
    # Behavior
    enable_cloudflare_bypass=True,
    inject_stealth_scripts=True,
    human_like_delays=True,
    
    # Timeouts
    page_load_wait=3.0,
    cloudflare_wait=10.0,
)

async with DockerPydollFusion(config) as browser:
    # ...
```

## Summary

We successfully:
1. Connected Pydoll to Docker Chrome via WebSocket
2. Patched Pydoll's validator for Docker compatibility
3. Injected stealth patches (UA, webdriver, etc.)
4. Enabled Cloudflare auto-bypass
5. Tested on real Cloudflare-protected sites
6. Created reusable `DockerPydollFusion` class

**The fusion is complete!**
