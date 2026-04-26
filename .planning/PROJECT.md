# ComfyUI OneApi

## What This Is

两个 ComfyUI 自定义节点，提供统一的图像生成 API 调用接口：
- **OneApiText2Img**：文生图节点
- **OneApiImg2Img**：图生图/编辑节点（支持多参考图）

用户只需配置 `base_url` + `api_key`，即可调用 OpenAI gpt-image-2 及所有 OpenAI-compatible 格式的 API（覆盖官方 API、中转平台、自建服务）。

## Core Value

一个节点兼容多家 API 平台，通过 base_url + api_key 通用接入。

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] OneApiText2Img 节点实现
- [ ] OneApiImg2Img 节点实现（支持多参考图）
- [ ] 官方分辨率预设（1K/2K/3K）
- [ ] gpt-image-2 完整参数支持
- [ ] OpenAI-compatible API 兼容
- [ ] 输出格式选择（png/jpeg）
- [ ] 错误处理和提示

### Out of Scope

- 平台预设选择（用 base_url 替代）
- 独立配置节点
- 代理/中转服务配置（通过 base_url 覆盖）
- 视频生成

## Context

### 节点参数设计

**OneApiText2Img**：
| 参数 | 类型 | 默认值 |
|------|------|--------|
| base_url | STRING | https://api.openai.com/v1 |
| api_key | STRING | - |
| model | STRING | gpt-image-2 |
| prompt | STRING | - |
| size | ENUM | 1024x1024 |
| quality | ENUM | standard |
| background | ENUM | opaque |
| moderation | ENUM | auto |
| output_format | ENUM | png |
| seed | INT | -1 |
| n | INT | 1 |
| extra_params | STRING | - |

**OneApiImg2Img**（额外参数）：
| 参数 | 类型 | 默认值 |
|------|------|--------|
| images | IMAGE | - (必填) |
| input_fidelity | ENUM | high |

**size 官方预设**：
- 1K: 1024x768, 768x1024, 1024x1024, 1024x1536, 1536x1024
- 2K: 1920x1080, 1080x1920, 2560x1440, 1440x2560
- 3K: 3840x2160, 2160x3840

## Constraints

- **Tech Stack**: Python 3.x, PyTorch, requests, Pillow
- **Platform**: ComfyUI 自定义节点
- **Dependencies**: 最小化外部依赖

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 按功能拆分为两个节点 | 文生图/图生图逻辑差异大，分开更清晰易测试 | — Pending |
| 用 base_url + api_key 替代平台预设 | 覆盖官方、中转、自建，更通用 | — Pending |
| 分辨率使用官方预设 | 确保与 gpt-image-2 兼容 | — Pending |

---
*Last updated: 2026-04-26 after node design clarification*
