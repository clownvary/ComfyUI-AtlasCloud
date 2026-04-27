"""ComfyUI AtlasCloud nodes for atlascloud.ai image generation API."""

import json
import torch
from .utils import base64_to_tensor
from .utils import make_api_request, make_edit_request
from .utils.image import tensor_batch_to_base64_list


# Official gpt-image-2 resolution presets
SIZE_OPTIONS = [
    # 1K
    "1024x768",
    "768x1024",
    "1024x1024",
    "1024x1536",
    "1536x1024",
    # 2K
    "1920x1080",
    "1080x1920",
    "2560x1440",
    "1440x2560",
    # 3K
    "3840x2160",
    "2160x3840",
]


class AtlasCloudText2Img:
    """
    Text-to-image generation node for atlascloud.ai API.

    Supports gpt-image-2 model with quality, size, and format options.
    """

    CATEGORY = "AtlasCloud"
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "info")
    FUNCTION = "generate"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_url": ("STRING", {
                    "default": "https://api.atlascloud.ai",
                    "multiline": False,
                    "tooltip": "Base URL for the AtlasCloud API endpoint",
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "AtlasCloud API key (required)",
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Text description of the image to generate",
                }),
            },
            "optional": {
                "model": ("STRING", {
                    "default": "openai/gpt-image-2/text-to-image",
                    "tooltip": "AI model to use for generation",
                }),
                "size": (SIZE_OPTIONS, {
                    "default": "1024x1024",
                    "tooltip": "Output image resolution (width x height)",
                }),
                "quality": (["low", "medium", "high"], {"default": "medium", "tooltip": "Image quality — higher quality takes longer to generate"}),
                "output_format": (["jpeg", "png"], {"default": "jpeg", "tooltip": "Output image file format"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random seed for reproducibility (-1 = random)"}),
                "extra_params": ("STRING", {"default": "", "multiline": True, "tooltip": "Additional JSON parameters to merge into the API request body"}),
            },
        }

    def __init__(self):
        pass

    def generate(
        self,
        base_url: str,
        api_key: str,
        prompt: str,
        model: str = "openai/gpt-image-2/text-to-image",
        size: str = "1024x1024",
        quality: str = "medium",
        output_format: str = "jpeg",
        seed: int = -1,
        extra_params: str = "",
    ):
        """Generate images from text prompt."""
        if not api_key.strip():
            raise Exception("API Key cannot be empty. Please enter a valid API Key.")

        if not prompt.strip():
            raise Exception("Prompt cannot be empty. Please enter a prompt.")

        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "enable_base64_output": True,
            "enable_sync_mode": False,
        }

        if seed >= 0:
            payload["seed"] = seed

        if extra_params.strip():
            try:
                extra = json.loads(extra_params)
                if isinstance(extra, dict):
                    payload.update(extra)
            except json.JSONDecodeError:
                raise Exception("extra_params has invalid format. Please provide valid JSON.")

        response = make_api_request(base_url, api_key, payload)

        if "data" not in response:
            raise Exception(f"Unexpected API response format: {response}")

        images = []
        for item in response["data"]:
            if "b64_json" in item:
                img_tensor = base64_to_tensor(item["b64_json"])
                images.append(img_tensor)

        if not images:
            raise Exception("API returned no image data.")

        result = torch.cat(images, dim=0)

        info_data = {
            "model": model,
            "size": size,
            "quality": quality,
            "output_format": output_format,
        }
        if seed >= 0:
            info_data["seed"] = seed

        info_str = json.dumps(info_data, ensure_ascii=False, indent=2)

        return (result, info_str)


class AtlasCloudImg2Img:
    """
    Image-to-image editing node for atlascloud.ai API.

    Takes up to 3 reference images and transforms them based on text prompt.
    Use input_fidelity to control detail preservation from the input images.
    High = preserve faces/logos, Low = more creative freedom.
    """

    CATEGORY = "AtlasCloud"
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "info")
    FUNCTION = "generate"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_url": ("STRING", {
                    "default": "https://api.atlascloud.ai",
                    "multiline": False,
                    "tooltip": "Base URL for the AtlasCloud API endpoint",
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "AtlasCloud API key (required)",
                }),
                "image_1": ("IMAGE", {
                    "tooltip": "Primary reference image (required)",
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Text description of how to edit the reference image(s)",
                }),
            },
            "optional": {
                "image_2": ("IMAGE", {
                    "tooltip": "Secondary reference image (optional)",
                }),
                "image_3": ("IMAGE", {
                    "tooltip": "Tertiary reference image (optional)",
                }),
                "model": ("STRING", {
                    "default": "openai/gpt-image-2/edit",
                    "tooltip": "AI model to use for image editing",
                }),
                "size": (SIZE_OPTIONS, {
                    "default": "1024x1024",
                    "tooltip": "Output image resolution (width x height)",
                }),
                "quality": (["low", "medium", "high"], {"default": "medium", "tooltip": "Image quality — higher quality takes longer to generate"}),
                "output_format": (["jpeg", "png"], {"default": "jpeg", "tooltip": "Output image file format"}),
                "input_fidelity": (["high", "low"], {"default": "high", "tooltip": "Detail preservation: high keeps faces/logos intact, low allows more creative freedom"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random seed for reproducibility (-1 = random)"}),
                "extra_params": ("STRING", {"default": "", "multiline": True, "tooltip": "Additional JSON parameters to merge into the API request body"}),
            },
        }

    def __init__(self):
        pass

    def generate(
        self,
        base_url: str,
        api_key: str,
        image_1: torch.Tensor,
        prompt: str,
        image_2: torch.Tensor = None,
        image_3: torch.Tensor = None,
        model: str = "openai/gpt-image-2/edit",
        size: str = "1024x1024",
        quality: str = "medium",
        output_format: str = "jpeg",
        input_fidelity: str = "high",
        seed: int = -1,
        extra_params: str = "",
    ):
        """Edit images with text prompt."""
        if not api_key.strip():
            raise Exception("API Key cannot be empty. Please enter a valid API Key.")

        if not prompt.strip():
            raise Exception("Prompt cannot be empty. Please enter a prompt.")

        images_list = [image_1, image_2, image_3]
        valid_images = [img for img in images_list if img is not None and img.numel() > 0]

        if not valid_images:
            raise Exception("At least one reference image is required.")

        format_upper = output_format.upper() if output_format != "jpeg" else "JPEG"
        images_uri = []
        for img in valid_images:
            b64_list = tensor_batch_to_base64_list(img, format=format_upper)
            for b64 in b64_list:
                images_uri.append(f"data:image/{output_format};base64,{b64}")

        if not images_uri:
            raise Exception("Failed to convert reference image.")

        payload = {
            "model": model,
            "prompt": prompt,
            "images": images_uri,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "input_fidelity": input_fidelity,
            "enable_base64_output": True,
            "enable_sync_mode": False,
        }

        if seed >= 0:
            payload["seed"] = seed

        if extra_params.strip():
            try:
                extra = json.loads(extra_params)
                if isinstance(extra, dict):
                    payload.update(extra)
            except json.JSONDecodeError:
                raise Exception("extra_params has invalid format. Please provide valid JSON.")

        response = make_edit_request(base_url, api_key, payload)

        if "data" not in response:
            raise Exception(f"Unexpected API response format: {response}")

        result_images = []
        for item in response["data"]:
            if "b64_json" in item:
                img_tensor = base64_to_tensor(item["b64_json"])
                result_images.append(img_tensor)

        if not result_images:
            raise Exception("API returned no image data.")

        result = torch.cat(result_images, dim=0)

        info_data = {
            "model": model,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "input_fidelity": input_fidelity,
            "input_images": len(images_uri),
        }
        if seed >= 0:
            info_data["seed"] = seed

        info_str = json.dumps(info_data, ensure_ascii=False, indent=2)

        return (result, info_str)


# Node class mappings for registration
NODE_CLASS_MAPPINGS = {
    "AtlasCloudText2Img": AtlasCloudText2Img,
    "AtlasCloudImg2Img": AtlasCloudImg2Img,
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "AtlasCloudText2Img": "AtlasCloud Text to Image",
    "AtlasCloudImg2Img": "AtlasCloud Image to Image",
}
