"""
CDP Client - Direct Chrome DevTools Protocol Client
====================================================

Low-level CDP client for direct communication with Chrome.
Use DockerPydollFusion for most use cases.
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class CDPConfig:
    """CDP connection configuration"""
    host: str = "localhost"
    port: int = 3000
    timeout: int = 30


class CDPClient:
    """
    Direct Chrome DevTools Protocol client.
    
    For low-level CDP access when you need fine-grained control.
    For most use cases, prefer DockerPydollFusion.
    
    Usage:
        async with CDPClient() as cdp:
            await cdp.navigate("https://example.com")
            html = await cdp.get_html()
    """
    
    def __init__(self, config: Optional[CDPConfig] = None):
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError("websockets not installed. Run: pip install websockets")
        
        self.config = config or CDPConfig()
        self._ws = None
        self._msg_id = 0
        self._session_id = None
    
    @property
    def ws_url(self) -> str:
        return f"ws://{self.config.host}:{self.config.port}"
    
    async def connect(self) -> bool:
        """Connect to Chrome via WebSocket"""
        try:
            self._ws = await websockets.connect(
                self.ws_url,
                max_size=16 * 1024 * 1024,
                ping_timeout=self.config.timeout
            )
            logger.info(f"Connected to Chrome at {self.ws_url}")
            
            # Enable required domains
            await self.send_command("Page.enable")
            await self.send_command("Network.enable")
            await self.send_command("Runtime.enable")
            
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    async def send_command(self, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Send a CDP command and wait for response"""
        if not self._ws:
            raise RuntimeError("Not connected")
        
        self._msg_id += 1
        message = {
            "id": self._msg_id,
            "method": method,
            "params": params or {}
        }
        
        if self._session_id:
            message["sessionId"] = self._session_id
        
        await self._ws.send(json.dumps(message))
        
        # Wait for response with matching ID
        while True:
            response = await asyncio.wait_for(
                self._ws.recv(),
                timeout=self.config.timeout
            )
            data = json.loads(response)
            
            if data.get("id") == self._msg_id:
                if "error" in data:
                    raise Exception(f"CDP Error: {data['error']}")
                return data.get("result", {})
    
    async def navigate(self, url: str) -> bool:
        """Navigate to a URL"""
        try:
            result = await self.send_command("Page.navigate", {"url": url})
            await asyncio.sleep(2)  # Wait for page load
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    async def get_html(self) -> str:
        """Get page HTML content"""
        result = await self.send_command(
            "Runtime.evaluate",
            {"expression": "document.documentElement.outerHTML", "returnByValue": True}
        )
        return result.get("result", {}).get("value", "")
    
    async def evaluate(self, expression: str) -> Any:
        """Evaluate JavaScript expression"""
        result = await self.send_command(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True}
        )
        return result.get("result", {}).get("value")
    
    async def screenshot(self, path: str) -> bool:
        """Take and save a screenshot"""
        try:
            import base64
            result = await self.send_command("Page.captureScreenshot", {"format": "png"})
            data = result.get("data")
            if data:
                with open(path, "wb") as f:
                    f.write(base64.b64decode(data))
                return True
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
        return False
    
    async def close(self):
        """Close the connection"""
        if self._ws:
            await self._ws.close()
            self._ws = None
        logger.info("CDP connection closed")
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
