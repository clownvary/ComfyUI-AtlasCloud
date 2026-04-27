# ComfyUI AtlasCloud

Image generation nodes for [atlascloud.ai](https://atlascloud.ai), supporting GPT Image 2 models.

## Nodes

- **AtlasCloud Text to Image** — text-to-image
- **AtlasCloud Image to Image** — image editing (up to 3 reference images)

## Installation

```bash
cd ComfyUI/custom_nodes/
git clone <repo_url> comfyui_AtlasCloud
```

Restart ComfyUI.

## Parameters

### AtlasCloudText2Img

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| base_url | STRING | `https://api.atlascloud.ai` | API base URL |
| api_key | STRING | - | API key (required) |
| prompt | STRING | - | Prompt (required) |
| model | STRING | `openai/gpt-image-2/text-to-image` | Model name |
| size | ENUM | `1024x1024` | Output resolution |
| quality | ENUM | `medium` | Quality: low / medium / high |
| output_format | ENUM | `jpeg` | Output format: jpeg / png |
| seed | INT | -1 | Random seed (-1 = random) |
| extra_params | STRING | - | Extra JSON params |

### AtlasCloudImg2Img

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| base_url | STRING | `https://api.atlascloud.ai` | API base URL |
| api_key | STRING | - | API key (required) |
| image_1 | IMAGE | - | Reference image (required) |
| prompt | STRING | - | Prompt (required) |
| image_2 | IMAGE | - | Reference image 2 (optional) |
| image_3 | IMAGE | - | Reference image 3 (optional) |
| model | STRING | `openai/gpt-image-2/edit` | Model name |
| size | ENUM | `1024x1024` | Output resolution |
| quality | ENUM | `medium` | Quality: low / medium / high |
| output_format | ENUM | `jpeg` | Output format: jpeg / png |
| input_fidelity | ENUM | `high` | Detail preservation: high / low |
| seed | INT | -1 | Random seed (-1 = random) |
| extra_params | STRING | - | Extra JSON params |

## Resolutions

1K: `1024x768`, `768x1024`, `1024x1024`, `1024x1536`, `1536x1024`
2K: `1920x1080`, `1080x1920`, `2560x1440`, `1440x2560`
3K: `3840x2160`, `2160x3840`

## License

MIT
