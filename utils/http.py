"""HTTP client utilities with retry logic."""

import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_http_client(timeout: float = 300.0, max_retries: int = 3) -> requests.Session:
    """
    Create HTTP client with retry logic.

    Args:
        timeout: Request timeout in seconds
        max_retries: Maximum number of retries

    Returns:
        Configured requests Session
    """
    session = requests.Session()

    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def make_api_request(
    base_url: str,
    api_key: str,
    payload: dict,
    timeout: float = 300.0,
) -> dict:
    """
    Make API request to image generation endpoint.

    Args:
        base_url: API base URL
        api_key: API key for authentication
        payload: Request payload
        timeout: Request timeout in seconds

    Returns:
        Response JSON

    Raises:
        Exception: If request fails with error message
    """
    client = create_http_client(timeout=timeout)

    url = base_url.rstrip("/") + "/images/generations"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = client.post(url, headers=headers, json=payload, timeout=timeout)

        if response.status_code == 401:
            raise Exception("认证失败：API Key 无效或已过期，请检查您的 API Key")

        if response.status_code == 403:
            raise Exception("访问被拒绝：您的账户可能没有权限或余额不足")

        if response.status_code == 429:
            raise Exception("请求过于频繁：请稍后重试")

        if response.status_code >= 500:
            raise Exception(f"服务器错误 ({response.status_code})：请稍后重试")

        if not response.ok:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", response.text)
            except:
                error_msg = response.text
            raise Exception(f"API 错误：{error_msg}")

        return response.json()

    except requests.exceptions.Timeout:
        raise Exception("请求超时：请检查网络连接或增加超时时间")
    except requests.exceptions.ConnectionError:
        raise Exception("连接失败：无法连接到 API 服务器，请检查 base_url 是否正确")
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败：{str(e)}")


def make_edit_request(
    base_url: str,
    api_key: str,
    payload: dict,
    images_b64: list,
    timeout: float = 300.0,
) -> dict:
    """
    Make API request for image editing with reference images.

    Args:
        base_url: API base URL
        api_key: API key for authentication
        payload: Request payload (prompt, size, etc.)
        images_b64: List of base64 encoded reference images
        timeout: Request timeout in seconds

    Returns:
        Response JSON
    """
    client = create_http_client(timeout=timeout)

    url = base_url.rstrip("/") + "/images/edits"

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    files = []
    for i, img_b64 in enumerate(images_b64):
        img_data = base64.b64decode(img_b64)
        files.append(("image[]", (f"image_{i}.png", img_data, "image/png")))

    data = {k: (v if not isinstance(v, (list, dict)) else json.dumps(v)) for k, v in payload.items()}

    try:
        response = client.post(url, headers=headers, data=data, files=files, timeout=timeout)

        if response.status_code == 401:
            raise Exception("认证失败：API Key 无效或已过期，请检查您的 API Key")

        if response.status_code == 403:
            raise Exception("访问被拒绝：您的账户可能没有权限或余额不足")

        if response.status_code == 429:
            raise Exception("请求过于频繁：请稍后重试")

        if response.status_code >= 500:
            raise Exception(f"服务器错误 ({response.status_code})：请稍后重试")

        if not response.ok:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", response.text)
            except:
                error_msg = response.text
            raise Exception(f"API 错误：{error_msg}")

        return response.json()

    except requests.exceptions.Timeout:
        raise Exception("请求超时：请检查网络连接或增加超时时间")
    except requests.exceptions.ConnectionError:
        raise Exception("连接失败：无法连接到 API 服务器，请检查 base_url 是否正确")
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败：{str(e)}")


import base64
