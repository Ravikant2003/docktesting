"""
CAPTCHA Detection Module
========================

Detects various CAPTCHA types in web pages.
"""

import logging
from enum import Enum, auto
from typing import List, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class CaptchaType(Enum):
    """Types of CAPTCHAs that can be detected"""
    NONE = auto()
    CLOUDFLARE_TURNSTILE = auto()
    RECAPTCHA_V2 = auto()
    RECAPTCHA_V3 = auto()
    HCAPTCHA = auto()
    FUNCAPTCHA = auto()
    IMAGE_CAPTCHA = auto()
    TEXT_CAPTCHA = auto()
    UNKNOWN = auto()


@dataclass
class CaptchaInfo:
    """Information about a detected CAPTCHA"""
    type: CaptchaType
    confidence: float  # 0.0 to 1.0
    sitekey: Optional[str] = None
    action: Optional[str] = None
    element_selector: Optional[str] = None


class CaptchaDetector:
    """
    Detects CAPTCHAs in web page content.
    
    Usage:
        detector = CaptchaDetector()
        result = detector.detect(html_content)
        if result.type != CaptchaType.NONE:
            print(f"Found {result.type.name}")
    """
    
    # Detection patterns for each CAPTCHA type
    PATTERNS = {
        CaptchaType.CLOUDFLARE_TURNSTILE: [
            ('cf-turnstile', 0.9),
            ('challenges.cloudflare.com/turnstile', 0.9),
            ('turnstile.min.js', 0.8),
            ('cf-chl-widget', 0.7),
        ],
        CaptchaType.RECAPTCHA_V2: [
            ('g-recaptcha', 0.9),
            ('recaptcha/api.js', 0.9),
            ('grecaptcha.render', 0.8),
            ('data-sitekey', 0.6),  # Lower confidence as it's shared
        ],
        CaptchaType.RECAPTCHA_V3: [
            ('recaptcha/api.js?render=', 0.9),
            ('grecaptcha.execute', 0.9),
            ('recaptcha-v3', 0.8),
        ],
        CaptchaType.HCAPTCHA: [
            ('h-captcha', 0.9),
            ('hcaptcha.com/1/api.js', 0.9),
            ('data-hcaptcha', 0.8),
        ],
        CaptchaType.FUNCAPTCHA: [
            ('funcaptcha', 0.9),
            ('arkoselabs.com', 0.9),
            ('fc-token', 0.7),
        ],
    }
    
    def __init__(self):
        self._cache: Dict[str, CaptchaInfo] = {}
    
    def detect(self, html: str) -> CaptchaInfo:
        """
        Detect CAPTCHA type in HTML content.
        
        Args:
            html: Page HTML content
            
        Returns:
            CaptchaInfo with detected type and confidence
        """
        if not html:
            return CaptchaInfo(type=CaptchaType.NONE, confidence=1.0)
        
        html_lower = html.lower()
        
        best_match = CaptchaInfo(type=CaptchaType.NONE, confidence=0.0)
        
        for captcha_type, patterns in self.PATTERNS.items():
            for pattern, confidence in patterns:
                if pattern.lower() in html_lower:
                    if confidence > best_match.confidence:
                        best_match = CaptchaInfo(
                            type=captcha_type,
                            confidence=confidence,
                            sitekey=self._extract_sitekey(html, captcha_type),
                        )
        
        # If no specific CAPTCHA found, check for generic indicators
        if best_match.type == CaptchaType.NONE:
            generic_patterns = ['captcha', 'verify you are human', 'robot check']
            for pattern in generic_patterns:
                if pattern in html_lower:
                    best_match = CaptchaInfo(
                        type=CaptchaType.UNKNOWN,
                        confidence=0.5,
                    )
                    break
        
        if best_match.type != CaptchaType.NONE:
            logger.info(f"Detected {best_match.type.name} (confidence: {best_match.confidence})")
        
        return best_match
    
    def _extract_sitekey(self, html: str, captcha_type: CaptchaType) -> Optional[str]:
        """Extract the sitekey from HTML if present"""
        import re
        
        patterns = {
            CaptchaType.CLOUDFLARE_TURNSTILE: r'data-sitekey=["\']([^"\']+)["\']',
            CaptchaType.RECAPTCHA_V2: r'data-sitekey=["\']([^"\']+)["\']',
            CaptchaType.RECAPTCHA_V3: r'grecaptcha\.execute\(["\']([^"\']+)["\']',
            CaptchaType.HCAPTCHA: r'data-sitekey=["\']([^"\']+)["\']',
        }
        
        pattern = patterns.get(captcha_type)
        if pattern:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        
        return None
    
    def detect_multiple(self, html: str) -> List[CaptchaInfo]:
        """
        Detect all CAPTCHAs in HTML content (for pages with multiple).
        
        Args:
            html: Page HTML content
            
        Returns:
            List of all detected CAPTCHAs
        """
        if not html:
            return []
        
        html_lower = html.lower()
        detected = []
        
        for captcha_type, patterns in self.PATTERNS.items():
            for pattern, confidence in patterns:
                if pattern.lower() in html_lower:
                    info = CaptchaInfo(
                        type=captcha_type,
                        confidence=confidence,
                        sitekey=self._extract_sitekey(html, captcha_type),
                    )
                    # Avoid duplicates
                    if not any(d.type == info.type for d in detected):
                        detected.append(info)
                    break
        
        return detected
    
    def is_cloudflare_challenge(self, html: str) -> bool:
        """Quick check if page has Cloudflare challenge"""
        indicators = [
            'cf-turnstile',
            'challenge-running',
            'Just a moment',
            'Checking your browser',
            'cf-chl-',
        ]
        return any(ind in html for ind in indicators)
