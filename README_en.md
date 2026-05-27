# Network Traffic Monitor v2.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 📖 Project Introduction

This is a **Network Traffic Monitor Tool** built with Python and Playwright. It captures all network requests (API calls) in the browser and automatically saves them to Excel and HAR files for easy analysis and automated testing.

### Core Features

- 🎯 **Real-time Traffic Interception**: Monitor and record all fetch and xhr requests
- 📊 **Detailed Data Capture**: URL, Method, Headers, Payload, Response, Duration
- 🔒 **Privacy Protection**: Uses browser incognito mode
- 📁 **Multi-format Export**: Excel (styled) + HAR + cURL + API docs
- 🔍 **Powerful Filtering**: Keywords, domain exclusion, HTTP methods, status codes, regex
- 🗂️ **Multi-tab Support**: Automatically monitors all newly opened tabs
- 📈 **Real-time Stats**: Request count, success/fail, average duration shown live
- 🔄 **Recording Comparison**: Diff two recordings to detect API changes
- 🎨 **Interactive + CLI**: Supports both interactive and command-line argument modes
- 🌐 **Bilingual Support**: Complete Chinese and English versions

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Playwright**: Browser automation and network interception
- **Pandas / Openpyxl**: Excel file generation and styling
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

#### Method 1: Double-click to Launch (Recommended for beginners)

1. **Chinese Version**: Double-click `run_zh.bat`
2. **English Version**: Double-click `run_en.bat`
3. Enter the website URL you want to monitor in the command line
4. Press Enter, the browser will automatically open
5. Perform your manual operations in the browser (multi-tab supported)
6. **Close the browser** window
7. The program automatically saves data and displays the file path

#### Method 2: Command Line Launch (Recommended for advanced users)

```bash
# Basic usage - interactive mode
python en/monitor.py

# Specify URL directly
python en/monitor.py https://example.com

# Keyword filter - only capture requests containing "api" or "login"
python en/monitor.py https://example.com -f api login

# Only capture POST and PUT requests
python en/monitor.py https://example.com -m POST PUT

# Only show failed requests
python en/monitor.py https://example.com -s fail

# Exclude CDN domains
python en/monitor.py https://example.com -e cdn.example.com static.example.com

# URL regex matching
python en/monitor.py https://example.com -r "/api/v[0-9]+"

# Generate cURL commands and API docs
python en/monitor.py https://example.com --curl --docs

# Append to existing Excel file (new sheet)
python en/monitor.py https://example.com --append -o recordings/existing.xlsx

# Compare two recordings
python en/monitor.py --compare recordings/before.xlsx recordings/after.xlsx
```

#### View full parameter help

```bash
python en/monitor.py -h
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
│   ├── monitor.py                 # Chinese main program
│   └── recordings/                # Chinese recording data
│
├── en/                            # English version directory
│   ├── __init__.py
│   ├── monitor.py                 # English main program
│   └── recordings/                # English recording data
│
├── run_zh.bat                     # Chinese version launch script
├── run_en.bat                     # English version launch script
├── LICENSE                        # MIT License
├── requirements.txt               # Python dependencies
├── README_zh.md                   # Chinese documentation
└── README_en.md                   # This file
```

---

## 🎛️ CLI Arguments

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `url` | - | Website URL to monitor (optional, enters interactive mode if omitted) | `https://example.com` |
| `--filter` | `-f` | Keyword filter, captures requests containing any keyword | `-f api login` |
| `--exclude` | `-e` | Domains to exclude (CDN, analytics, etc.) | `-e cdn.example.com` |
| `--method` | `-m` | Only capture specified HTTP methods | `-m POST PUT DELETE` |
| `--status` | `-s` | Status code filter | `-s fail` / `-s 4xx` / `-s 200` |
| `--regex` | `-r` | URL regex matching | `-r "/api/v[0-9]+"` |
| `--output` | `-o` | Custom output file path | `-o output.xlsx` |
| `--append` | - | Append mode, write to new sheet in existing Excel | `--append -o existing.xlsx` |
| `--curl` | - | Generate cURL commands file | `--curl` |
| `--docs` | - | Generate API documentation (Markdown) | `--docs` |
| `--compare` | - | Compare two recording files | `--compare a.xlsx b.xlsx` |

### Status Code Filter Options

| Value | Description |
|-------|-------------|
| `fail` | Only capture 4xx and 5xx errors |
| `2xx` | Only capture successful requests |
| `4xx` | Only capture client errors |
| `5xx` | Only capture server errors |
| `200` | Only capture specific status code |

---

## 📋 Recording Data Description

### Excel Table Fields

| Field | Description |
|-------|-------------|
| Time | Request timestamp (millisecond precision) |
| Method | HTTP method (GET/POST/PUT/DELETE, etc.) |
| URL | Complete API endpoint (clickable hyperlink) |
| Request Headers | Request header information (JSON format) |
| Payload | Request body content (POST parameters, etc.) |
| Status | HTTP status code (color-coded: 2xx green / 4xx yellow / 5xx red) |
| Duration(ms) | Request-to-response duration in milliseconds |
| Response Headers | Response header information (JSON format) |
| Response Body | Response content (JSON format) |

### Excel Styling Features

- Frozen header row (stays visible when scrolling)
- Blue header with white bold text
- Auto-adjusted column widths
- Status code color coding (2xx green / 4xx yellow / 5xx red)
- Clickable URL hyperlinks

### Output Files

Each recording generates the following files (e.g. `example_com_20260527_143052`):

| File | Description | When Generated |
|------|-------------|----------------|
| `*.xlsx` | Excel recording data | Always |
| `*.har` | HAR format (importable to Postman/Chrome DevTools/Charles) | Always |
| `*_curl.sh` | cURL command collection (executable in terminal) | With `--curl` |
| `*_api_docs.md` | API documentation (deduplicated by domain+path) | With `--docs` |
| `*_compare.md` | Comparison report | With `--compare` |

---

## 🎯 Use Cases

### 1. API Analysis
- Understand all API calls made by a website
- Analyze API parameter and response structures
- Check API performance via the Duration field

### 2. API Testing Preparation
- Quickly collect test data
- Auto-generate API documentation (`--docs`)
- Export cURL commands for direct reuse (`--curl`)
- Import HAR files into Postman to batch-create requests

### 3. Regression Testing
- Record baseline API data
- Record again after changes
- Use `--compare` to diff and detect API changes

### 4. Problem Troubleshooting
- Record complete request flow when issues occur
- Use `-s fail` to focus on failed requests only
- Save detailed error information

---

## ⚙️ Advanced Usage

### Combined Filtering

```bash
# Only POST requests containing "api", failed only, excluding CDN
python en/monitor.py https://example.com \
  -f api \
  -m POST \
  -s fail \
  -e cdn.example.com
```

### Multi-session Recording

Record multiple sessions into the same Excel file as different sheets:

```bash
# First recording
python en/monitor.py https://example.com -o recordings/test_flow.xlsx

# Second recording (appends as new sheet)
python en/monitor.py https://example.com --append -o recordings/test_flow.xlsx
```

### Recording Comparison

```bash
# Compare two recordings, generate diff report
python en/monitor.py --compare recordings/v1.xlsx recordings/v2.xlsx

# Custom report output path
python en/monitor.py --compare recordings/v1.xlsx recordings/v2.xlsx -o report.md
```

Comparison report includes:
- New endpoints (in B but not in A)
- Removed endpoints (in A but not in B)
- Changed endpoints (status code changes, request body changes, response field additions/removals)

### Auto-generate API Documentation

```bash
python en/monitor.py https://example.com --docs
```

The generated Markdown documentation groups by domain, with each endpoint showing:
- HTTP method and path
- Status code and duration
- Request body sample (JSON format)
- Response body sample (JSON format, auto-truncated if too long)

### Generate cURL Commands

```bash
python en/monitor.py https://example.com --curl
```

Each request is converted to an executable cURL command for terminal replay and debugging.

---

## ❓ FAQ

### Q1: Why aren't any requests captured?
- Ensure the target website makes API calls (refresh page, click buttons, etc.)
- Check if the correct page is opened
- Confirm it's not a purely static page
- Check if filter conditions are too restrictive

### Q2: What if the program gets stuck?
- Make sure you have closed all browser tabs
- Check if there are popups blocking the closure

### Q3: What if the Excel file is too large?
- Reduce operation time to avoid capturing too much data
- Use `-f` keyword filter to reduce irrelevant requests
- Use `-e` to exclude CDN and static resource domains
- Use `-m` to capture only needed HTTP methods

### Q4: Chinese characters are garbled?
- Make sure to open Excel files with UTF-8 encoding
- In Excel, import via "Data → From Text" to correctly recognize Chinese

### Q5: Requests from new tabs aren't captured?
- v2.0 supports multi-tab monitoring out of the box
- All tabs opened within the same browser window are automatically monitored

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
5. Run `python en/monitor.py -h` for parameter help

---

## 📝 Version History

### v2.0 (2026-05-27)
- ✅ Excel styling: frozen header, auto column width, status code coloring, URL hyperlinks
- ✅ Request duration tracking (millisecond precision)
- ✅ Real-time stats panel: request count, success/fail, average duration
- ✅ HAR format export (importable to Postman/Chrome DevTools/Charles)
- ✅ Enhanced filtering: domain exclusion, HTTP methods, status codes, regex matching
- ✅ Multi-tab support: automatically monitors all newly opened tabs
- ✅ Multi-session recording: append mode writes to new sheets in existing Excel
- ✅ CLI arguments (argparse): supports scripting and CI integration
- ✅ Auto-generate API documentation (Markdown format)
- ✅ cURL command generation
- ✅ Recording comparison: diff two recordings to detect new/removed/changed endpoints

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
**Last Updated**: 2026-05-27
**Version**: v2.0
