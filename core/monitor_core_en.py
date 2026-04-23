"""
Network Traffic Monitor - Core Module

This module provides the core functionality for capturing and recording
network traffic (API calls) from web browsers using Playwright.

Author: Network Traffic Monitor v1.0
Date: 2026-04-23
"""

import json
import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import os


class TrafficMonitor:
    """
    Traffic Monitor Class
    
    Responsible for intercepting and recording network requests and responses
    from a browser instance. Uses Playwright's browser automation capabilities
    to capture all fetch and xhr requests.
    
    Attributes:
        target_url (str): The URL to monitor
        output_file (str): Path to save the Excel output file
        filter_keywords (list): Keywords to filter requests
        records (list): List to store captured traffic records
    """
    
    def __init__(self, target_url, output_file, filter_keywords=None):
        """
        Initialize the TrafficMonitor instance.
        
        Args:
            target_url (str): The URL to monitor
            output_file (str): Path to save the Excel output file
            filter_keywords (list, optional): Keywords to filter requests.
                Only requests containing these keywords will be captured.
                Defaults to None (capture all requests).
        """
        self.target_url = target_url
        self.output_file = output_file
        self.filter_keywords = filter_keywords or []
        self.records = []

    def handle_request(self, request):
        """
        Handle outgoing HTTP requests.
        
        This callback is triggered for every network request made by the browser.
        It filters requests to only capture fetch and xhr types (API calls),
        and optionally filters by keywords.
        
        Args:
            request: Playwright's request object
            
        Note:
            - Only captures 'fetch' and 'xhr' resource types (API calls)
            - If filter_keywords is set, only captures requests containing those keywords
            - Records are temporarily attached to the request object for later response association
        """
        # Only focus on fetch and xhr (API requests)
        if request.resource_type in ["fetch", "xhr"]:
            # If keyword filtering is provided, apply the filter
            if self.filter_keywords:
                if not any(kw in request.url for kw in self.filter_keywords):
                    return
            
            # Record basic request information
            record = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "Method": request.method,
                "URL": request.url,
                "Request Headers": json.dumps(request.headers, indent=2, ensure_ascii=False),
                "Payload": request.post_data or "",
                "Status": "Pending",
                "Response Headers": "",
                "Response Body": ""
            }
            # Attach the record to the request object for later response callback to find
            request._traffic_record = record

    def handle_response(self, response):
        """
        Handle incoming HTTP responses.
        
        This callback is triggered for every network response received by the browser.
        It associates the response with the corresponding request and updates the record.
        
        Args:
            response: Playwright's response object
            
        Note:
            - Only processes responses that have a corresponding request record
            - Captures status code, response headers, and response body
            - Binary content (images, fonts) is marked as "[Binary Content]"
        """
        request = response.request
        
        # Check if this response has a corresponding request record
        if hasattr(request, "_traffic_record"):
            record = request._traffic_record
            
            # Update the record with response information
            record["Status"] = response.status
            record["Response Headers"] = json.dumps(response.headers, indent=2, ensure_ascii=False)
            
            try:
                # Try to get the response body
                content_type = response.headers.get("content-type", "").lower()
                
                # Mark binary content (images, fonts) as "[Binary Content]"
                if "image" in content_type or "font" in content_type:
                    record["Response Body"] = "[Binary Content]"
                else:
                    # Get text content
                    record["Response Body"] = response.text()
            except Exception as e:
                # Handle errors when reading response body
                record["Response Body"] = f"[Error reading response: {str(e)}]"
            
            # Add the completed record to the records list
            self.records.append(record)
            
            # Print the captured request to console
            print(f"[{record['Method']}] {record['URL']} -> {record['Status']}")

    def start(self):
        """
        Start the traffic monitoring process.
        
        Launches a Chromium browser in incognito mode, navigates to the target URL,
        and begins capturing network traffic. The monitoring continues until the
        user closes the browser window.
        
        Note:
            - Browser runs in non-headless mode (visible window)
            - Incognito mode is used for privacy
            - Monitoring stops when browser window is closed
        """
        with sync_playwright() as p:
            # Launch browser in incognito mode
            print("Launching browser (incognito mode)...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            # Register event handlers for request and response interception
            page.on("request", self.handle_request)
            page.on("response", self.handle_response)

            # Navigate to the target URL
            print(f"Opening webpage: {self.target_url}")
            page.goto(self.target_url)
            
            # Display user instructions
            print("\n" + "="*50)
            print("Monitoring is ready!")
            print("Please perform your operations in the browser window.")
            print("After completing, simply CLOSE the browser window.")
            print("="*50 + "\n")
            
            # Wait for the browser window to be closed
            page.wait_for_event('close', timeout=0)
            
            # Browser has been closed, save the captured data
            print("\nBrowser closed, saving data...")
            self.save_to_excel()

    def save_to_excel(self):
        """
        Save the captured traffic data to an Excel file.
        
        Converts the captured records into a pandas DataFrame, sorts them by
        timestamp, and exports to Excel format.
        
        Note:
            - Records are sorted by time
            - Output directory is created if it doesn't exist
            - Excel file is saved with the specified output_file path
        """
        # Check if any records were captured
        if not self.records:
            print("No qualifying API requests were captured.")
            return
        
        # Create DataFrame and sort by time
        df = pd.DataFrame(self.records)
        df.sort_values(by="Time", inplace=True)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(os.path.abspath(self.output_file))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save to Excel file
        df.to_excel(self.output_file, index=False)
        print(f"Success! Recording data saved to:")
        print(f"   {os.path.abspath(self.output_file)}")
