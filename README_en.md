# Network Traffic Monitor v1.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 📖 Project Introduction

This is a **Network Traffic Monitor Tool** built with Python and Playwright. It captures all network requests (API calls) in the browser and automatically saves them to Excel files for easy analysis and automated testing.

### Core Features

- 🎯 **Real-time Traffic Interception**: Monitor and record all fetch and xhr requests
- 📊 **Detailed Data Capture**: URL, Method, Headers, Payload, Response
- 🔒 **Privacy Protection**: Uses browser incognito mode
- 📁 **Auto-save**: Automatically generates Excel reports after closing the browser
- 🎨 **Interactive Interface**: Simple and easy-to-use command-line operation
- 🌐 **Bilingual Support**: Complete Chinese and English versions

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Playwright**: Browser automation and network interception
- **Pandas / Openpyxl**: Excel file generation
- **JSON**: Data structuring

---

## 🚀 Quick Start

### Requirements

```bash
# 1. Install all Python dependencies (one-click install, recommended)
pip install -r requirements.txt

# 2. Install browser drivers
playwright install chromium
```

### How to Use

#### Method 1: Double-click to Launch (Recommended)

1. **Chinese Version**: Double-click `run_zh.bat`
2. **English Version**: Double-click `run_en.bat`
3. Enter the website URL you want to monitor in the command line
4. Press Enter, the browser will automatically open
5. Perform your manual operations in the browser
6. **Close the browser** window
7. The program automatically saves data and displays the file path

#### Method 2: Command Line Launch

```bash
# Chinese version
cd monitor_api
python zh/monitor.py

# English version
cd monitor_api
python en/monitor.py
```

---

## 📂 Project Structure

```
monitor_api/
├── core/                          # Core module directory
│   ├── __init__.py
│   ├── monitor_core_zh.py         # Chinese core module
│   └── monitor_core_en.py         # English core module
│
├── zh/                            # Chinese version directory
│   ├── __init__.py
│   └── monitor.py                 # Chinese main program
│
├── en/                            # English version directory
│   ├── __init__.py
│   └── monitor.py                 # English main program
│
├── run_zh.bat                     # Chinese version launch script
├── run_en.bat                    # English version launch script
├── LICENSE                       # MIT License
├── requirements.txt              # Python dependencies
├── README_zh.md                  # Chinese documentation
└── README_en.md                  # This file
```

---

## 📋 Recording Data Description

### Excel Table Fields

| Field | Description |
|-------|-------------|
| Time | Request timestamp (millisecond precision) |
| Method | HTTP method (GET/POST/PUT/DELETE, etc.) |
| URL | Complete API endpoint |
| Request Headers | Request header information (JSON format) |
| Payload | Request body content (POST parameters, etc.) |
| Status | HTTP status code |
| Response Headers | Response header information (JSON format) |
| Response Body | Response content (JSON format) |

### Output File Naming Convention

```
[domain]_[timestamp].xlsx
```

Examples:
- `example_com_20260423_143052.xlsx`
- `api_website_20260423_150315.xlsx`

---

## 🎯 Use Cases

### 1. API Analysis
- Understand all API calls made by a website
- Analyze API parameter and response structures
- Check API performance (via timestamps)

### 2. API Testing Preparation
- Quickly collect test data
- Export API documentation
- Prepare test cases

### 3. Problem Troubleshooting
- Record complete request flow when issues occur
- Save detailed error information
- Facilitate later problem reproduction

---

## ⚙️ Advanced Usage

### Specify Keyword Filtering

Modify the filter rules in the corresponding `monitor.py` to only monitor specific interfaces:

```python
# Chinese version: modify zh/monitor.py TrafficMonitor initialization
from core.monitor_core_zh import TrafficMonitor
monitor = TrafficMonitor(url, output_file, filter_keywords=["api", "login"])

# English version: modify en/monitor.py TrafficMonitor initialization
from core.monitor_core_en import TrafficMonitor
monitor = TrafficMonitor(url, output_file, filter_keywords=["api", "login"])
```

### Custom Output Path

Modify the `generate_filename()` function in the corresponding version's `monitor.py` to customize the file output location.

---

## ❓ FAQ

### Q1: Why aren't any requests captured?
- Ensure the target website makes API calls (refresh page, click buttons, etc.)
- Check if the correct page is opened
- Confirm it's not a purely static page

### Q2: What if the program gets stuck?
- Make sure you have closed the browser window
- Check if there are popups blocking the closure

### Q3: What if the Excel file is too large?
- Reduce operation time to avoid capturing too much data
- Use keyword filtering to reduce irrelevant requests

### Q4: Chinese characters are garbled?
- Make sure to open Excel files with UTF-8 encoding
- In Excel, import via "Data → From Text" to correctly recognize Chinese

---

## 🔧 Troubleshooting

### Error: ModuleNotFoundError
```bash
# Reinstall dependencies
pip install -r requirements.txt
playwright install chromium
```

### Error: Browser fails to start
```bash
# Reinstall browser drivers
playwright install chromium
```

### Error: Permission denied
- Ensure you have write permissions for the `recordings/` directory
- Try running the program as administrator

---

## ⚖️ Legal Disclaimer

**Important Notice**: This tool is for lawful use only.

### ✅ Permitted Uses
- Development, testing, and debugging of your own web applications
- Analyzing publicly available API structures and call patterns
- Security research on systems you own or have explicit authorization to test
- Learning about HTTP protocols and network request mechanics

### ❌ Prohibited Uses
- Unauthorized interception, monitoring, or analysis of other parties' network traffic
- Accessing systems, resources, or data without explicit authorization
- Collecting login credentials, personal privacy information, or trade secrets
- Any activities that violate local laws and regulations

### ⚠️ Risk Warning
- Some websites and APIs explicitly prohibit automated traffic interception in their Terms of Service
- Unauthorized network monitoring is illegal in many jurisdictions
- By using this tool, you agree to assume all risks and responsibilities

**Analogy**: This tool's functionality is similar to Chrome DevTools Network Panel, Burp Suite, Fiddler, and other standard development debugging tools. Like those tools, this software must be used within authorized boundaries.

---

**© 2024 - Use Responsibly**

---

## 📞 Technical Support

If you encounter issues, please check:
1. Python version is >= 3.8
2. All dependencies are correctly installed
3. Browser drivers are fully installed
4. Network connection is working

---

## 📝 Version History

### v1.0 (2026-04-23)
- ✅ Implemented basic traffic monitoring functionality
- ✅ Added interactive URL input support
- ✅ Auto-generated Excel reports
- ✅ Optimized browser close detection
- ✅ Added complete Chinese and English bilingual support

---

## 📜 License

This tool is open source under the MIT License.

---

**Created**: 2026-04-23
**Version**: v1.0
