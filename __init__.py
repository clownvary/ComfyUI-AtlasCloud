"""
ComfyUI OneApi - Universal image generation API nodes

Provides two nodes for text-to-image and image-to-image generation
compatible with OpenAI gpt-image-2 and OpenAI-compatible APIs.
"""

from .nodes import (
    OneApiText2Img,
    OneApiImg2Img,
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS,
)

__all__ = [
    "OneApiText2Img",
    "OneApiImg2Img",
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]

# Web directory (optional, for custom UI)
WEB_DIRECTORY = None
