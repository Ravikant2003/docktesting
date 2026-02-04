"""
Docker + Pydoll Fusion Browser Client
=====================================

The main browser automation client that fuses Pydoll with Docker Chrome.

Usage:
    async with DockerPydollFusion() as browser:
        await browser.navigate("https://example.com")
        content = await browser.get_page_source()
"""

import asyncio
import random
import logging
import json
import urllib.request
from typing import Optional, Any, List
from dataclasses import dataclass, field

try:
    from pydoll.browser import Chrome as PydollChrome
    from pydoll.constants import By
    PYDOLL_AVAILABLE = True
except ImportError:
    PYDOLL_AVAILABLE = False
    PydollChrome = None
    By = None

from ..utils.stealth import StealthConfig, inject_stealth

logger = logging.getLogger(__name__)


@dataclass
class FusionConfig:
    """Configuration for Docker + Pydoll fusion"""
    
    # Docker Chrome settings
    docker_host: str = "localhost"
    docker_port: int = 3000
    
    # Stealth settings
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    platform: str = "macOS"
    languages: List[str] = field(default_factory=lambda: ["en-US", "en"])
    
    # Timeouts
    connect_timeout: int = 30
    command_timeout: int = 60
    page_load_wait: float = 3.0
    cloudflare_wait: float = 10.0
    
    # Behavior
    enable_cloudflare_bypass: bool = True
    inject_stealth_scripts: bool = True
    human_like_delays: bool = True
    
    # VLM CAPTCHA Solver settings
    vlm_enabled: bool = False
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "minicpm-v:8b"


class DockerPydollFusion:
    """
    Fuses Pydoll with Docker Chrome for ultimate stealth.
    
    This class:
    1. Patches Pydoll to accept Docker's WebSocket URL
    2. Connects Pydoll to Docker Chrome
    3. Injects stealth patches (UA, webdriver, etc.)
    4. Enables Cloudflare bypass
    5. Provides convenient navigation/scraping methods
    """
    
    def __init__(self, config: Optional[FusionConfig] = None):
        if not PYDOLL_AVAILABLE:
            raise ImportError("Pydoll is not installed. Run: pip install pydoll")
        
        self.config = config or FusionConfig()
        self._browser: Optional[PydollChrome] = None
        self._tab = None
        self._handler = None
        self._patched = False
        self._vlm_solver = None
        
    def _patch_pydoll_validator(self):
        """Patch Pydoll to accept Docker's short WebSocket URL"""
        if self._patched:
            return
            
        @staticmethod
        def patched_validate(ws_address: str):
            if not ws_address.startswith('ws://'):
                from pydoll.exceptions import InvalidWebSocketAddress
                raise InvalidWebSocketAddress('WebSocket address must start with ws://')
            logger.debug(f"Allowing WebSocket: {ws_address}")
        
        PydollChrome._validate_ws_address = patched_validate
        self._patched = True
        logger.info("Patched Pydoll validator for Docker compatibility")
    
    async def _inject_stealth(self):
        """Inject stealth patches via CDP"""
        if not self.config.inject_stealth_scripts:
            return
        
        stealth_config = StealthConfig(
            user_agent=self.config.user_agent,
            platform=self.config.platform,
            languages=self.config.languages,
        )
        await inject_stealth(self._handler, stealth_config, self.config.command_timeout)
        logger.info("Stealth patches injected")
    
    async def connect(self) -> bool:
        """Connect to Docker Chrome via Pydoll"""
        try:
            self._patch_pydoll_validator()
            
            ws_url = f"ws://{self.config.docker_host}:{self.config.docker_port}"
            http_url = f"http://{self.config.docker_host}:{self.config.docker_port}/json/version"
            
            try:
                response = urllib.request.urlopen(http_url, timeout=5)
                version = json.loads(response.read().decode())
                logger.info(f"Docker Chrome: {version.get('Browser', 'Unknown')}")
            except Exception as e:
                logger.error(f"Docker Chrome not running at {http_url}: {e}")
                return False
            
            self._browser = PydollChrome()
            self._tab = await self._browser.connect(ws_url)
            self._handler = self._tab._connection_handler
            
            logger.info(f"Connected to Docker Chrome at {ws_url}")
            
            await self._inject_stealth()
            
            if self.config.enable_cloudflare_bypass:
                await self._tab.enable_auto_solve_cloudflare_captcha()
                logger.info("Cloudflare auto-bypass enabled")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False
    
    async def navigate(self, url: str, wait: Optional[float] = None) -> bool:
        """Navigate to a URL with stealth"""
        if not self._tab:
            raise RuntimeError("Not connected. Call connect() first.")
        
        try:
            await self._tab.go_to(url)
            
            wait_time = wait or self.config.page_load_wait
            if self.config.human_like_delays:
                wait_time += random.uniform(0.5, 1.5)
            await asyncio.sleep(wait_time)
            
            current_url = await self._tab.current_url
            logger.info(f"Navigated to: {current_url}")
            return True
            
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    async def wait_for_cloudflare(self, timeout: float = 15.0) -> bool:
        """Wait for Cloudflare challenge to be bypassed"""
        if not self._tab:
            raise RuntimeError("Not connected")
        
        start = asyncio.get_event_loop().time()
        
        while (asyncio.get_event_loop().time() - start) < timeout:
            try:
                source = await self._tab.page_source
                cf_indicators = ['cf-turnstile', 'challenge-running', 'Just a moment']
                if not any(ind in source for ind in cf_indicators):
                    return True
                await asyncio.sleep(1)
            except Exception:
                await asyncio.sleep(1)
        
        return False
    
    async def get_page_source(self) -> str:
        """Get the current page HTML source"""
        if not self._tab:
            raise RuntimeError("Not connected")
        return await self._tab.page_source
    
    async def get_current_url(self) -> str:
        """Get the current page URL"""
        if not self._tab:
            raise RuntimeError("Not connected")
        return await self._tab.current_url
    
    async def execute_script(self, script: str) -> Any:
        """Execute JavaScript and return result"""
        if not self._tab:
            raise RuntimeError("Not connected")
        return await self._tab.execute_script(script)
    
    async def find_element(self, by: str, value: str, timeout: int = 10):
        """Find an element on the page"""
        if not self._tab:
            raise RuntimeError("Not connected")
        
        by_map = {
            'css': By.CSS_SELECTOR,
            'xpath': By.XPATH,
            'id': By.ID,
            'class': By.CLASS_NAME,
            'name': By.NAME,
            'tag': By.TAG_NAME,
        }
        
        pydoll_by = by_map.get(by.lower(), By.CSS_SELECTOR)
        
        try:
            return await self._tab.find_or_wait_element(
                pydoll_by, value, timeout=timeout, raise_exc=False
            )
        except Exception as e:
            logger.debug(f"Element not found: {e}")
            return None
    
    async def click(self, by: str, value: str, timeout: int = 10) -> bool:
        """Find and click an element"""
        element = await self.find_element(by, value, timeout)
        if element:
            try:
                await element.click()
                if self.config.human_like_delays:
                    await asyncio.sleep(random.uniform(0.3, 0.8))
                return True
            except Exception as e:
                logger.error(f"Click failed: {e}")
        return False
    
    async def type_text(self, by: str, value: str, text: str, timeout: int = 10) -> bool:
        """Find element and type text with human-like delays"""
        element = await self.find_element(by, value, timeout)
        if element:
            try:
                await element.click()
                
                if self.config.human_like_delays:
                    for char in text:
                        await element.send_keys(char)
                        await asyncio.sleep(random.uniform(0.03, 0.12))
                else:
                    await element.send_keys(text)
                
                return True
            except Exception as e:
                logger.error(f"Type failed: {e}")
        return False
    
    async def screenshot(self, path: str) -> bool:
        """Take a screenshot and save to file"""
        if not self._tab:
            raise RuntimeError("Not connected")
        
        try:
            import base64
            result = await self._handler.execute_command({
                'method': 'Page.captureScreenshot',
                'params': {'format': 'png'}
            }, timeout=self.config.command_timeout)
            
            data = result.get('result', {}).get('data')
            if data:
                with open(path, 'wb') as f:
                    f.write(base64.b64decode(data))
                logger.info(f"Screenshot saved: {path}")
                return True
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
        return False
    
    async def scroll_down(self, pixels: int = 500):
        """Scroll the page down"""
        if self.config.human_like_delays:
            steps = random.randint(3, 7)
            per_step = pixels // steps
            for _ in range(steps):
                await self.execute_script(f"window.scrollBy(0, {per_step})")
                await asyncio.sleep(random.uniform(0.1, 0.3))
        else:
            await self.execute_script(f"window.scrollBy(0, {pixels})")
    
    async def _get_captcha_screenshot(self) -> Optional[bytes]:
        """Take a screenshot of the current page for CAPTCHA analysis"""
        try:
            import base64
            result = await self._handler.execute_command({
                'method': 'Page.captureScreenshot',
                'params': {'format': 'png'}
            }, timeout=self.config.command_timeout)
            
            data = result.get('result', {}).get('data')
            if data:
                return base64.b64decode(data)
        except Exception as e:
            logger.error(f"CAPTCHA screenshot failed: {e}")
        return None
    
    async def _init_vlm_solver(self):
        """Initialize VLM solver if enabled"""
        if self._vlm_solver is None and self.config.vlm_enabled:
            from ..utils.vlm_solver import VLMSolver, VLMConfig
            vlm_config = VLMConfig(
                ollama_host=self.config.ollama_host,
                model=self.config.ollama_model,
            )
            self._vlm_solver = VLMSolver(vlm_config)
        return self._vlm_solver
    
    async def detect_captcha(self) -> Optional[str]:
        """
        Detect if there's a CAPTCHA on the current page.
        
        Returns:
            CAPTCHA type string or None if no CAPTCHA detected
        """
        source = await self.get_page_source()
        
        captcha_indicators = {
            'recaptcha': ['g-recaptcha', 'recaptcha', 'rc-imageselect'],
            'hcaptcha': ['h-captcha', 'hcaptcha'],
            'cloudflare': ['cf-turnstile', 'challenge-running'],
            'slider': ['slider-captcha', 'slide-verify', 'geetest'],
            'text': ['captcha-image', 'captcha-input'],
        }
        
        for captcha_type, indicators in captcha_indicators.items():
            if any(ind.lower() in source.lower() for ind in indicators):
                logger.info(f"Detected CAPTCHA type: {captcha_type}")
                return captcha_type
        
        return None
    
    async def solve_captcha(self, hint: str = "") -> bool:
        """
        Attempt to solve any CAPTCHA on the current page using VLM.
        
        Args:
            hint: Optional hint about what to look for (e.g., "traffic lights")
        
        Returns:
            True if CAPTCHA was solved successfully
        """
        if not self.config.vlm_enabled:
            logger.warning("VLM solver not enabled. Set vlm_enabled=True in config.")
            return False
        
        solver = await self._init_vlm_solver()
        if not solver:
            logger.error("Failed to initialize VLM solver")
            return False
        
        # Detect CAPTCHA type
        captcha_type = await self.detect_captcha()
        if not captcha_type:
            logger.info("No CAPTCHA detected on page")
            return True  # No CAPTCHA = success
        
        logger.info(f"Attempting to solve {captcha_type} CAPTCHA with VLM...")
        
        # Take screenshot for analysis
        screenshot_bytes = await self._get_captcha_screenshot()
        if not screenshot_bytes:
            logger.error("Failed to capture CAPTCHA screenshot")
            return False
        
        # Convert to base64
        import base64
        image_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
        
        # Solve with VLM
        from ..utils.vlm_solver import CaptchaType
        solution = await solver.solve(image_b64, hint)
        
        if not solution.success:
            logger.error(f"VLM failed to solve CAPTCHA: {solution.raw_response}")
            return False
        
        logger.info(f"VLM solution: {solution.solution}")
        
        # Apply solution based on type
        try:
            if solution.captcha_type == CaptchaType.RECAPTCHA_IMAGE:
                # Click on identified cells
                cells = solution.solution
                if cells:
                    # This requires knowing the grid element positions
                    # For now, log the solution
                    logger.info(f"Image selection: click cells {cells}")
                    # TODO: Implement cell clicking based on grid layout
                    
            elif solution.captcha_type == CaptchaType.TEXT_DISTORTED:
                # Type the text into the input field
                text = solution.solution
                await self.type_text('css', 'input[name*="captcha"], input.captcha-input', text)
                
            elif solution.captcha_type == CaptchaType.MATH:
                # Type the answer
                answer = solution.solution
                await self.type_text('css', 'input[name*="captcha"], input.captcha-input', answer)
                
            elif solution.captcha_type == CaptchaType.SLIDER:
                # Slider requires drag action
                position = solution.solution
                logger.info(f"Slider position: drag to x={position.get('x', 0)}")
                # TODO: Implement drag action
            
            # Wait and check if CAPTCHA is gone
            await asyncio.sleep(2)
            new_captcha = await self.detect_captcha()
            
            if not new_captcha:
                logger.info("CAPTCHA solved successfully!")
                return True
            else:
                logger.warning(f"CAPTCHA still present: {new_captcha}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to apply CAPTCHA solution: {e}")
            return False
    
    async def close(self):
        """Close the browser connection"""
        if self._vlm_solver:
            await self._vlm_solver.close()
            self._vlm_solver = None
        self._browser = None
        self._tab = None
        self._handler = None
        logger.info("Disconnected from Docker Chrome")
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Convenience function
async def scrape(url: str, config: Optional[FusionConfig] = None) -> Optional[str]:
    """Quick scrape a URL using Docker + Pydoll fusion"""
    async with DockerPydollFusion(config) as browser:
        if await browser.navigate(url):
            await browser.wait_for_cloudflare()
            return await browser.get_page_source()
    return None
