"""
Stealth Configuration and Injection
====================================

Provides stealth patches to avoid bot detection.
"""

import json
import logging
from typing import List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class StealthConfig:
    """Stealth configuration for browser fingerprinting"""
    
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    platform: str = "macOS"
    languages: List[str] = field(default_factory=lambda: ["en-US", "en"])
    vendor: str = "Google Inc."
    webgl_vendor: str = "Intel Inc."
    webgl_renderer: str = "Intel Iris Pro Graphics"


async def inject_stealth(handler, config: StealthConfig, timeout: int = 30):
    """
    Inject stealth patches into a browser session via CDP.
    
    Args:
        handler: Pydoll connection handler or CDP client
        config: Stealth configuration
        timeout: Command timeout in seconds
    """
    
    # 1. Override User-Agent
    await handler.execute_command({
        'method': 'Network.enable',
        'params': {}
    }, timeout=timeout)
    
    await handler.execute_command({
        'method': 'Network.setUserAgentOverride',
        'params': {
            'userAgent': config.user_agent,
            'platform': config.platform,
            'acceptLanguage': ','.join(config.languages)
        }
    }, timeout=timeout)
    logger.debug(f"User-Agent set: {config.user_agent[:50]}...")
    
    # 2. Inject stealth JavaScript
    stealth_js = f'''
    // Remove webdriver flag
    Object.defineProperty(navigator, 'webdriver', {{ get: () => undefined }});

    // Add chrome object
    window.chrome = {{
        runtime: {{}},
        loadTimes: function() {{ return {{}}; }},
        csi: function() {{ return {{}}; }},
        app: {{}}
    }};

    // Fix navigator properties
    Object.defineProperty(navigator, 'plugins', {{ get: () => [1, 2, 3, 4, 5] }});
    Object.defineProperty(navigator, 'languages', {{ get: () => {json.dumps(config.languages)} }});
    Object.defineProperty(navigator, 'platform', {{ get: () => 'MacIntel' }});
    Object.defineProperty(navigator, 'vendor', {{ get: () => '{config.vendor}' }});

    // Spoof timezone
    Object.defineProperty(Intl.DateTimeFormat().resolvedOptions(), 'timeZone', {{ get: () => 'America/New_York' }});

    // Spoof hardwareConcurrency
    Object.defineProperty(navigator, 'hardwareConcurrency', {{ get: () => 8 }});

    // Spoof mediaDevices
    if (navigator.mediaDevices) {{
        Object.defineProperty(navigator.mediaDevices, 'enumerateDevices', {{
            value: () => Promise.resolve([
                {{ kind: 'audioinput', label: 'Microphone', deviceId: 'default' }},
                {{ kind: 'audiooutput', label: 'Speaker', deviceId: 'default' }},
                {{ kind: 'videoinput', label: 'Webcam', deviceId: 'default' }}
            ])
        }})
    }}

    // Spoof screen properties
    Object.defineProperty(window, 'outerWidth', {{ get: () => 1920 }});
    Object.defineProperty(window, 'outerHeight', {{ get: () => 1080 }});
    Object.defineProperty(window.screen, 'width', {{ get: () => 1920 }});
    Object.defineProperty(window.screen, 'height', {{ get: () => 1080 }});
    Object.defineProperty(window, 'devicePixelRatio', {{ get: () => 1 }});

    // Simulate mouse movement
    window.addEventListener('DOMContentLoaded', function() {{
        let evt = new MouseEvent('mousemove', {{
            clientX: 100,
            clientY: 100,
            bubbles: true
        }});
        document.dispatchEvent(evt);
    }});

    // Fix permissions query
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({{ state: Notification.permission }}) :
            originalQuery(parameters)
    );

    // WebGL vendor/renderer spoofing
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {{
        if (parameter === 37445) return '{config.webgl_vendor}';
        if (parameter === 37446) return '{config.webgl_renderer}';
        return getParameter.apply(this, arguments);
    }};
    '''
    
    await handler.execute_command({
        'method': 'Page.addScriptToEvaluateOnNewDocument',
        'params': {'source': stealth_js}
    }, timeout=timeout)
    
    logger.debug("Stealth JavaScript injected")


# Common user agents for rotation
USER_AGENTS = [
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


def get_random_user_agent() -> str:
    """Get a random user agent from the pool"""
    import random
    return random.choice(USER_AGENTS)
