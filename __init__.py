"""
ComfyUI AtlasCloud - atlascloud.ai image generation API nodes
"""

from .nodes import (
    AtlasCloudText2Img,
    AtlasCloudImg2Img,
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS,
)

__all__ = [
    "AtlasCloudText2Img",
    "AtlasCloudImg2Img",
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]

# Web directory (optional, for custom UI)
WEB_DIRECTORY = None
