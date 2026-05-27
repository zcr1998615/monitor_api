# 网络流量监控工具 v2.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 📖 项目简介

这是一个基于 Python 和 Playwright 的**网络流量监控工具**，用于捕获浏览器中的所有网络请求（API接口），并自动保存到 Excel 和 HAR 文件中，方便后续进行接口分析和自动化测试。

### 核心功能

- 🎯 **实时流量拦截**：监控并记录所有 fetch 和 xhr 请求
- 📊 **详细数据捕获**：URL、Method、Headers、Payload、Response、耗时
- 🔒 **隐私保护**：使用浏览器无痕模式
- 📁 **多格式导出**：Excel（美化格式）+ HAR + cURL + 接口文档
- 🔍 **强大过滤**：关键词、域名排除、HTTP 方法、状态码、正则匹配
- 🗂️ **多标签页支持**：自动监控所有新开标签页
- 📈 **实时统计**：请求数、成功/失败、平均耗时实时显示
- 🔄 **录制对比**：两次录制 diff，发现接口变更
- 🎨 **交互式 + CLI**：支持交互式操作和命令行参数两种模式
- 🌐 **双语支持**：完整的中文和英文版本

---

## 🛠️ 技术栈

- **Python 3.8+**
- **Playwright**：浏览器自动化和网络拦截
- **Pandas / Openpyxl**：Excel 文件生成与美化
- **JSON**：数据结构化处理

---

## 🚀 快速开始

### 环境要求

```bash
# 1. 安装所有 Python 依赖（一键安装，推荐）
pip install -r requirements.txt

# 2. 安装浏览器驱动
playwright install chromium
```

### 使用方法

#### 方式一：双击启动（推荐新手）

1. **中文版**：双击 `run_zh.bat` 文件
2. **英文版**：双击 `run_en.bat` 文件
3. 在命令行中输入要监控的网站 URL
4. 按回车键，浏览器将自动打开
5. 在浏览器中进行您的手工操作（支持多标签页）
6. **关闭浏览器**窗口
7. 程序自动保存数据并显示文件路径

#### 方式二：命令行启动（推荐进阶用户）

```bash
# 基础用法 - 交互式
python zh/monitor.py

# 直接指定 URL
python zh/monitor.py https://example.com

# 关键词过滤 - 只捕获包含 api 或 login 的请求
python zh/monitor.py https://example.com -f api login

# 只捕获 POST 和 PUT 请求
python zh/monitor.py https://example.com -m POST PUT

# 只看失败请求
python zh/monitor.py https://example.com -s fail

# 排除 CDN 域名
python zh/monitor.py https://example.com -e cdn.example.com static.example.com

# URL 正则匹配
python zh/monitor.py https://example.com -r "/api/v[0-9]+"

# 生成 cURL 命令文件和接口文档
python zh/monitor.py https://example.com --curl --docs

# 追加到已有 Excel 文件（新 sheet）
python zh/monitor.py https://example.com --append -o recordings/existing.xlsx

# 对比两次录制
python zh/monitor.py --compare recordings/before.xlsx recordings/after.xlsx
```

#### 查看完整参数帮助

```bash
python zh/monitor.py -h
```

---

## 📂 项目结构

```
monitor_api/
├── core/                          # 核心模块目录
│   ├── __init__.py
│   ├── monitor_core_zh.py         # 中文版核心模块
│   └── monitor_core_en.py         # 英文版核心模块
│
├── zh/                            # 中文版目录
│   ├── __init__.py
│   ├── monitor.py                 # 中文版主程序
│   └── recordings/                # 中文版录制数据
│
├── en/                            # 英文版目录
│   ├── __init__.py
│   ├── monitor.py                 # 英文版主程序
│   └── recordings/                # 英文版录制数据
│
├── run_zh.bat                     # 中文版启动脚本
├── run_en.bat                     # 英文版启动脚本
├── LICENSE                        # MIT 许可证
├── requirements.txt               # Python 依赖
├── README_zh.md                   # 本文档
└── README_en.md                   # 英文文档
```

---

## 🎛️ 命令行参数

| 参数 | 缩写 | 说明 | 示例 |
|------|------|------|------|
| `url` | - | 要监控的网站 URL（可选，不填则进入交互式模式） | `https://example.com` |
| `--filter` | `-f` | 关键词过滤，包含任一关键词的请求会被捕获 | `-f api login` |
| `--exclude` | `-e` | 排除的域名（如 CDN、统计服务） | `-e cdn.example.com` |
| `--method` | `-m` | 只捕获指定的 HTTP 方法 | `-m POST PUT DELETE` |
| `--status` | `-s` | 状态码过滤 | `-s fail` / `-s 4xx` / `-s 200` |
| `--regex` | `-r` | URL 正则匹配 | `-r "/api/v[0-9]+"` |
| `--output` | `-o` | 自定义输出文件路径 | `-o output.xlsx` |
| `--append` | - | 追加模式，写入已有 Excel 的新 sheet | `--append -o existing.xlsx` |
| `--curl` | - | 额外生成 cURL 命令文件 | `--curl` |
| `--docs` | - | 额外生成接口文档（Markdown） | `--docs` |
| `--compare` | - | 对比两次录制文件 | `--compare a.xlsx b.xlsx` |

### 状态码过滤选项

| 值 | 说明 |
|----|------|
| `fail` | 只捕获 4xx 和 5xx 错误 |
| `2xx` | 只捕获成功请求 |
| `4xx` | 只捕获客户端错误 |
| `5xx` | 只捕获服务端错误 |
| `200` | 只捕获指定状态码 |

---

## 📋 录制数据说明

### Excel 表格字段

| 字段名 | 说明 |
|--------|------|
| 时间 | 请求发送时间（精确到毫秒） |
| 方法 | HTTP 方法（GET/POST/PUT/DELETE 等） |
| URL | 完整的接口地址（可点击跳转） |
| 请求头 | 请求头信息（JSON 格式） |
| 载荷 | 请求体内容（POST 参数等） |
| 状态 | HTTP 状态码（颜色标记：2xx绿/4xx黄/5xx红） |
| 耗时(ms) | 请求到响应的耗时（毫秒） |
| 响应头 | 响应头信息（JSON 格式） |
| 响应体 | 响应内容（JSON 格式） |

### Excel 美化特性

- 表头冻结（滚动时表头保持可见）
- 蓝底白字加粗表头
- 自动列宽调整
- 状态码颜色标记（2xx 绿色 / 4xx 黄色 / 5xx 红色）
- URL 列可点击超链接

### 输出文件

每次录制会生成以下文件（以 `example_com_20260527_143052` 为例）：

| 文件 | 说明 | 何时生成 |
|------|------|----------|
| `*.xlsx` | Excel 录制数据 | 始终生成 |
| `*.har` | HAR 格式（可导入 Postman/Chrome DevTools/Charles） | 始终生成 |
| `*_curl.sh` | cURL 命令集（可直接在终端执行） | 使用 `--curl` 时 |
| `*_api_docs.md` | 接口文档（按域名+路径去重） | 使用 `--docs` 时 |
| `*_compare.md` | 对比报告 | 使用 `--compare` 时 |

---

## 🎯 使用场景

### 1. 接口分析
- 了解网站的所有 API 调用
- 分析接口参数和响应结构
- 通过耗时字段检查接口性能

### 2. 接口测试准备
- 快速收集测试数据
- 自动生成接口文档（`--docs`）
- 导出 cURL 命令直接复用（`--curl`）
- HAR 文件导入 Postman 批量创建请求

### 3. 回归测试
- 录制基线版本接口数据
- 新版本再次录制
- 使用 `--compare` 对比差异，发现接口变更

### 4. 问题排查
- 记录问题发生的完整请求流程
- 使用 `-s fail` 只看失败请求
- 保存错误接口的详细信息

---

## ⚙️ 高级用法

### 过滤组合示例

```bash
# 只看 POST 请求中包含 api 关键词且失败的请求，排除 CDN
python zh/monitor.py https://example.com \
  -f api \
  -m POST \
  -s fail \
  -e cdn.example.com
```

### 断点续录

多次录制写入同一个 Excel 文件的不同 sheet：

```bash
# 第一次录制
python zh/monitor.py https://example.com -o recordings/test_flow.xlsx

# 第二次录制（追加到新 sheet）
python zh/monitor.py https://example.com --append -o recordings/test_flow.xlsx
```

### 录制对比

```bash
# 对比两次录制，生成差异报告
python zh/monitor.py --compare recordings/v1.xlsx recordings/v2.xlsx

# 自定义报告输出路径
python zh/monitor.py --compare recordings/v1.xlsx recordings/v2.xlsx -o report.md
```

对比报告内容：
- 新增接口（B 中有但 A 中没有）
- 移除接口（A 中有但 B 中没有）
- 变更接口（状态码变化、请求体变化、响应字段增减）

### 自动生成接口文档

```bash
python zh/monitor.py https://example.com --docs
```

生成的 Markdown 文档按域名分组，每个接口包含：
- HTTP 方法和路径
- 状态码和耗时
- 请求体示例（JSON 格式）
- 响应体示例（JSON 格式，超长自动截断）

### 生成 cURL 命令

```bash
python zh/monitor.py https://example.com --curl
```

每条请求自动转换为可执行的 cURL 命令，方便在终端中重放调试。

---

## ❓ 常见问题

### Q1: 为什么没有捕获到任何请求？
- 确保目标网站有 API 调用（刷新页面、点击按钮等）
- 检查是否打开了正确的页面
- 确认不是纯静态页面
- 检查过滤条件是否过于严格

### Q2: 程序卡住了怎么办？
- 确保已经关闭了所有浏览器标签页
- 检查是否有弹窗阻止了关闭

### Q3: Excel 文件太大怎么办？
- 减少操作时间，避免捕获过多数据
- 使用 `-f` 关键词过滤减少无关请求
- 使用 `-e` 排除 CDN 等静态资源域名
- 使用 `-m` 只捕获需要的 HTTP 方法

### Q4: 中文显示乱码？
- 确保 Excel 文件使用 UTF-8 编码打开
- 在 Excel 中通过"数据→自文本"导入可正确识别中文

### Q5: 新开的标签页请求没被捕获？
- v2.0 已支持多标签页监控，无需额外配置
- 所有在同一个浏览器窗口中新开的标签页都会自动纳入监控

---

## 🔧 故障排查

### 错误：ModuleNotFoundError
```bash
# 重新安装依赖
pip install -r requirements.txt
playwright install chromium
```

### 错误：浏览器无法启动
```bash
# 重新安装浏览器驱动
playwright install chromium
```

### 错误：权限拒绝
- 确保有写入 `recordings/` 目录的权限
- 尝试以管理员身份运行程序

---

## ⚖️ 法律声明

**重要提示**：本工具仅供合法使用。

### ✅ 合法用途
- 开发、测试和调试自己的 Web 应用程序
- 分析公开 API 的调用方式和数据结构
- 安全研究和渗透测试（仅限已授权的系统）
- 学习 HTTP 协议和网络请求的工作原理

### ❌ 禁止用途
- 未经授权拦截、监控或分析他人的网络流量
- 访问未经明确授权的系统、资源或数据
- 收集他人的登录凭证、个人隐私信息或商业机密
- 任何违反当地法律法规的活动

### ⚠️ 风险提示
- 某些网站和 API 的服务条款明确禁止自动化的流量拦截
- 未经授权的网络监控行为在很多司法管辖区属于违法
- 使用本工具即表示您同意承担所有使用风险

**类比说明**：本工具功能类似于 Chrome DevTools 网络面板、Burp Suite、Fiddler 等调试工具，这类工具在开发者社区是标准工具，但同样需要在授权范围内使用。

---

**© 2024 - 请负责任地使用**

---

## 📞 技术支持

如遇问题，请检查：
1. Python 版本是否 >= 3.8
2. 所有依赖是否正确安装
3. 浏览器驱动是否完整安装
4. 网络连接是否正常
5. 运行 `python zh/monitor.py -h` 查看参数帮助

---

## 📝 版本历史

### v2.0 (2026-05-27)
- ✅ Excel 美化：表头冻结、自动列宽、状态码着色、URL 超链接
- ✅ 请求耗时统计（ms 级精度）
- ✅ 实时统计面板：请求数、成功/失败、平均耗时
- ✅ HAR 格式导出（可导入 Postman/Chrome DevTools/Charles）
- ✅ 增强过滤：域名排除、HTTP 方法、状态码、正则匹配
- ✅ 多标签页支持：自动监控所有新开标签页
- ✅ 断点续录：追加模式写入已有 Excel 的新 sheet
- ✅ 命令行参数（argparse）：支持脚本化和 CI 集成
- ✅ 自动生成接口文档（Markdown 格式）
- ✅ cURL 命令生成
- ✅ 录制对比：两次录制 diff，发现新增/移除/变更接口

### v1.0 (2026-04-23)
- ✅ 实现基础的流量监控功能
- ✅ 支持交互式 URL 输入
- ✅ 自动生成 Excel 报表
- ✅ 优化浏览器关闭检测
- ✅ 添加完整的中文和英文双语支持

---

## 📜 许可证

本工具基于 MIT 许可证开源。

---

**制作日期**：2026-04-23
**最后更新**：2026-05-27
**工具版本**：v2.0
