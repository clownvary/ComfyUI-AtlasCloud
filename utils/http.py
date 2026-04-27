"""HTTP client utilities for atlascloud.ai API."""

import base64
import time
import requests


def _normalize_base_url(base_url: str) -> str:
    base_url = base_url.rstrip("/")
    if base_url.endswith("/api/v1"):
        base_url = base_url[:-7]
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    return base_url or "https://api.atlascloud.ai"


def _poll_until_done(base_url: str, api_key: str, prediction_id: str, timeout: float) -> dict:
    """Poll prediction status until completed/succeeded or failed."""
    poll_url = f"{base_url}/api/v1/model/prediction/{prediction_id}"

    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise Exception(f"Request timed out after {timeout} seconds.")

        response = requests.get(poll_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
        result = response.json()

        status = result.get("data", {}).get("status", "unknown")

        if status in ("completed", "succeeded"):
            outputs = result["data"].get("outputs", [])
            if not outputs:
                raise Exception("Generation completed but no images returned.")
            return convert_to_b64_response(outputs)

        elif status == "failed":
            error_msg = result["data"].get("error") or "Generation failed"
            raise Exception(f"Generation failed: {error_msg}")

        else:
            time.sleep(2)


def make_api_request(
    base_url: str,
    api_key: str,
    payload: dict,
    timeout: float = 300.0,
) -> dict:
    """Submit image generation request and poll until done."""
    base_url = _normalize_base_url(base_url)
    generate_url = f"{base_url}/api/v1/model/generateImage"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    generate_response = requests.post(generate_url, headers=headers, json=payload, timeout=timeout)

    if generate_response.status_code != 200:
        error_text = generate_response.text or "(empty response)"
        raise Exception(f"API error ({generate_response.status_code}): {error_text}")

    generate_result = generate_response.json()

    if "data" not in generate_result or "id" not in generate_result["data"]:
        raise Exception(f"Unexpected API response format: {generate_result}")

    prediction_id = generate_result["data"]["id"]

    return _poll_until_done(base_url, api_key, prediction_id, timeout)


def convert_to_b64_response(outputs: list) -> dict:
    """Convert URL outputs to base64 format for ComfyUI."""
    data_list = []

    for output in outputs:
        if output.startswith("data:"):
            # Data URI format: data:image/jpeg;base64,/9j/4AAQ...
            # Extract base64 part after comma
            base64_data = output.split(",", 1)[-1]
            data_list.append({"b64_json": base64_data})
        elif output.startswith("http"):
            img_response = requests.get(output, timeout=60)
            if img_response.ok:
                img_b64 = base64.b64encode(img_response.content).decode("utf-8")
                data_list.append({"b64_json": img_b64})
            else:
                raise Exception(f"Failed to download image: {output}")
        else:
            # Already pure base64
            data_list.append({"b64_json": output})

    return {"data": data_list}


def make_edit_request(
    base_url: str,
    api_key: str,
    payload: dict,
    timeout: float = 300.0,
) -> dict:
    """Submit image edit request and poll until done."""
    base_url = _normalize_base_url(base_url)
    generate_url = f"{base_url}/api/v1/model/generateImage"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    generate_response = requests.post(generate_url, headers=headers, json=payload, timeout=timeout)

    if generate_response.status_code != 200:
        error_text = generate_response.text or "(empty response)"
        raise Exception(f"API error ({generate_response.status_code}): {error_text}")

    generate_result = generate_response.json()

    if "data" not in generate_result or "id" not in generate_result["data"]:
        raise Exception(f"Unexpected API response format: {generate_result}")

    prediction_id = generate_result["data"]["id"]

    return _poll_until_done(base_url, api_key, prediction_id, timeout)
