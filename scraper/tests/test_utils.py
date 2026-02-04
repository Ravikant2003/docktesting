#!/usr/bin/env python3
"""
Test Suite for the Scraper Package
===================================

Run with: python -m pytest scraper/tests/ -v
"""

import asyncio
import pytest
import sys
sys.path.insert(0, '../..')


class TestCaptchaDetector:
    """Tests for CaptchaDetector"""
    
    def test_detect_cloudflare_turnstile(self):
        from scraper.utils.captcha import CaptchaDetector, CaptchaType
        
        detector = CaptchaDetector()
        html = '<div class="cf-turnstile" data-sitekey="0x123"></div>'
        
        result = detector.detect(html)
        
        assert result.type == CaptchaType.CLOUDFLARE_TURNSTILE
        assert result.confidence >= 0.7
        assert result.sitekey == "0x123"
    
    def test_detect_recaptcha(self):
        from scraper.utils.captcha import CaptchaDetector, CaptchaType
        
        detector = CaptchaDetector()
        html = '<div class="g-recaptcha" data-sitekey="abc123"></div>'
        
        result = detector.detect(html)
        
        assert result.type == CaptchaType.RECAPTCHA_V2
        assert result.sitekey == "abc123"
    
    def test_detect_hcaptcha(self):
        from scraper.utils.captcha import CaptchaDetector, CaptchaType
        
        detector = CaptchaDetector()
        html = '<div class="h-captcha" data-sitekey="xyz789"></div>'
        
        result = detector.detect(html)
        
        assert result.type == CaptchaType.HCAPTCHA
    
    def test_detect_no_captcha(self):
        from scraper.utils.captcha import CaptchaDetector, CaptchaType
        
        detector = CaptchaDetector()
        html = '<html><body><h1>Hello World</h1></body></html>'
        
        result = detector.detect(html)
        
        assert result.type == CaptchaType.NONE
    
    def test_is_cloudflare_challenge(self):
        from scraper.utils.captcha import CaptchaDetector
        
        detector = CaptchaDetector()
        
        assert detector.is_cloudflare_challenge("cf-turnstile") == True
        assert detector.is_cloudflare_challenge("Just a moment") == True
        assert detector.is_cloudflare_challenge("Hello World") == False


class TestProxyManager:
    """Tests for ProxyManager"""
    
    def test_add_proxy(self):
        from scraper.utils.proxy import ProxyManager
        
        manager = ProxyManager()
        manager.add_proxy("http://user:pass@proxy.example.com:8080")
        
        assert manager.count == 1
    
    def test_add_multiple_proxies(self):
        from scraper.utils.proxy import ProxyManager
        
        manager = ProxyManager()
        manager.add_proxies([
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
            "http://proxy3.example.com:8080",
        ])
        
        assert manager.count == 3
    
    def test_get_next_rotation(self):
        from scraper.utils.proxy import ProxyManager
        
        manager = ProxyManager()
        manager.add_proxies([
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
        ])
        
        proxy1 = manager.get_next()
        proxy2 = manager.get_next()
        proxy3 = manager.get_next()
        
        # Should rotate
        assert proxy1 != proxy2 or manager.count == 1
    
    def test_report_success(self):
        from scraper.utils.proxy import ProxyManager
        
        manager = ProxyManager()
        manager.add_proxy("http://proxy.example.com:8080")
        
        proxy = manager.get_next()
        manager.report_success(proxy, response_time=0.5)
        
        stats = manager.get_stats()
        assert stats["proxies"][0]["success_rate"] == 1.0
    
    def test_report_failure(self):
        from scraper.utils.proxy import ProxyManager
        
        manager = ProxyManager()
        manager.add_proxy("http://proxy.example.com:8080")
        
        proxy = manager.get_next()
        for _ in range(5):
            manager.report_failure(proxy)
        
        assert manager.healthy_count == 0


class TestStealth:
    """Tests for stealth configuration"""
    
    def test_stealth_config_defaults(self):
        from scraper.utils.stealth import StealthConfig
        
        config = StealthConfig()
        
        assert "Chrome" in config.user_agent
        assert config.platform == "macOS"
        assert "en-US" in config.languages
    
    def test_get_random_user_agent(self):
        from scraper.utils.stealth import get_random_user_agent, USER_AGENTS
        
        ua = get_random_user_agent()
        
        assert ua in USER_AGENTS
        assert "Chrome" in ua


class TestProxyConfig:
    """Tests for ProxyConfig"""
    
    def test_from_url_basic(self):
        from scraper.utils.proxy import ProxyConfig
        
        config = ProxyConfig.from_url("http://proxy.example.com:8080")
        
        assert config.host == "proxy.example.com"
        assert config.port == 8080
    
    def test_from_url_with_auth(self):
        from scraper.utils.proxy import ProxyConfig
        
        config = ProxyConfig.from_url("http://user:pass@proxy.example.com:8080")
        
        assert config.host == "proxy.example.com"
        assert config.port == 8080
        assert config.username == "user"
        assert config.password == "pass"
    
    def test_to_url(self):
        from scraper.utils.proxy import ProxyConfig, ProxyType
        
        config = ProxyConfig(
            host="proxy.example.com",
            port=8080,
            username="user",
            password="pass",
            proxy_type=ProxyType.HTTP
        )
        
        assert config.url == "http://user:pass@proxy.example.com:8080"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
