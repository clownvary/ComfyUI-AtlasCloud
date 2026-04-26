# ComfyUI OneApi

通用图像生成 API 节点，支持 OpenAI gpt-image-2 及所有 OpenAI-compatible 格式的 API。

## 功能

- **OneApiText2Img** - 文生图节点
- **OneApiImg2Img** - 图生图/编辑节点（支持多参考图）

只需配置 `base_url` + `api_key`，即可调用：
- OpenAI 官方 API
- 各类中转平台（API2D、OpenAI-SB 等）
- 自建服务

## 安装

将此目录放入 ComfyUI 的 `custom_nodes/` 文件夹：

```bash
cd ComfyUI/custom_nodes/
git clone <repo_url> comfyui_OneApi
```

重启 ComfyUI 即可使用。

## 节点参数

### OneApiText2Img

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| base_url | STRING | https://api.openai.com/v1 | API 基础 URL |
| api_key | STRING | - | API Key（必填） |
| model | STRING | gpt-image-2 | 模型名称 |
| prompt | STRING | - | 提示词（必填） |
| size | ENUM | 1024x1024 | 分辨率预设 |
| quality | ENUM | standard | 质量（standard/hd） |
| background | ENUM | opaque | 背景（opaque/transparent） |
| moderation | ENUM | auto | 内容审核（auto/low） |
| output_format | ENUM | png | 输出格式（png/jpeg） |
| seed | INT | -1 | 种子（-1=随机） |
| n | INT | 1 | 生成数量 |
| extra_params | STRING | - | JSON 额外参数 |

### OneApiImg2Img

额外参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| images | IMAGE | - | 参考图像 batch（必填） |
| input_fidelity | ENUM | high | 保留输入细节（high/low） |

## 分辨率预设（gpt-image-2 官方）

**1K:**
- 1024×768 (4:3)
- 768×1024 (3:4)
- 1024×1024 (1:1)
- 1024×1536 (2:3)
- 1536×1024 (3:2)

**2K:**
- 1920×1080 (16:9)
- 1080×1920 (9:16)
- 2560×1440 (16:9)
- 1440×2560 (9:16)

**3K:**
- 3840×2160 (16:9)
- 2160×3840 (9:16)

## 使用示例

### 文生图

1. 添加 `OneApi Text to Image` 节点
2. 填写 `api_key`
3. 输入 `prompt`
4. 选择 `size` 和其他参数
5. 连接到 `Save Image` 节点保存结果

### 图生图

1. 加载参考图像（使用 `Load Image` 节点）
2. 添加 `OneApi Image to Image` 节点
3. 连接参考图像到 `images` 输入
4. 填写 `api_key` 和 `prompt`
5. 设置 `input_fidelity`（high 保留更多细节）

## 中转平台配置

只需修改 `base_url` 为中转平台的地址：

```
base_url: https://api.api2d.com/v1
base_url: https://api.openai-sb.com/v1
```

其他参数保持不变。

## 错误提示

节点会显示友好的错误信息：
- 认证失败 → 检查 API Key
- 连接失败 → 检查 base_url
- 余额不足 → 账户充值
- 请求超时 → 检查网络

## License

MIT