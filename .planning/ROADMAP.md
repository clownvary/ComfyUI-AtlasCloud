# Roadmap: ComfyUI OneApi

**Created:** 2026-04-26
**Granularity:** Standard
**Total Phases:** 4

---

## Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Core + gpt-image-2 | 实现核心框架和 OpenAI gpt-image-2 完整支持 | OPENAI-01~10, PLAT-01~03, OUT-01~02 | 3 |
| 2 | Platform Expansion | 扩展支持 Google Imagen 和 OpenAI-compatible | GOOGLE-01~04, COMPAT-01~03 | 3 |
| 3 | UX Polish | 完善用户体验：进度、错误提示、tooltip | UX-01~03 | 3 |
| 4 | Release Prep | 文档、测试、社区发布准备 | (integration) | 3 |

---

## Phase 1: Core + gpt-image-2

**Goal:** 实现核心框架和 OpenAI gpt-image-2 完整支持

### Requirements Covered

- OPENAI-01: API Key 输入验证
- OPENAI-02: text-to-image 文本生成
- OPENAI-03: 多参考图编辑模式
- OPENAI-04: 模型版本选择
- OPENAI-05: 分辨率预设
- OPENAI-06: quality 参数
- OPENAI-07: background 参数
- OPENAI-08: moderation 参数
- OPENAI-09: seed 可复现
- OPENAI-10: 生成数量
- PLAT-01: 平台选择下拉
- PLAT-02: 动态模型列表
- PLAT-03: 平台对应参数
- OUT-01: IMAGE tensor 输出
- OUT-02: 节点可连接性

### Success Criteria

1. 用户可以在 ComfyUI 中加载节点并成功使用 gpt-image-2 生成图像
2. 多参考图编辑模式正常工作，支持多张参考图输入
3. 所有 gpt-image-2 专属参数（quality, background, moderation）可正常使用

### Approach

1. 创建项目文件结构（__init__.py, nodes.py, adapters/, utils/）
2. 实现 BaseAdapter 抽象类定义接口
3. 实现 OpenAIAdapter 适配 gpt-image-2 API
4. 实现图像转换工具（tensor ↔ base64）
5. 实现主节点类，定义输入输出
6. 实现多参考图输入逻辑
7. 基础错误处理

### Files to Create/Modify

| File | Description |
|------|-------------|
| `__init__.py` | 节点注册入口 |
| `nodes.py` | 主节点类定义 |
| `adapters/__init__.py` | 适配器模块入口 |
| `adapters/base.py` | BaseAdapter 抽象类 |
| `adapters/openai.py` | OpenAI API 适配器 |
| `utils/__init__.py` | 工具模块入口 |
| `utils/image.py` | 图像转换工具 |
| `utils/http.py` | HTTP 客户端 |

---

## Phase 2: Platform Expansion

**Goal:** 扩展支持 Google Imagen 和 OpenAI-compatible

### Requirements Covered

- GOOGLE-01~04: Google Imagen 基本支持
- COMPAT-01~03: OpenAI-compatible 兼容支持

### Success Criteria

1. 用户可以切换到 Google Imagen 平台并正常生成图像
2. 用户可以使用自定义 URL 接入 OpenAI-compatible 服务

### Approach

1. 实现 GoogleImagenAdapter
2. 实现 OpenAICompatibleAdapter
3. 平台预设配置（platforms.json 或代码内嵌）
4. 平台切换时参数动态适配
5. 各平台的错误响应处理

### Files to Create/Modify

| File | Description |
|------|-------------|
| `adapters/google_imagen.py` | Google Imagen 适配器 |
| `adapters/compatible.py` | OpenAI-compatible 适配器 |
| `presets/platforms.json` | 平台预设配置（可选） |

---

## Phase 3: UX Polish

**Goal:** 完善用户体验：进度、错误提示、tooltip

### Requirements Covered

- UX-01: 进度回调
- UX-02: 错误提示
- UX-03: 参数 tooltip

### Success Criteria

1. 生成过程中用户可以在控制台看到进度信息
2. API 错误时显示友好的错误信息（非原始 traceback）
3. 所有参数有清晰的 tooltip 说明

### Approach

1. 实现 ComfyUI 进度回调机制
2. 错误信息格式化和本地化
3. 为所有输入参数添加 tooltip
4. 参数默认值优化

---

## Phase 4: Release Prep

**Goal:** 文档、测试、社区发布准备

### Success Criteria

1. README 文档完整（安装、使用、参数说明）
2. 基本测试覆盖关键路径
3. 符合 ComfyUI 社区节点发布规范

### Approach

1. 编写 README.md（安装说明、使用示例、参数文档）
2. 编写使用示例工作流（JSON）
3. 代码清理和注释
4. 版本号和更新日志
5. GitHub release 准备

---

## Dependencies

```
Phase 2 depends on Phase 1
Phase 3 depends on Phase 1, 2
Phase 4 depends on Phase 1, 2, 3
```

---

## Notes

- Phase 1 是核心，优先确保 gpt-image-2 功能完整
- Phase 2 的 Google Imagen 支持可以简化，先实现基本功能
- Phase 4 可以与之前的 Phase 一起进行部分工作

---
*Roadmap created: 2026-04-26*
