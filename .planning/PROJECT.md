# ComfyUI OneApi

## What This Is

一个 ComfyUI 自定义节点，提供统一的图像生成 API 调用接口。用户只需配置 API URL 和 API Key，即可调用多种图像生成平台（OpenAI gpt-image-2、Google Imagen 等），无需为每个平台安装专用节点。

**主要目标模型**：OpenAI gpt-image-2，参数设计优先适配此模型。

## Core Value

一个节点兼容多家图像生成 API 平台，降低用户接入成本，提升工作流灵活性。

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] 支持 OpenAI gpt-image-2 图像生成（text-to-image）
- [ ] 支持 gpt-image-2 多参考图编辑模式（image-to-image）
- [ ] 支持 Google Imagen 图像生成
- [ ] 支持 OpenAI-compatible 兼容格式 API
- [ ] 支持自定义平台配置
- [ ] 节点内直接配置参数（API URL、Key、模型等）
- [ ] 输出标准 ComfyUI IMAGE tensor
- [ ] 进度回调显示
- [ ] 模型选择功能
- [ ] 分辨率预设选项

### Out of Scope

- 外部配置文件管理 — 用户通过节点参数配置，不使用独立配置文件
- 独立的配置节点 — 所有配置在同一节点内完成
- 代理/中转服务配置 — 主要支持官方 API 直接调用
- 异步回调/webhook — 同步生成模式为主
- 视频生成 — 仅支持图像生成

## Context

### 技术背景
- ComfyUI 是一个基于节点的 Stable Diffusion 工作流工具
- 自定义节点通过 Python 类实现，定义 INPUT_TYPES、RETURN_TYPES、FUNCTION
- 图像格式为 PyTorch tensor（BHWC 格式，值范围 0-1）

### API 平台共性
- 认证：`Authorization: Bearer {key}` 或 `x-goog-api-key: {key}`
- 核心参数：prompt, size/width/height, model, n/num_outputs, seed
- 响应格式：base64 JSON、binary、或托管 URL

### gpt-image-2 特性
- 支持多参考图输入进行编辑
- 独有参数：quality (standard/hd), background (transparent/opaque), moderation (low/auto)
- 支持多种分辨率和宽高比

## Constraints

- **Tech Stack**: Python 3.x, PyTorch, requests/httpx, Pillow
- **Platform**: ComfyUI 自定义节点
- **Compatibility**: 需兼容 ComfyUI 最新版本（v0.17.x）
- **Dependencies**: 最小化外部依赖，优先使用 ComfyUI 内置库

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 参数设计以 gpt-image-2 为主 | gpt-image-2 是主要目标模型，功能最丰富 | — Pending |
| 多参考图输入使用 IMAGE_BATCH | ComfyUI 标准 batch 输入方式，支持多图 | — Pending |
| 不使用独立配置节点 | 简化用户操作，所有配置在一处完成 | — Pending |
| 同步生成模式 | 简化实现，符合大多数用户习惯 | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-26 after initialization*
