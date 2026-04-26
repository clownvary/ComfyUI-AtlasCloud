# Requirements: ComfyUI OneApi

**Defined:** 2026-04-26
**Core Value:** 一个节点兼容多家 API 平台，通过 base_url + api_key 通用接入

## v1 Requirements

### OneApiText2Img Node

- [ ] **T2I-01**: 用户可以输入 base_url 和 api_key 进行 API 连接
- [ ] **T2I-02**: 用户可以输入 prompt 文本生成图像
- [ ] **T2I-03**: 用户可以选择官方分辨率预设（1K/2K/3K 共 13 个选项）
- [ ] **T2I-04**: 用户可以设置 quality 参数（standard/hd）
- [ ] **T2I-05**: 用户可以设置 background 参数（opaque/transparent）
- [ ] **T2I-06**: 用户可以设置 moderation 参数（auto/low）
- [ ] **T2I-07**: 用户可以选择输出格式（png/jpeg）
- [ ] **T2I-08**: 用户可以设置 seed 值（-1 为随机）
- [ ] **T2I-09**: 用户可以设置生成数量 n
- [ ] **T2I-10**: 用户可以通过 extra_params 传递额外 JSON 参数
- [ ] **T2I-11**: 节点输出 ComfyUI IMAGE tensor

### OneApiImg2Img Node

- [ ] **I2I-01**: 用户可以输入 base_url 和 api_key 进行 API 连接
- [ ] **I2I-02**: 用户可以输入 prompt 文本进行图像编辑
- [ ] **I2I-03**: 用户可以输入多张参考图像（IMAGE batch）
- [ ] **I2I-04**: 用户可以设置 input_fidelity 参数（high/low）
- [ ] **I2I-05**: 用户可以选择官方分辨率预设
- [ ] **I2I-06**: 用户可以设置 quality、background、moderation 参数
- [ ] **I2I-07**: 用户可以选择输出格式（png/jpeg）
- [ ] **I2I-08**: 用户可以设置 seed 值和生成数量
- [ ] **I2I-09**: 节点输出 ComfyUI IMAGE tensor

### Error Handling

- [ ] **ERR-01**: API Key 错误时显示清晰的认证失败信息
- [ ] **ERR-02**: 网络错误时显示连接失败信息并提示重试
- [ ] **ERR-03**: API 返回错误时显示具体错误信息

## v2 Requirements

Deferred to future release.

- 异步生成模式
- 更多平台原生支持
- 图像修复（inpainting）

## Out of Scope

| Feature | Reason |
|---------|--------|
| 平台预设选择 | 用 base_url 替代，更通用 |
| 独立配置节点 | 所有配置在节点内完成 |
| 代理/中转服务 | 通过自定义 base_url 覆盖 |
| 视频生成 | 仅支持图像生成 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| T2I-01 | Phase 1 | Pending |
| T2I-02 | Phase 1 | Pending |
| T2I-03 | Phase 1 | Pending |
| T2I-04 | Phase 1 | Pending |
| T2I-05 | Phase 1 | Pending |
| T2I-06 | Phase 1 | Pending |
| T2I-07 | Phase 1 | Pending |
| T2I-08 | Phase 1 | Pending |
| T2I-09 | Phase 1 | Pending |
| T2I-10 | Phase 1 | Pending |
| T2I-11 | Phase 1 | Pending |
| I2I-01 | Phase 1 | Pending |
| I2I-02 | Phase 1 | Pending |
| I2I-03 | Phase 1 | Pending |
| I2I-04 | Phase 1 | Pending |
| I2I-05 | Phase 1 | Pending |
| I2I-06 | Phase 1 | Pending |
| I2I-07 | Phase 1 | Pending |
| I2I-08 | Phase 1 | Pending |
| I2I-09 | Phase 1 | Pending |
| ERR-01 | Phase 1 | Pending |
| ERR-02 | Phase 1 | Pending |
| ERR-03 | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-26*
*Last updated: 2026-04-26 after node design clarification*
