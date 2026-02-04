"""
VLM-based CAPTCHA Solver
========================

Uses Vision Language Models (Ollama) to solve various CAPTCHA types.

Supported CAPTCHAs:
- reCAPTCHA v2 (image selection)
- Text-based CAPTCHAs
- Slider CAPTCHAs (position detection)
- Math/Logic CAPTCHAs
"""

import base64
import json
import logging
import re
import httpx
from typing import Optional, List, Tuple, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class CaptchaType(Enum):
    """Types of CAPTCHAs that can be solved"""
    RECAPTCHA_IMAGE = "recaptcha_image"  # Select all images with X
    RECAPTCHA_TEXT = "recaptcha_text"    # Type the text you see
    SLIDER = "slider"                     # Drag slider to position
    TEXT_DISTORTED = "text_distorted"     # Distorted text recognition
    MATH = "math"                         # Math problems
    OBJECT_CLICK = "object_click"         # Click on specific object
    UNKNOWN = "unknown"


@dataclass
class VLMConfig:
    """Configuration for VLM solver"""
    
    ollama_host: str = "http://localhost:11434"
    model: str = "minicpm-v:8b"  # Vision model
    timeout: int = 60
    max_retries: int = 3


@dataclass
class CaptchaSolution:
    """Result from CAPTCHA solving attempt"""
    
    success: bool
    captcha_type: CaptchaType
    solution: Any  # Could be text, coordinates, etc.
    confidence: float = 0.0
    raw_response: str = ""


class VLMSolver:
    """
    Vision Language Model based CAPTCHA solver.
    
    Uses Ollama with vision models (minicpm-v, llava, etc.)
    to analyze and solve various CAPTCHA types.
    """
    
    def __init__(self, config: Optional[VLMConfig] = None):
        self.config = config or VLMConfig()
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
    
    async def _call_ollama(self, prompt: str, image_base64: str) -> str:
        """Call Ollama API with image"""
        
        url = f"{self.config.ollama_host}/api/generate"
        
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for precise answers
            }
        }
        
        try:
            response = await self._client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    async def detect_captcha_type(self, image_base64: str) -> CaptchaType:
        """Detect what type of CAPTCHA is shown in the image"""
        
        prompt = """Analyze this image and determine what type of CAPTCHA it is.
        
Respond with ONLY one of these types:
- RECAPTCHA_IMAGE (if it shows a grid of images asking to select something)
- SLIDER (if it shows a slider puzzle to drag)
- TEXT_DISTORTED (if it shows distorted text to type)
- MATH (if it shows a math problem)
- OBJECT_CLICK (if it asks to click on a specific object)
- UNKNOWN (if you can't determine)

Just respond with the type name, nothing else."""

        response = await self._call_ollama(prompt, image_base64)
        response = response.strip().upper()
        
        type_map = {
            "RECAPTCHA_IMAGE": CaptchaType.RECAPTCHA_IMAGE,
            "SLIDER": CaptchaType.SLIDER,
            "TEXT_DISTORTED": CaptchaType.TEXT_DISTORTED,
            "MATH": CaptchaType.MATH,
            "OBJECT_CLICK": CaptchaType.OBJECT_CLICK,
        }
        
        return type_map.get(response, CaptchaType.UNKNOWN)
    
    async def solve_image_selection(
        self, 
        image_base64: str, 
        target: str,
        grid_size: Tuple[int, int] = (3, 3)
    ) -> List[int]:
        """
        Solve reCAPTCHA image selection.
        
        Args:
            image_base64: Base64 encoded image of the CAPTCHA grid
            target: What to select (e.g., "traffic lights", "crosswalks")
            grid_size: Grid dimensions (rows, cols)
        
        Returns:
            List of cell indices (0-8 for 3x3 grid) that match the target
        """
        
        rows, cols = grid_size
        total_cells = rows * cols
        
        prompt = f"""This is a CAPTCHA image grid with {rows}x{cols}={total_cells} cells.
The cells are numbered 0-{total_cells-1}, left to right, top to bottom:
[0][1][2]
[3][4][5]
[6][7][8]

Task: Select ALL cells that contain "{target}".

Respond with ONLY a JSON array of cell numbers that contain {target}.
Example: [0, 2, 5] or [] if none match.

Important: Look carefully at each cell. Only include cells that clearly show {target}."""

        response = await self._call_ollama(prompt, image_base64)
        
        # Parse JSON array from response
        try:
            # Find JSON array in response
            match = re.search(r'\[[\d,\s]*\]', response)
            if match:
                cells = json.loads(match.group())
                # Validate cell numbers
                cells = [c for c in cells if 0 <= c < total_cells]
                logger.info(f"Image selection solution: cells {cells} for '{target}'")
                return cells
        except json.JSONDecodeError:
            pass
        
        logger.warning(f"Could not parse image selection response: {response}")
        return []
    
    async def solve_text_captcha(self, image_base64: str) -> str:
        """
        Solve text-based CAPTCHA (distorted text recognition).
        
        Returns:
            The text shown in the CAPTCHA
        """
        
        prompt = """This image shows a CAPTCHA with distorted text.

Your task: Read and type out EXACTLY what text is shown.

Rules:
- Only output the text characters you see
- Ignore background noise/lines
- Be case-sensitive
- No extra explanation, just the text

Text:"""

        response = await self._call_ollama(prompt, image_base64)
        
        # Clean up response - extract just alphanumeric
        text = re.sub(r'[^a-zA-Z0-9]', '', response.strip())
        logger.info(f"Text CAPTCHA solution: {text}")
        return text
    
    async def solve_math_captcha(self, image_base64: str) -> str:
        """
        Solve math-based CAPTCHA.
        
        Returns:
            The answer to the math problem
        """
        
        prompt = """This image shows a math problem CAPTCHA.

Read the math problem and calculate the answer.

Respond with ONLY the numerical answer, nothing else.

Answer:"""

        response = await self._call_ollama(prompt, image_base64)
        
        # Extract number from response
        match = re.search(r'-?\d+', response)
        if match:
            answer = match.group()
            logger.info(f"Math CAPTCHA solution: {answer}")
            return answer
        
        return response.strip()
    
    async def solve_slider_position(self, image_base64: str) -> Dict[str, int]:
        """
        Detect slider puzzle position.
        
        Returns:
            Dict with 'x' and 'y' coordinates for slider destination
        """
        
        prompt = """This image shows a slider CAPTCHA puzzle.

There is a puzzle piece that needs to be dragged to complete an image.
Identify the X position (in pixels from left) where the piece should go.

Estimate the image width as 300 pixels.
Respond with ONLY a JSON object: {"x": <number>}

Position:"""

        response = await self._call_ollama(prompt, image_base64)
        
        try:
            match = re.search(r'\{[^}]+\}', response)
            if match:
                position = json.loads(match.group())
                logger.info(f"Slider position: {position}")
                return position
        except json.JSONDecodeError:
            pass
        
        return {"x": 150}  # Default to middle
    
    async def solve(self, image_base64: str, hint: str = "") -> CaptchaSolution:
        """
        Auto-detect and solve any CAPTCHA type.
        
        Args:
            image_base64: Base64 encoded CAPTCHA image
            hint: Optional hint about what to select/solve
        
        Returns:
            CaptchaSolution with results
        """
        
        try:
            # Detect type
            captcha_type = await self.detect_captcha_type(image_base64)
            logger.info(f"Detected CAPTCHA type: {captcha_type}")
            
            solution = None
            
            if captcha_type == CaptchaType.RECAPTCHA_IMAGE:
                # Extract target from hint or detect
                target = hint or "the requested objects"
                solution = await self.solve_image_selection(image_base64, target)
                
            elif captcha_type == CaptchaType.TEXT_DISTORTED:
                solution = await self.solve_text_captcha(image_base64)
                
            elif captcha_type == CaptchaType.MATH:
                solution = await self.solve_math_captcha(image_base64)
                
            elif captcha_type == CaptchaType.SLIDER:
                solution = await self.solve_slider_position(image_base64)
                
            else:
                # Try generic approach
                prompt = f"""Analyze this CAPTCHA and solve it.
{f'Hint: {hint}' if hint else ''}

Provide the solution in the most appropriate format."""
                
                response = await self._call_ollama(prompt, image_base64)
                solution = response.strip()
            
            return CaptchaSolution(
                success=solution is not None,
                captcha_type=captcha_type,
                solution=solution,
                confidence=0.8 if solution else 0.0
            )
            
        except Exception as e:
            logger.error(f"CAPTCHA solving failed: {e}")
            return CaptchaSolution(
                success=False,
                captcha_type=CaptchaType.UNKNOWN,
                solution=None,
                confidence=0.0,
                raw_response=str(e)
            )
    
    async def close(self):
        """Close HTTP client"""
        await self._client.aclose()


def image_to_base64(image_path: str) -> str:
    """Convert image file to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def bytes_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string"""
    return base64.b64encode(image_bytes).decode("utf-8")
