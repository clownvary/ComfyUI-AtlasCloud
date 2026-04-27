"""Image conversion utilities for ComfyUI AtlasCloud nodes."""

import base64
import io
import torch
import numpy as np
from PIL import Image


def tensor_to_base64(image_tensor: torch.Tensor, format: str = "PNG") -> str:
    """
    Convert ComfyUI IMAGE tensor to base64 string.

    Args:
        image_tensor: Tensor of shape (B, H, W, C) or (H, W, C), values 0-1
        format: Output image format (PNG or JPEG)

    Returns:
        Base64 encoded string of the image
    """
    if len(image_tensor.shape) == 4:
        image_tensor = image_tensor[0]

    arr = (image_tensor.cpu().numpy() * 255).astype(np.uint8)

    if arr.shape[2] == 4:
        mode = "RGBA"
    elif arr.shape[2] == 3:
        mode = "RGB"
    else:
        mode = "L"
        arr = arr[:, :, 0]

    pil_image = Image.fromarray(arr, mode=mode)

    buffer = io.BytesIO()
    pil_image.save(buffer, format=format)
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")


def base64_to_tensor(base64_string: str) -> torch.Tensor:
    """
    Convert base64 string to ComfyUI IMAGE tensor.

    Args:
        base64_string: Base64 encoded image string

    Returns:
        Tensor of shape (1, H, W, C), values 0-1
    """
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(io.BytesIO(image_data))

    # Convert to RGB (ComfyUI standard format)
    if pil_image.mode == "RGBA":
        # Create white background and composite
        background = Image.new("RGB", pil_image.size, (255, 255, 255))
        background.paste(pil_image, mask=pil_image.split()[3])
        pil_image = background
    elif pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")

    arr = np.array(pil_image).astype(np.float32) / 255.0

    return torch.from_numpy(arr).unsqueeze(0)


def tensor_batch_to_base64_list(image_tensor: torch.Tensor, format: str = "PNG") -> list:
    """
    Convert batch of IMAGE tensors to list of base64 strings.

    Args:
        image_tensor: Tensor of shape (B, H, W, C)
        format: Output image format

    Returns:
        List of base64 encoded strings
    """
    if len(image_tensor.shape) == 3:
        image_tensor = image_tensor.unsqueeze(0)

    results = []
    for i in range(image_tensor.shape[0]):
        single = image_tensor[i:i+1]
        results.append(tensor_to_base64(single, format))

    return results
