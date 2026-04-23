"""
网络流量监控工具 - 主入口

提供网络流量监控工具的命令行界面。处理用户输入、URL 验证，
并启动监控过程。

作者: 网络流量监控工具 v1.0
日期: 2026-04-23
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.monitor_core_zh import TrafficMonitor
import os
from datetime import datetime
import re


def generate_filename(url):
    """
    根据 URL 和当前时间戳生成文件名。
    
    从 URL 中提取域名，并结合时间戳创建一个唯一的、描述性的录制文件名。
    
    参数:
        url (str): 要提取域名的 URL
        
    返回:
        str: 输出文件的完整路径
    """
    try:
        # 解析 URL 以提取域名
        from urllib.parse import urlparse
        parsed = urlparse(url)
        
        # 提取域名并清理（替换冒号和点）
        domain = parsed.netloc.replace(':', '_').replace('.', '_')
        
        # 生成时间戳，格式：YYYYMMDD_HHMMSS
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 构建文件名：域名_时间戳.xlsx
        filename = f"{domain}_{timestamp}.xlsx"
    except:
        # 如果 URL 解析失败则使用备用方案
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"recording_{timestamp}.xlsx"
    
    # 在项目目录中创建输出目录路径
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings")
    return os.path.join(output_dir, filename)


def validate_url(url):
    """
    验证 URL 的格式。
    
    检查提供的字符串是否是具有正确协议（http:// 或 https://）
    和网络位置的合法 URL。
    
    参数:
        url (str): 要验证的 URL 字符串
        
    返回:
        bool: 如果 URL 有效则返回 True，否则返回 False
    """
    # 检查 URL 是否为空
    if not url:
        return False
    
    # 如果没有提供协议，自动添加 https://
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        # 解析并验证 URL 组件
        from urllib.parse import urlparse
        result = urlparse(url)
        
        # 有效的 URL 必须同时具有协议和网络位置（域名）
        return all([result.scheme, result.netloc])
    except:
        return False


def main():
    """
    网络流量监控工具的主入口点。
    
    显示欢迎横幅，提示用户输入 URL，验证输入，然后启动流量监控过程。
    """
    # 显示欢迎横幅
    print("="*60)
    print("        网络流量监控工具 v1.0")
    print("="*60)
    print()
    
    # 提示用户输入 URL
    url = input("请输入要监控的网站URL: ").strip()
    
    # 验证 URL 不为空
    if not url:
        print("错误：URL不能为空！")
        return
    
    # 验证 URL 格式
    if not validate_url(url):
        # 如果它以 http/https 开头但验证失败，则为无效
        if url.startswith(('http://', 'https://')):
            print("错误：无效的URL格式！")
            return
        # 尝试添加 https:// 前缀
        url = 'https://' + url
        if not validate_url(url):
            print("错误：无效的URL格式！")
            return
    
    # 根据 URL 和时间戳生成输出文件名
    output_file = generate_filename(url)
    
    # 显示配置
    print()
    print(f"目标网站: {url}")
    print(f"输出文件: {output_file}")
    print()
    print("按回车后将在浏览器中打开该页面并开始监控...")
    print("(关闭浏览器后自动保存数据)")
    print()
    input()
    
    # 启动监控
    print("\n" + "="*60)
    print("启动监控中...")
    print("="*60 + "\n")
    
    # 创建 TrafficMonitor 实例并开始监控
    monitor = TrafficMonitor(url, output_file)
    monitor.start()
    
    # 显示完成消息
    print("\n" + "="*60)
    print("监控完成！")
    print("="*60)
    print(f"\n✅ 录制数据已保存至:")
    print(f"   {os.path.abspath(output_file)}")
    print()


if __name__ == "__main__":
    """
    入口点检查
    
    确保 main() 函数仅在脚本直接运行时调用（而不是作为模块导入时）。
    """
    main()
