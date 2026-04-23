"""
Network Traffic Monitor - Main Entry Point

Provides the command-line interface for the Network Traffic Monitor.
Handles user input, URL validation, and launches the monitoring process.

Author: Network Traffic Monitor v1.0
Date: 2026-04-23
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.monitor_core_en import TrafficMonitor
import os
from datetime import datetime
import re


def generate_filename(url):
    """
    Generate a filename based on the URL and current timestamp.
    
    Extracts the domain from the URL and combines it with a timestamp
    to create a unique, descriptive filename for the recording.
    
    Args:
        url (str): The URL to extract the domain from
        
    Returns:
        str: The full path to the output file
    """
    try:
        # Parse the URL to extract the domain
        from urllib.parse import urlparse
        parsed = urlparse(url)
        
        # Extract domain and clean it (replace colons and dots)
        domain = parsed.netloc.replace(':', '_').replace('.', '_')
        
        # Generate timestamp in format: YYYYMMDD_HHMMSS
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Construct filename: domain_timestamp.xlsx
        filename = f"{domain}_{timestamp}.xlsx"
    except:
        # Fallback if URL parsing fails
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"recording_{timestamp}.xlsx"
    
    # Create output directory path in the project directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings")
    return os.path.join(output_dir, filename)


def validate_url(url):
    """
    Validate the format of a URL.
    
    Checks if the provided string is a valid URL with proper
    scheme (http:// or https://) and network location.
    
    Args:
        url (str): The URL string to validate
        
    Returns:
        bool: True if the URL is valid, False otherwise
    """
    # Check if URL is empty
    if not url:
        return False
    
    # Auto-add https:// if no scheme is provided
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        # Parse and validate URL components
        from urllib.parse import urlparse
        result = urlparse(url)
        
        # Valid URL must have both scheme and netloc (domain)
        return all([result.scheme, result.netloc])
    except:
        return False


def main():
    """
    Main entry point for the Network Traffic Monitor.
    
    Displays a welcome banner, prompts the user for a URL,
    validates the input, and launches the traffic monitoring process.
    """
    # Display welcome banner
    print("="*60)
    print("        Network Traffic Monitor v1.0")
    print("="*60)
    print()
    
    # Prompt user for URL
    url = input("Enter the website URL to monitor: ").strip()
    
    # Validate that URL is not empty
    if not url:
        print("Error: URL cannot be empty!")
        return
    
    # Validate URL format
    if not validate_url(url):
        # If it starts with http/https but validation failed, it's invalid
        if url.startswith(('http://', 'https://')):
            print("Error: Invalid URL format!")
            return
        # Try adding https:// prefix
        url = 'https://' + url
        if not validate_url(url):
            print("Error: Invalid URL format!")
            return
    
    # Generate output filename based on URL and timestamp
    output_file = generate_filename(url)
    
    # Display configuration
    print()
    print(f"Target website: {url}")
    print(f"Output file: {output_file}")
    print()
    print("Press Enter to open the page in browser and start monitoring...")
    print("(Data will be automatically saved after closing the browser)")
    print()
    input()
    
    # Launch monitoring
    print("\n" + "="*60)
    print("Starting monitoring...")
    print("="*60 + "\n")
    
    # Create TrafficMonitor instance and start monitoring
    monitor = TrafficMonitor(url, output_file)
    monitor.start()
    
    # Display completion message
    print("\n" + "="*60)
    print("Monitoring complete!")
    print("="*60)
    print(f"\n✅ Recording data saved to:")
    print(f"   {os.path.abspath(output_file)}")
    print()


if __name__ == "__main__":
    """
    Entry point check
    
    Ensures the main() function is only called when the script
    is run directly (not when imported as a module).
    """
    main()
