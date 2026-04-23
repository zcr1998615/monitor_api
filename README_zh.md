# 网络流量监控工具 v1.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 📖 项目简介

这是一个基于 Python 和 Playwright 的**网络流量监控工具**，用于捕获浏览器中的所有网络请求（API接口），并自动保存到 Excel 文件中，方便后续进行接口分析和自动化测试。

### 核心功能

- 🎯 **实时流量拦截**：监控并记录所有 fetch 和 xhr 请求
- 📊 **详细数据捕获**：URL、Method、Headers、Payload、Response
- 🔒 **隐私保护**：使用浏览器无痕模式
- 📁 **自动保存**：关闭浏览器后自动生成 Excel 报表
- 🎨 **交互式界面**：简单易用的命令行操作
- 🌐 **双语支持**：完整的中文和英文版本

---

## 🛠️ 技术栈

- **Python 3.8+**
- **Playwright**：浏览器自动化和网络拦截
- **Pandas / Openpyxl**：Excel 文件生成
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

#### 方式一：双击启动（推荐）

1. **中文版**：双击 `run_zh.bat` 文件
2. **英文版**：双击 `run_en.bat` 文件
3. 在命令行中输入要监控的网站 URL
4. 按回车键，浏览器将自动打开
5. 在浏览器中进行您的手工操作
6. **关闭浏览器**窗口
7. 程序自动保存数据并显示文件路径

#### 方式二：命令行启动

```bash
# 中文版
cd monitor_api
python zh/monitor.py

# 英文版
cd monitor_api
python en/monitor.py
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
│   └── monitor.py                 # 中文版主程序
│
├── en/                            # 英文版目录
│   ├── __init__.py
│   └── monitor.py                 # 英文版主程序
│
├── run_zh.bat                     # 中文版启动脚本
├── run_en.bat                    # 英文版启动脚本
├── LICENSE                       # MIT 许可证
├── requirements.txt              # Python 依赖
├── README_zh.md                  # 本文档
└── README_en.md                  # 英文文档
```

---

## 📋 录制数据说明

### Excel 表格字段

| 字段名 | 说明 |
|--------|------|
| 时间 (Time) | 请求发送时间（精确到毫秒） |
| 方法 (Method) | HTTP方法（GET/POST/PUT/DELETE等） |
| URL | 完整的接口地址 |
| 请求头 (Request Headers) | 请求头信息（JSON格式） |
| 载荷 (Payload) | 请求体内容（POST参数等） |
| 状态 (Status) | HTTP状态码 |
| 响应头 (Response Headers) | 响应头信息（JSON格式） |
| 响应体 (Response Body) | 响应内容（JSON格式） |

### 输出文件命名规则

```
[域名]_[时间戳].xlsx
```

示例：
- `example_com_20260423_143052.xlsx`
- `api_website_20260423_150315.xlsx`

---

## 🎯 使用场景

### 1. 接口分析
- 了解网站的所有API调用
- 分析接口参数和响应结构
- 检查接口性能（通过时间戳）

### 2. 接口测试准备
- 快速收集测试数据
- 导出接口文档
- 准备测试用例

### 3. 问题排查
- 记录问题发生的完整请求流程
- 保存错误接口的详细信息
- 便于后续复现问题

---

## ⚙️ 高级用法

### 指定关键词过滤

在对应的 `monitor.py` 中可以修改过滤规则，只监控特定接口：

```python
# 中文版：修改 zh/monitor.py 中的 TrafficMonitor 初始化
from core.monitor_core_zh import TrafficMonitor
monitor = TrafficMonitor(url, output_file, filter_keywords=["api", "login"])

# 英文版：修改 en/monitor.py 中的 TrafficMonitor 初始化
from core.monitor_core_en import TrafficMonitor
monitor = TrafficMonitor(url, output_file, filter_keywords=["api", "login"])
```

### 自定义输出路径

修改对应版本 `monitor.py` 中的 `generate_filename()` 函数可以自定义文件输出位置。

---

## ❓ 常见问题

### Q1: 为什么没有捕获到任何请求？
- 确保目标网站有API调用（刷新页面、点击按钮等）
- 检查是否打开了正确的页面
- 确认不是纯静态页面

### Q2: 程序卡住了怎么办？
- 确保已经关闭了浏览器窗口
- 检查是否有弹窗阻止了关闭

### Q3: Excel文件太大怎么办？
- 减少操作时间，避免捕获过多数据
- 使用关键词过滤减少无关请求

### Q4: 中文显示乱码？
- 确保 Excel 文件使用 UTF-8 编码打开
- 在 Excel 中通过"数据→自文本"导入可正确识别中文

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

---

## 📝 版本历史

### v1.0 (2026-04-23)
- ✅ 实现基础的流量监控功能
- ✅ 支持交互式URL输入
- ✅ 自动生成Excel报表
- ✅ 优化浏览器关闭检测
- ✅ 添加完整的中文和英文双语支持

---

## 📜 许可证

本工具基于 MIT 许可证开源。

---

**制作日期**：2026-04-23
**工具版本**：v1.0
