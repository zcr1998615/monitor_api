"""
网络流量监控工具 - 主入口

提供网络流量监控工具的命令行界面。支持交互式模式和命令行参数模式。
处理用户输入、URL 验证，并启动监控过程。

作者: 网络流量监控工具 v1.0
日期: 2026-04-23
"""

import sys
import os
import argparse

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.monitor_core_zh import TrafficMonitor, compare_recordings
from datetime import datetime


def generate_filename(url):
    """
    根据 URL 和当前时间戳生成文件名。

    参数:
        url (str): 要提取域名的 URL

    返回:
        str: 输出文件的完整路径
    """
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.replace(':', '_').replace('.', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{domain}_{timestamp}.xlsx"
    except Exception:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"recording_{timestamp}.xlsx"

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings")
    return os.path.join(output_dir, filename)


def validate_url(url):
    """
    验证 URL 的格式。

    参数:
        url (str): 要验证的 URL 字符串

    返回:
        bool: 如果 URL 有效则返回 True，否则返回 False
    """
    if not url:
        return False
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def main():
    """
    网络流量监控工具的主入口点。

    支持两种模式:
    1. 交互式模式 (无参数): 提示用户输入 URL
    2. 命令行模式 (带参数): 直接指定 URL 和过滤选项
    """
    parser = argparse.ArgumentParser(
        description="网络流量监控工具 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python monitor.py                                      交互式模式
  python monitor.py https://example.com                  直接指定URL
  python monitor.py https://example.com -f api login     关键词过滤
  python monitor.py https://example.com -m POST PUT      只捕获POST和PUT
  python monitor.py https://example.com -s fail          只看失败请求
  python monitor.py https://example.com -e cdn.example   排除CDN域名
  python monitor.py https://example.com -r "/api/v[0-9]" URL正则匹配
  python monitor.py https://example.com --curl --docs    生成cURL和接口文档
  python monitor.py https://example.com --append -o r.xlsx  追加到已有文件
  python monitor.py --compare file1.xlsx file2.xlsx      对比两次录制
        """
    )
    parser.add_argument("url", nargs="?", help="要监控的网站URL")
    parser.add_argument("-f", "--filter", nargs="*", help="关键词过滤 (包含任一关键词的请求)")
    parser.add_argument("-e", "--exclude", nargs="*", help="排除的域名 (如 CDN)")
    parser.add_argument("-m", "--method", nargs="*", help="只捕获指定HTTP方法 (如 GET POST)")
    parser.add_argument("-s", "--status", help="状态码过滤 (fail/2xx/4xx/5xx/具体码)")
    parser.add_argument("-r", "--regex", help="URL正则匹配")
    parser.add_argument("-o", "--output", help="自定义输出文件路径")
    parser.add_argument("--append", action="store_true", help="追加模式 (写入已有Excel的新sheet)")
    parser.add_argument("--curl", action="store_true", help="生成cURL命令文件")
    parser.add_argument("--docs", action="store_true", help="生成接口文档")
    parser.add_argument("--compare", nargs=2, metavar=("FILE1", "FILE2"),
                        help="对比两次录制文件")

    args = parser.parse_args()

    # 对比模式
    if args.compare:
        output = args.output or os.path.splitext(args.compare[0])[0] + "_compare.md"
        compare_recordings(args.compare[0], args.compare[1], output)
        return

    # 获取 URL
    if args.url:
        url = args.url
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        if not validate_url(url):
            print("错误：无效的URL格式！")
            return
    else:
        # 交互式模式
        print("="*60)
        print("        网络流量监控工具 v1.0")
        print("="*60)
        print()
        url = input("请输入要监控的网站URL: ").strip()
        if not url:
            print("错误：URL不能为空！")
            return
        if not validate_url(url):
            if url.startswith(('http://', 'https://')):
                print("错误：无效的URL格式！")
                return
            url = 'https://' + url
            if not validate_url(url):
                print("错误：无效的URL格式！")
                return

    output_file = args.output or generate_filename(url)

    # 显示配置
    print()
    print(f"目标网站: {url}")
    print(f"输出文件: {output_file}")
    if args.filter:
        print(f"关键词过滤: {', '.join(args.filter)}")
    if args.exclude:
        print(f"排除域名: {', '.join(args.exclude)}")
    if args.method:
        print(f"HTTP方法: {', '.join(args.method)}")
    if args.status:
        print(f"状态过滤: {args.status}")
    if args.regex:
        print(f"URL正则: {args.regex}")
    if args.append:
        print(f"追加模式: 开启")
    print()

    # 交互式模式下等待用户确认
    if not args.url:
        print("按回车后将在浏览器中打开该页面并开始监控...")
        print("(关闭浏览器后自动保存数据)")
        print()
        print("提示: 使用命令行参数可启用更多功能，运行 python monitor.py -h 查看帮助")
        print()
        input()

    print("\n" + "="*60)
    print("启动监控中...")
    print("="*60 + "\n")

    monitor = TrafficMonitor(
        url, output_file,
        filter_keywords=args.filter,
        exclude_domains=args.exclude,
        method_filter=args.method,
        status_filter=args.status,
        url_pattern=args.regex,
        append_mode=args.append,
        generate_curl=args.curl,
        generate_docs=args.docs
    )
    monitor.start()

    print("\n" + "="*60)
    print("监控完成！")
    print("="*60)


if __name__ == "__main__":
    main()
