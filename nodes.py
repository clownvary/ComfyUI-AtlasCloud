"""ComfyUI OneApi nodes for universal image generation API."""

import json
import torch
from .utils import tensor_to_base64, base64_to_tensor
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


class OneApiText2Img:
    """
    Text-to-image generation node supporting OpenAI gpt-image-2 and compatible APIs.

    Supports all gpt-image-2 parameters including quality, background, moderation.
    """

    CATEGORY = "OneApi"
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "info")
    FUNCTION = "generate"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_url": ("STRING", {
                    "default": "https://api.openai.com/v1",
                    "multiline": False,
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
                "model": ("STRING", {
                    "default": "gpt-image-2",
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                }),
                "size": (SIZE_OPTIONS, {
                    "default": "1024x1024",
                }),
            },
            "optional": {
                "quality": (["standard", "hd"], {"default": "standard"}),
                "background": (["opaque", "transparent"], {"default": "opaque"}),
                "moderation": (["auto", "low"], {"default": "auto"}),
                "output_format": (["png", "jpeg"], {"default": "png"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
                "n": ("INT", {"default": 1, "min": 1, "max": 10}),
                "extra_params": ("STRING", {"default": "", "multiline": True}),
            },
        }

    def __init__(self):
        pass

    def generate(
        self,
        base_url: str,
        api_key: str,
        model: str,
        prompt: str,
        size: str,
        quality: str = "standard",
        background: str = "opaque",
        moderation: str = "auto",
        output_format: str = "png",
        seed: int = -1,
        n: int = 1,
        extra_params: str = "",
    ):
        """
        Generate images from text prompt.

        Args:
            base_url: API base URL
            api_key: API key for authentication
            model: Model name (gpt-image-2, dall-e-3, etc.)
            prompt: Text prompt
            size: Image size (resolution preset)
            quality: Image quality (standard/hd)
            background: Background type (opaque/transparent)
            moderation: Moderation level (auto/low)
            output_format: Output format (png/jpeg)
            seed: Random seed (-1 for random)
            n: Number of images to generate
            extra_params: Additional JSON parameters

        Returns:
            Tuple of (image tensor, info string)
        """
        if not api_key.strip():
            raise Exception("API Key 不能为空，请输入有效的 API Key")

        if not prompt.strip():
            raise Exception("Prompt 不能为空，请输入提示词")

        # Build payload
        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "background": background,
            "moderation": moderation,
            "output_format": output_format,
            "output": "b64_json",
            "n": n,
        }

        # Add seed if specified
        if seed >= 0:
            payload["seed"] = seed

        # Add extra params if provided
        if extra_params.strip():
            try:
                extra = json.loads(extra_params)
                if isinstance(extra, dict):
                    payload.update(extra)
            except json.JSONDecodeError:
                raise Exception("extra_params 格式错误，请提供有效的 JSON 格式")

        # Make API request
        try:
            response = make_api_request(base_url, api_key, payload)
        except Exception as e:
            raise e

        # Parse response
        if "data" not in response:
            raise Exception(f"API 响应格式错误：{response}")

        images = []
        for item in response["data"]:
            if "b64_json" in item:
                img_tensor = base64_to_tensor(item["b64_json"])
                images.append(img_tensor)

        if not images:
            raise Exception("API 未返回图像数据")

        # Stack all images into batch
        result = torch.cat(images, dim=0)

        # Build info string
        info_data = {
            "model": model,
            "size": size,
            "quality": quality,
            "n": n,
        }
        if seed >= 0:
            info_data["seed"] = seed
        if "revised_prompt" in response["data"][0]:
            info_data["revised_prompt"] = response["data"][0]["revised_prompt"]

        info_str = json.dumps(info_data, ensure_ascii=False, indent=2)

        return (result, info_str)


class OneApiImg2Img:
    """
    Image-to-image editing node supporting OpenAI gpt-image-2 and compatible APIs.

    Supports multi-reference image input and input_fidelity for detail preservation.
    """

    CATEGORY = "OneApi"
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "info")
    FUNCTION = "generate"
    OUTPUT_NODE = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_url": ("STRING", {
                    "default": "https://api.openai.com/v1",
                    "multiline": False,
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
                "model": ("STRING", {
                    "default": "gpt-image-2",
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                }),
                "images": ("IMAGE",),
                "size": (SIZE_OPTIONS, {
                    "default": "1024x1024",
                }),
            },
            "optional": {
                "input_fidelity": (["high", "low"], {"default": "high"}),
                "quality": (["standard", "hd"], {"default": "standard"}),
                "background": (["opaque", "transparent"], {"default": "opaque"}),
                "moderation": (["auto", "low"], {"default": "auto"}),
                "output_format": (["png", "jpeg"], {"default": "png"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
                "n": ("INT", {"default": 1, "min": 1, "max": 10}),
                "extra_params": ("STRING", {"default": "", "multiline": True}),
            },
        }

    def __init__(self):
        pass

    def generate(
        self,
        base_url: str,
        api_key: str,
        model: str,
        prompt: str,
        images: torch.Tensor,
        size: str,
        input_fidelity: str = "high",
        quality: str = "standard",
        background: str = "opaque",
        moderation: str = "auto",
        output_format: str = "png",
        seed: int = -1,
        n: int = 1,
        extra_params: str = "",
    ):
        """
        Edit images with text prompt.

        Args:
            base_url: API base URL
            api_key: API key for authentication
            model: Model name
            prompt: Text prompt
            images: Reference images tensor batch
            size: Output size
            input_fidelity: Detail preservation level (high/low)
            quality: Image quality
            background: Background type
            moderation: Moderation level
            output_format: Output format
            seed: Random seed
            n: Number of images to generate
            extra_params: Additional JSON parameters

        Returns:
            Tuple of (image tensor, info string)
        """
        if not api_key.strip():
            raise Exception("API Key 不能为空，请输入有效的 API Key")

        if not prompt.strip():
            raise Exception("Prompt 不能为空，请输入提示词")

        # Convert images to base64 list
        format_upper = output_format.upper() if output_format != "jpeg" else "JPEG"
        images_b64 = tensor_batch_to_base64_list(images, format=format_upper)

        if not images_b64:
            raise Exception("参考图像不能为空，请提供至少一张参考图像")

        # Build payload
        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "input_fidelity": input_fidelity,
            "quality": quality,
            "background": background,
            "moderation": moderation,
            "output_format": output_format,
            "output": "b64_json",
            "n": n,
        }

        if seed >= 0:
            payload["seed"] = seed

        if extra_params.strip():
            try:
                extra = json.loads(extra_params)
                if isinstance(extra, dict):
                    payload.update(extra)
            except json.JSONDecodeError:
                raise Exception("extra_params 格式错误，请提供有效的 JSON 格式")

        # Make edit request
        try:
            response = make_edit_request(base_url, api_key, payload, images_b64)
        except Exception as e:
            raise e

        # Parse response
        if "data" not in response:
            raise Exception(f"API 响应格式错误：{response}")

        result_images = []
        for item in response["data"]:
            if "b64_json" in item:
                img_tensor = base64_to_tensor(item["b64_json"])
                result_images.append(img_tensor)

        if not result_images:
            raise Exception("API 未返回图像数据")

        result = torch.cat(result_images, dim=0)

        info_data = {
            "model": model,
            "size": size,
            "input_fidelity": input_fidelity,
            "quality": quality,
            "n": n,
            "input_images": len(images_b64),
        }
        if seed >= 0:
            info_data["seed"] = seed

        info_str = json.dumps(info_data, ensure_ascii=False, indent=2)

        return (result, info_str)


# Node class mappings for registration
NODE_CLASS_MAPPINGS = {
    "OneApiText2Img": OneApiText2Img,
    "OneApiImg2Img": OneApiImg2Img,
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "OneApiText2Img": "OneApi Text to Image",
    "OneApiImg2Img": "OneApi Image to Image",
}
