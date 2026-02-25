# 📂 Repcz (通用进阶配置)

[🔙 返回上一级](../README.md)

> 🤖 自动技术分析 | 2 个配置文件

## ⚔️ 配置横向对比

| 特性 | `config_lite.yaml` | `config.yaml` |
| :--- | :--- | :--- |
| **大小** | 3.0 KB | 8.2 KB |
| **混合端口** | 7893 | 7893 |
| **面板地址** | - | - |
| **运行模式** | rule | rule |
| **TUN** | ✅ | ✅ |
| **策略组** | **1** | **18** |
| **规则数** | **16** | **26** |

## 📄 配置详情

#### 📝 config_lite.yaml
- **路径**: `config_lite.yaml` | **大小**: 3.0 KB | [查看源码](https://github.com/opyzzzz/MIHOMO_YAMLS/blob/main/THEYAMLS/General_Config/Repcz/config_lite.yaml)
- **模式**: rule | **TUN**: ✅ | **IPv6**: 🚫
<details>
<summary>🔍 策略组 (1个)</summary>

| 名称 | 类型 |
| :--- | :--- |
| 👆 Proxy | `select` |
</details>

#### 📝 config.yaml
- **路径**: `config.yaml` | **大小**: 8.2 KB | [查看源码](https://github.com/opyzzzz/MIHOMO_YAMLS/blob/main/THEYAMLS/General_Config/Repcz/config.yaml)
- **模式**: rule | **TUN**: ✅ | **IPv6**: 🚫
<details>
<summary>🔍 策略组 (18个)</summary>

| 名称 | 类型 |
| :--- | :--- |
| 👆 手动切换 | `select` |
| 👆 国外网站 | `select` |
| 👆 国际媒体 | `select` |
| 👆 苹果服务 | `select` |
| 👆 微软服务 | `select` |
| 👆 谷歌服务 | `select` |
| 👆 电报消息 | `select` |
| 👆 推特消息 | `select` |
| 👆 AI | `select` |
| 👆 游戏平台 | `select` |
| 👆 Emby | `select` |
| 👆 Spotify | `select` |
| 👆 兜底分流 | `select` |
| ♻️ 香港节点 | `url-test` |
| ♻️ 美国节点 | `url-test` |
| ♻️ 狮城节点 | `url-test` |
| ♻️ 日本节点 | `url-test` |
| ♻️ 台湾节点 | `url-test` |
</details>
