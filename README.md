# Docker + Pydoll Fusion Scraper

A modular, stealthy web scraper that fuses **Pydoll** with **Docker Chrome** for reliable, scalable web automation.

## Features

- **Cloudflare Bypass** - Automatic Turnstile solving via Pydoll
- **Stealth Mode** - User-Agent spoofing, webdriver removal, fingerprint masking
- **Docker Isolation** - Chrome runs in a container, no local browser needed
- **Human-like Behavior** - Random delays, smooth scrolling
- **Modular Design** - Clean, testable, extensible architecture

## Quick Start

### 1. Start Docker Chrome
```bash
docker run -d -p 3000:3000 browserless/chrome
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Demo
```bash
python main.py
```

## Usage

### Basic Scraping
```python
from scraper import DockerPydollFusion

async with DockerPydollFusion() as browser:
    await browser.navigate("https://example.com")
    content = await browser.get_page_source()
    print(f"Got {len(content)} bytes")
```

### With Configuration
```python
from scraper import DockerPydollFusion, FusionConfig

config = FusionConfig(
    docker_host="localhost",
    docker_port=3000,
    enable_cloudflare_bypass=True,
    human_like_delays=True,
)

async with DockerPydollFusion(config) as browser:
    await browser.navigate("https://protected-site.com")
    await browser.wait_for_cloudflare(timeout=15)
    content = await browser.get_page_source()
```

### Form Interaction
```python
async with DockerPydollFusion() as browser:
    await browser.navigate("https://example.com/login")
    
    # Type with human-like delays
    await browser.type_text("name", "username", "myuser")
    await browser.type_text("name", "password", "mypass")
    
    # Click login button
    await browser.click("css", "button[type='submit']")
```

### Screenshots
```python
async with DockerPydollFusion() as browser:
    await browser.navigate("https://example.com")
    await browser.screenshot("/tmp/page.png")
```

## Project Structure

```
docker2/
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project configuration
├── docker-compose.yml      # Docker setup
├── scraper/                # Main package
│   ├── __init__.py
│   ├── core/               # Core components
│   │   ├── browser.py      # DockerPydollFusion
│   │   └── cdp.py          # Low-level CDP client
│   ├── utils/              # Utility modules
│   │   ├── captcha.py      # CAPTCHA detection
│   │   ├── proxy.py        # Proxy management
│   │   └── stealth.py      # Stealth configuration
│   ├── examples/           # Usage examples
│   │   ├── basic_usage.py
│   │   ├── cloudflare_bypass.py
│   │   └── form_interaction.py
│   └── tests/              # Test suite
│       ├── test_utils.py
│       └── test_browser.py
```

## Testing

```bash
# Run all tests
python main.py --test

# Or with pytest directly
pytest scraper/tests/ -v
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `docker_host` | `localhost` | Docker Chrome host |
| `docker_port` | `3000` | Docker Chrome port |
| `user_agent` | Chrome 120 | Browser User-Agent |
| `enable_cloudflare_bypass` | `True` | Enable Cloudflare solving |
| `inject_stealth_scripts` | `True` | Inject stealth JS |
| `human_like_delays` | `True` | Add random delays |
| `page_load_wait` | `3.0` | Seconds to wait after navigation |

## Architecture

```
┌─────────────────────────────────────────┐
│         Your Python Code                │
│      (main.py / your scripts)           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│       DockerPydollFusion                │
│  (scraper/core/browser.py)              │
│  - Stealth patches                      │
│  - Cloudflare bypass                    │
│  - Human-like behavior                  │
└────────────────┬────────────────────────┘
                 │ uses
                 ▼
┌─────────────────────────────────────────┐
│           Pydoll Library                │
│  - CDP communication                    │
│  - Event handling                       │
└────────────────┬────────────────────────┘
                 │ WebSocket
                 ▼
┌─────────────────────────────────────────┐
│       Docker browserless/chrome         │
│  - Headless Chrome                      │
│  - Port 3000                            │
└─────────────────────────────────────────┘
```

---

## Detailed Flow Diagram

### Complete Request Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              USER REQUEST                                     │
│                     python main.py --url https://site.com                     │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  main.py (CLI Entry Point)                                                   │
│  ─────────────────────────                                                   │
│  - Parses command line arguments (--url, --screenshot, --output)             │
│  - Sets up logging configuration                                             │
│  - Calls scrape_url() or demo() async function                               │
│  - Handles --test flag to run pytest                                         │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  scraper/__init__.py (Package Entry)                                         │
│  ────────────────────────────────────                                        │
│  - Exports: DockerPydollFusion, FusionConfig                                 │
│  - Exports: CaptchaDetector, ProxyManager, StealthConfig                     │
│  - Provides clean public API for the package                                 │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  scraper/core/browser.py (Main Fusion Class)                                 │
│  ───────────────────────────────────────────                                 │
│                                                                              │
│  class DockerPydollFusion:                                                   │
│    1. _patch_pydoll_validator()                                              │
│       └─ Patches Pydoll to accept Docker's ws://localhost:3000 URL           │
│                                                                              │
│    2. connect()                                                              │
│       ├─ Checks Docker Chrome is running (HTTP /json/version)                │
│       ├─ Creates Pydoll Chrome instance                                      │
│       ├─ Connects via WebSocket to Docker Chrome                             │
│       ├─ Calls _inject_stealth() for fingerprint masking                     │
│       └─ Enables Cloudflare auto-bypass                                      │
│                                                                              │
│    3. navigate(url)                                                          │
│       ├─ Calls Pydoll's go_to(url)                                           │
│       └─ Adds human-like random delays                                       │
│                                                                              │
│    4. wait_for_cloudflare()                                                  │
│       └─ Polls page source for Cloudflare indicators                         │
│                                                                              │
│    5. screenshot(path)                                                       │
│       └─ CDP Page.captureScreenshot command                                  │
│                                                                              │
│  class FusionConfig:                                                         │
│    - docker_host, docker_port                                                │
│    - user_agent, platform, languages                                         │
│    - enable_cloudflare_bypass, inject_stealth_scripts                        │
│    - human_like_delays, page_load_wait                                       │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ scraper/utils/      │ │ scraper/utils/      │ │ scraper/utils/      │
│ stealth.py          │ │ captcha.py          │ │ proxy.py            │
│ ────────────────    │ │ ────────────────    │ │ ────────────────    │
│                     │ │                     │ │                     │
│ StealthConfig:      │ │ CaptchaType (enum): │ │ ProxyConfig:        │
│ - user_agent        │ │ - CLOUDFLARE        │ │ - host, port        │
│ - platform          │ │ - RECAPTCHA_V2/V3   │ │ - username, pass    │
│ - languages         │ │ - HCAPTCHA          │ │ - protocol          │
│                     │ │ - SLIDER            │ │                     │
│ inject_stealth():   │ │ - GEETEST           │ │ ProxyManager:       │
│ - UA override       │ │                     │ │ - add_proxy()       │
│ - webdriver=undef   │ │ CaptchaDetector:    │ │ - get_proxy()       │
│ - chrome object     │ │ - detect(html)      │ │ - rotate()          │
│ - plugins array     │ │ - returns type      │ │ - health_check()    │
│ - WebGL spoof       │ │                     │ │                     │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
              │
              │ CDP Commands
              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  scraper/core/cdp.py (Low-Level CDP Client)                                  │
│  ───────────────────────────────────────────                                 │
│                                                                              │
│  class CDPClient:                                                            │
│    - connect(ws_url) - WebSocket connection                                  │
│    - send_command(method, params) - Send CDP command                         │
│    - Emulation.setUserAgentOverride                                          │
│    - Page.addScriptToEvaluateOnNewDocument                                   │
│    - Page.captureScreenshot                                                  │
│    - Runtime.evaluate                                                        │
│                                                                              │
│  (Used for direct CDP when Pydoll doesn't expose a method)                   │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │
                                   │ WebSocket (ws://localhost:3000)
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        DOCKER CONTAINER                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  browserless/chrome (docker-compose.yml)                               │  │
│  │  ─────────────────────────────────────────                             │  │
│  │                                                                        │  │
│  │  - Image: browserless/chrome                                           │  │
│  │  - Port: 3000 (exposed)                                                │  │
│  │  - Headless Chrome with DevTools Protocol                              │  │
│  │  - No GUI needed                                                       │  │
│  │  - Isolated environment                                                │  │
│  │  - Scalable (can run multiple containers)                              │  │
│  │                                                                        │  │
│  │  Endpoints:                                                            │  │
│  │  - ws://localhost:3000  (WebSocket for CDP)                            │  │
│  │  - http://localhost:3000/json/version (Version info)                   │  │
│  │  - http://localhost:3000/json/list (Active pages)                      │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │
                                   │ HTTPS Request
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          TARGET WEBSITE                                       │
│                    (e.g., opensea.io, crunchbase.com)                         │
└──────────────────────────────────────────────────────────────────────────────┘
```

### File Responsibilities Summary

| File | Purpose | Key Functions/Classes |
|------|---------|----------------------|
| `main.py` | CLI entry point | `demo()`, `scrape_url()`, argument parsing |
| `scraper/__init__.py` | Package exports | Public API surface |
| `scraper/core/browser.py` | Main fusion logic | `DockerPydollFusion`, `FusionConfig` |
| `scraper/core/cdp.py` | Raw CDP commands | `CDPClient`, `CDPConfig` |
| `scraper/utils/stealth.py` | Anti-detection | `StealthConfig`, `inject_stealth()` |
| `scraper/utils/captcha.py` | CAPTCHA detection | `CaptchaDetector`, `CaptchaType` |
| `scraper/utils/proxy.py` | Proxy rotation | `ProxyManager`, `ProxyConfig` |
| `docker-compose.yml` | Container config | browserless/chrome on port 3000 |

### Stealth Injection Flow

```
connect() called
     │
     ▼
┌─────────────────────────────────────┐
│ 1. Emulation.setUserAgentOverride   │
│    "HeadlessChrome" → "Chrome/120"  │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 2. Page.addScriptToEvaluate...      │
│    navigator.webdriver = undefined  │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 3. Inject window.chrome object      │
│    Fake Chrome runtime API          │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 4. Spoof navigator.plugins          │
│    Add fake PDF/Flash plugins       │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 5. WebGL vendor/renderer override   │
│    "Google Inc." → "Intel Inc."     │
└─────────────────────────────────────┘
     │
     ▼
  STEALTH READY
```

---

## License

MIT
