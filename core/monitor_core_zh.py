"""
网络流量监控工具 - 核心模块

本模块提供使用 Playwright 从 Web 浏览器捕获和记录网络流量（API 调用）
的核心功能。

作者: 网络流量监控工具 v1.0
日期: 2026-04-23
"""

import json
import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import os


class TrafficMonitor:
    """
    流量监控类
    
    负责从浏览器实例拦截和记录网络请求及响应。使用 Playwright
    的浏览器自动化功能来捕获所有 fetch 和 xhr 请求。
    
    属性:
        target_url (str): 要监控的目标 URL
        output_file (str): 保存 Excel 输出文件的路径
        filter_keywords (list): 用于过滤请求的关键词列表
        records (list): 用于存储捕获流量记录的列表
    """
    
    def __init__(self, target_url, output_file, filter_keywords=None):
        """
        初始化 TrafficMonitor 实例。
        
        参数:
            target_url (str): 要监控的目标 URL
            output_file (str): 保存 Excel 输出文件的路径
            filter_keywords (list, 可选): 用于过滤请求的关键词列表。
                只有包含这些关键词的请求会被捕获。
                默认为 None（捕获所有请求）。
        """
        self.target_url = target_url
        self.output_file = output_file
        self.filter_keywords = filter_keywords or []
        self.records = []

    def handle_request(self, request):
        """
        处理发出的 HTTP 请求。
        
        此回调在浏览器发出的每个网络请求时触发。它过滤请求以仅捕获 fetch 和 xhr 
        类型（API 调用），并可选择性地按关键词过滤。
        
        参数:
            request: Playwright 的请求对象
            
        注意:
            - 只捕获 'fetch' 和 'xhr' 资源类型（API 调用）
            - 如果设置了 filter_keywords，则只捕获包含这些关键词的请求
            - 记录暂时附加到请求对象上，以便后续响应关联
        """
        # 仅关注 fetch 和 xhr（接口请求）
        if request.resource_type in ["fetch", "xhr"]:
            # 如果提供了关键词过滤，则进行过滤
            if self.filter_keywords:
                if not any(kw in request.url for kw in self.filter_keywords):
                    return
            
            # 记录请求基础信息
            record = {
                "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "方法": request.method,
                "URL": request.url,
                "请求头": json.dumps(request.headers, indent=2, ensure_ascii=False),
                "载荷": request.post_data or "",
                "状态": "待处理",
                "响应头": "",
                "响应体": ""
            }
            # 将记录临时绑定到请求对象上，方便响应回调关联
            request._traffic_record = record

    def handle_response(self, response):
        """
        处理收到的 HTTP 响应。
        
        此回调在浏览器收到的每个网络响应时触发。它将响应与相应的请求关联并更新记录。
        
        参数:
            response: Playwright 的响应对象
            
        注意:
            - 只处理有对应请求记录的响应
            - 捕获状态码、响应头和响应体
            - 二进制内容（图片、字体）标记为 "[二进制内容]"
        """
        request = response.request
        
        # 检查此响应是否有对应的请求记录
        if hasattr(request, "_traffic_record"):
            record = request._traffic_record
            
            # 更新记录的响应信息
            record["状态"] = response.status
            record["响应头"] = json.dumps(response.headers, indent=2, ensure_ascii=False)
            
            try:
                # 尝试获取响应体
                content_type = response.headers.get("content-type", "").lower()
                
                # 将二进制内容（图片、字体）标记为 "[二进制内容]"
                if "image" in content_type or "font" in content_type:
                    record["响应体"] = "[二进制内容]"
                else:
                    # 获取文本内容
                    record["响应体"] = response.text()
            except Exception as e:
                # 处理读取响应体时的错误
                record["响应体"] = f"[读取响应错误: {str(e)}]"
            
            # 将完成的记录添加到记录列表
            self.records.append(record)
            
            # 打印捕获的请求到控制台
            print(f"[{record['方法']}] {record['URL']} -> {record['状态']}")

    def start(self):
        """
        启动流量监控过程。
        
        启动无痕模式的 Chromium 浏览器，导航到目标 URL，并开始捕获网络流量。
        监控持续到用户关闭浏览器窗口。
        
        注意:
            - 浏览器以非无头模式运行（可见窗口）
            - 使用无痕模式以保护隐私
            - 关闭浏览器窗口时监控停止
        """
        with sync_playwright() as p:
            # 启动无痕模式浏览器
            print("正在启动浏览器 (无痕模式)...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            # 注册请求和响应拦截的事件处理程序
            page.on("request", self.handle_request)
            page.on("response", self.handle_response)

            # 导航到目标 URL
            print(f"正在打开网页: {self.target_url}")
            page.goto(self.target_url)
            
            # 显示用户说明
            print("\n" + "="*50)
            print("监控已就绪！")
            print("请在该浏览器窗口中进行您的手工操作。")
            print("完成录制后，只需【直接关闭浏览器窗口】即可。")
            print("="*50 + "\n")
            
            # 等待浏览器窗口关闭
            page.wait_for_event('close', timeout=0)
            
            # 浏览器已关闭，正在保存数据
            print("\n浏览器已关闭，正在保存数据...")
            self.save_to_excel()

    def save_to_excel(self):
        """
        将捕获的流量数据保存到 Excel 文件。
        
        将捕获的记录转换为 pandas DataFrame，按时间戳排序，并导出为 Excel 格式。
        
        注意:
            - 记录按时间排序
            - 如果输出目录不存在则创建
            - Excel 文件保存到指定的 output_file 路径
        """
        # 检查是否有捕获的记录
        if not self.records:
            print("未捕获到任何符合条件的接口请求。")
            return
        
        # 创建 DataFrame 并按时间排序
        df = pd.DataFrame(self.records)
        df.sort_values(by="时间", inplace=True)
        
        # 确保输出目录存在
        output_dir = os.path.dirname(os.path.abspath(self.output_file))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 保存到 Excel 文件
        df.to_excel(self.output_file, index=False)
        print(f"成功！录制数据已保存至:")
        print(f"   {os.path.abspath(self.output_file)}")
