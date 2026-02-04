"""
Proxy Manager
=============

Manages proxy rotation and health checking.
"""

import logging
import random
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ProxyType(Enum):
    """Proxy protocol types"""
    HTTP = "http"
    HTTPS = "https"
    SOCKS5 = "socks5"


@dataclass
class ProxyConfig:
    """Single proxy configuration"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    proxy_type: ProxyType = ProxyType.HTTP
    
    @property
    def url(self) -> str:
        """Get proxy URL string"""
        auth = ""
        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"
        return f"{self.proxy_type.value}://{auth}{self.host}:{self.port}"
    
    @classmethod
    def from_url(cls, url: str) -> "ProxyConfig":
        """Parse proxy from URL string"""
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        return cls(
            host=parsed.hostname or "",
            port=parsed.port or 80,
            username=parsed.username,
            password=parsed.password,
            proxy_type=ProxyType(parsed.scheme) if parsed.scheme else ProxyType.HTTP,
        )


@dataclass
class ProxyHealth:
    """Health status of a proxy"""
    proxy: ProxyConfig
    is_healthy: bool = True
    success_count: int = 0
    failure_count: int = 0
    avg_response_time: float = 0.0
    last_used: Optional[float] = None
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0


class ProxyManager:
    """
    Manages a pool of proxies with rotation and health tracking.
    
    Usage:
        manager = ProxyManager()
        manager.add_proxy("http://user:pass@proxy.example.com:8080")
        
        proxy = manager.get_next()
        # Use proxy...
        manager.report_success(proxy)
    """
    
    def __init__(self):
        self._proxies: Dict[str, ProxyHealth] = {}
        self._rotation_index = 0
    
    def add_proxy(self, proxy: str | ProxyConfig) -> None:
        """Add a proxy to the pool"""
        if isinstance(proxy, str):
            proxy = ProxyConfig.from_url(proxy)
        
        key = proxy.url
        if key not in self._proxies:
            self._proxies[key] = ProxyHealth(proxy=proxy)
            logger.debug(f"Added proxy: {proxy.host}:{proxy.port}")
    
    def add_proxies(self, proxies: List[str]) -> None:
        """Add multiple proxies"""
        for proxy in proxies:
            self.add_proxy(proxy)
    
    def get_next(self, healthy_only: bool = True) -> Optional[ProxyConfig]:
        """
        Get next proxy using round-robin rotation.
        
        Args:
            healthy_only: Only return healthy proxies
            
        Returns:
            Next proxy or None if no proxies available
        """
        if not self._proxies:
            return None
        
        proxies = list(self._proxies.values())
        
        if healthy_only:
            proxies = [p for p in proxies if p.is_healthy]
        
        if not proxies:
            # Fall back to unhealthy proxies if no healthy ones
            proxies = list(self._proxies.values())
        
        if not proxies:
            return None
        
        self._rotation_index = (self._rotation_index + 1) % len(proxies)
        selected = proxies[self._rotation_index]
        
        import time
        selected.last_used = time.time()
        
        return selected.proxy
    
    def get_random(self, healthy_only: bool = True) -> Optional[ProxyConfig]:
        """Get a random proxy from the pool"""
        if not self._proxies:
            return None
        
        proxies = list(self._proxies.values())
        
        if healthy_only:
            proxies = [p for p in proxies if p.is_healthy]
        
        if not proxies:
            proxies = list(self._proxies.values())
        
        if not proxies:
            return None
        
        selected = random.choice(proxies)
        
        import time
        selected.last_used = time.time()
        
        return selected.proxy
    
    def get_best(self) -> Optional[ProxyConfig]:
        """Get the best performing proxy based on success rate"""
        if not self._proxies:
            return None
        
        healthy = [p for p in self._proxies.values() if p.is_healthy]
        if not healthy:
            return None
        
        best = max(healthy, key=lambda p: (p.success_rate, -p.avg_response_time))
        return best.proxy
    
    def report_success(self, proxy: ProxyConfig, response_time: float = 0.0) -> None:
        """Report a successful request through a proxy"""
        key = proxy.url
        if key in self._proxies:
            health = self._proxies[key]
            health.success_count += 1
            health.is_healthy = True
            
            # Update average response time
            total = health.success_count + health.failure_count
            health.avg_response_time = (
                (health.avg_response_time * (total - 1) + response_time) / total
            )
    
    def report_failure(self, proxy: ProxyConfig) -> None:
        """Report a failed request through a proxy"""
        key = proxy.url
        if key in self._proxies:
            health = self._proxies[key]
            health.failure_count += 1
            
            # Mark as unhealthy after 3 consecutive failures
            if health.failure_count >= 3 and health.success_rate < 0.5:
                health.is_healthy = False
                logger.warning(f"Proxy marked unhealthy: {proxy.host}:{proxy.port}")
    
    def remove_proxy(self, proxy: ProxyConfig) -> None:
        """Remove a proxy from the pool"""
        key = proxy.url
        if key in self._proxies:
            del self._proxies[key]
            logger.debug(f"Removed proxy: {proxy.host}:{proxy.port}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the proxy pool"""
        total = len(self._proxies)
        healthy = sum(1 for p in self._proxies.values() if p.is_healthy)
        
        return {
            "total": total,
            "healthy": healthy,
            "unhealthy": total - healthy,
            "proxies": [
                {
                    "host": h.proxy.host,
                    "port": h.proxy.port,
                    "healthy": h.is_healthy,
                    "success_rate": h.success_rate,
                    "avg_response_time": h.avg_response_time,
                }
                for h in self._proxies.values()
            ]
        }
    
    def clear(self) -> None:
        """Clear all proxies"""
        self._proxies.clear()
        self._rotation_index = 0
    
    @property
    def count(self) -> int:
        """Number of proxies in the pool"""
        return len(self._proxies)
    
    @property
    def healthy_count(self) -> int:
        """Number of healthy proxies"""
        return sum(1 for p in self._proxies.values() if p.is_healthy)
