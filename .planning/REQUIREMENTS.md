# Requirements: ComfyUI OneApi

**Defined:** 2026-04-26
**Core Value:** 一个节点兼容多家图像生成 API 平台，降低用户接入成本

## v1 Requirements

### OpenAI gpt-image-2 Support

- [ ] **OPENAI-01**: 用户可以输入 OpenAI API Key 进行身份验证
- [ ] **OPENAI-02**: 用户可以输入 prompt 文本生成图像（text-to-image）
- [ ] **OPENAI-03**: 用户可以输入多张参考图像进行编辑（image-to-image）
- [ ] **OPENAI-04**: 用户可以选择 gpt-image-2 模型版本
- [ ] **OPENAI-05**: 用户可以选择预设分辨率（1024x1024, 1024x1792, 1792x1024）
- [ ] **OPENAI-06**: 用户可以设置 quality 参数（standard, hd）
- [ ] **OPENAI-07**: 用户可以设置 background 参数（transparent, opaque）
- [ ] **OPENAI-08**: 用户可以设置 moderation 参数（low, auto）
- [ ] **OPENAI-09**: 用户可以设置 seed 值进行可复现生成
- [ ] **OPENAI-10**: 用户可以设置生成数量（num_outputs）

### Google Imagen Support

- [ ] **GOOGLE-01**: 用户可以输入 Google API Key 进行身份验证
- [ ] **GOOGLE-02**: 用户可以输入 prompt 文本生成图像
- [ ] **GOOGLE-03**: 用户可以选择 Imagen 模型版本
- [ ] **GOOGLE-04**: 用户可以选择预设分辨率

### OpenAI-Compatible Support

- [ ] **COMPAT-01**: 用户可以输入自定义 API URL
- [ ] **COMPAT-02**: 节点使用标准 OpenAI 格式构造请求
- [ ] **COMPAT-03**: 节点正确解析 OpenAI 格式的响应

### Platform Selection

- [ ] **PLAT-01**: 用户可以通过下拉菜单选择平台（OpenAI, Google, Compatible, Custom）
- [ ] **PLAT-02**: 切换平台时，模型列表动态更新
- [ ] **PLAT-03**: 切换平台时，显示对应平台的参数

### Output

- [ ] **OUT-01**: 节点输出标准 ComfyUI IMAGE tensor
- [ ] **OUT-02**: 输出图像可在工作流中继续连接其他节点处理

### Progress & UX

- [ ] **UX-01**: 生成过程中显示进度信息
- [ ] **UX-02**: API 错误时显示清晰的错误信息
- [ ] **UX-03**: 参数有清晰的 tooltip 说明

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Advanced Features

- **ADV-01**: 支持异步生成模式（webhook 回调）
- **ADV-02**: 支持更多平台（Replicate, Stability AI, Together AI）
- **ADV-03**: 支持图像修复（inpainting）
- **ADV-04**: 支持批量生成不同参数组合

## Out of Scope

| Feature | Reason |
|---------|--------|
| 外部配置文件 | 用户通过节点参数配置，简化操作 |
| 独立配置节点 | 所有配置在同一节点内完成 |
| 代理/中转服务 | 主要支持官方 API 直接调用 |
| 视频生成 | 仅支持图像生成，视频是独立项目 |
| 本地模型推理 | 本项目专注 API 调用，本地推理由其他节点处理 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| OPENAI-01 | Phase 1 | Pending |
| OPENAI-02 | Phase 1 | Pending |
| OPENAI-03 | Phase 1 | Pending |
| OPENAI-04 | Phase 1 | Pending |
| OPENAI-05 | Phase 1 | Pending |
| OPENAI-06 | Phase 1 | Pending |
| OPENAI-07 | Phase 1 | Pending |
| OPENAI-08 | Phase 1 | Pending |
| OPENAI-09 | Phase 1 | Pending |
| OPENAI-10 | Phase 1 | Pending |
| GOOGLE-01 | Phase 2 | Pending |
| GOOGLE-02 | Phase 2 | Pending |
| GOOGLE-03 | Phase 2 | Pending |
| GOOGLE-04 | Phase 2 | Pending |
| COMPAT-01 | Phase 2 | Pending |
| COMPAT-02 | Phase 2 | Pending |
| COMPAT-03 | Phase 2 | Pending |
| PLAT-01 | Phase 1 | Pending |
| PLAT-02 | Phase 1 | Pending |
| PLAT-03 | Phase 1 | Pending |
| OUT-01 | Phase 1 | Pending |
| OUT-02 | Phase 1 | Pending |
| UX-01 | Phase 3 | Pending |
| UX-02 | Phase 3 | Pending |
| UX-03 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 24 total
- Mapped to phases: 24
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-26*
*Last updated: 2026-04-26 after initial definition*
