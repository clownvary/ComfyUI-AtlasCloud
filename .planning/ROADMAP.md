# Roadmap: ComfyUI OneApi

**Created:** 2026-04-26
**Granularity:** Standard
**Total Phases:** 3

---

## Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Core Nodes | 实现两个核心节点 + API 调用逻辑 | T2I-01~11, I2I-01~09, ERR-01~03 | 3 |
| 2 | Polish & Test | 完善错误处理、测试验证 | (integration) | 3 |
| 3 | Release | 文档、发布准备 | (documentation) | 2 |

---

## Phase 1: Core Nodes

**Goal:** 实现两个核心节点 + API 调用逻辑

### Requirements Covered

- T2I-01~11: OneApiText2Img 完整实现
- I2I-01~09: OneApiImg2Img 完整实现
- ERR-01~03: 错误处理

### Success Criteria

1. 在 ComfyUI 中加载节点成功
2. 文生图节点可以调用 API 生成图像并输出 tensor
3. 图生图节点可以接收多张参考图并生成结果
4. 错误情况显示友好提示

### Approach

1. 创建项目文件结构
2. 实现图像转换工具（tensor ↔ base64）
3. 实现 HTTP 客户端（带重试）
4. 实现 OneApiText2Img 节点
5. 实现 OneApiImg2Img 节点（多图 batch 处理）
6. 错误处理和提示

### Files to Create

| File | Description |
|------|-------------|
| `__init__.py` | 节点注册入口 |
| `nodes.py` | 两个节点类定义 |
| `utils/image.py` | 图像转换工具 |
| `utils/http.py` | HTTP 客户端 |

---

## Phase 2: Polish & Test

**Goal:** 完善错误处理、测试验证

### Success Criteria

1. 所有参数正常工作
2. 错误信息清晰友好
3. 边界情况处理（空 prompt、无效 key 等）

### Approach

1. 手动测试所有参数组合
2. 测试错误情况
3. 优化错误信息
4. 代码清理

---

## Phase 3: Release

**Goal:** 文档、发布准备

### Success Criteria

1. README 完整（安装、使用、参数说明）
2. 示例工作流
3. 可发布到社区

### Approach

1. 编写 README.md
2. 创建示例工作流 JSON
3. 版本号和更新日志

---

## Dependencies

```
Phase 2 depends on Phase 1
Phase 3 depends on Phase 2
```

---
*Roadmap created: 2026-04-26*
*Last updated: 2026-04-26 after node design clarification*
