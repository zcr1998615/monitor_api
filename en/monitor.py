"""
Network Traffic Monitor - Main Entry Point

Provides the command-line interface for the Network Traffic Monitor.
Supports both interactive mode and CLI argument mode.
Handles user input, URL validation, and launches the monitoring process.

Author: Network Traffic Monitor v1.0
Date: 2026-04-23
"""

import sys
import os
import argparse

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.monitor_core_en import TrafficMonitor, compare_recordings
from datetime import datetime


def generate_filename(url):
    """
    Generate a filename based on the URL and current timestamp.

    Args:
        url (str): The URL to extract the domain from

    Returns:
        str: The full path to the output file
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
    Validate the format of a URL.

    Args:
        url (str): The URL string to validate

    Returns:
        bool: True if the URL is valid, False otherwise
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
    Main entry point for the Network Traffic Monitor.

    Supports two modes:
    1. Interactive mode (no arguments): prompts user for URL
    2. CLI mode (with arguments): specify URL and filter options directly
    """
    parser = argparse.ArgumentParser(
        description="Network Traffic Monitor v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python monitor.py                                      Interactive mode
  python monitor.py https://example.com                  Specify URL directly
  python monitor.py https://example.com -f api login     Keyword filter
  python monitor.py https://example.com -m POST PUT      Only capture POST and PUT
  python monitor.py https://example.com -s fail          Only failed requests
  python monitor.py https://example.com -e cdn.example   Exclude CDN domain
  python monitor.py https://example.com -r "/api/v[0-9]" URL regex match
  python monitor.py https://example.com --curl --docs    Generate cURL and API docs
  python monitor.py https://example.com --append -o r.xlsx  Append to existing file
  python monitor.py --compare file1.xlsx file2.xlsx      Compare two recordings
        """
    )
    parser.add_argument("url", nargs="?", help="Website URL to monitor")
    parser.add_argument("-f", "--filter", nargs="*", help="Keyword filter (requests containing any keyword)")
    parser.add_argument("-e", "--exclude", nargs="*", help="Domains to exclude (e.g. CDN)")
    parser.add_argument("-m", "--method", nargs="*", help="Only capture specified HTTP methods (e.g. GET POST)")
    parser.add_argument("-s", "--status", help="Status code filter (fail/2xx/4xx/5xx/specific code)")
    parser.add_argument("-r", "--regex", help="URL regex match")
    parser.add_argument("-o", "--output", help="Custom output file path")
    parser.add_argument("--append", action="store_true", help="Append mode (write to new sheet in existing Excel)")
    parser.add_argument("--curl", action="store_true", help="Generate cURL commands file")
    parser.add_argument("--docs", action="store_true", help="Generate API documentation")
    parser.add_argument("--compare", nargs=2, metavar=("FILE1", "FILE2"),
                        help="Compare two recording files")

    args = parser.parse_args()

    # Compare mode
    if args.compare:
        output = args.output or os.path.splitext(args.compare[0])[0] + "_compare.md"
        compare_recordings(args.compare[0], args.compare[1], output)
        return

    # Get URL
    if args.url:
        url = args.url
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        if not validate_url(url):
            print("Error: Invalid URL format!")
            return
    else:
        # Interactive mode
        print("="*60)
        print("        Network Traffic Monitor v1.0")
        print("="*60)
        print()
        url = input("Enter the website URL to monitor: ").strip()
        if not url:
            print("Error: URL cannot be empty!")
            return
        if not validate_url(url):
            if url.startswith(('http://', 'https://')):
                print("Error: Invalid URL format!")
                return
            url = 'https://' + url
            if not validate_url(url):
                print("Error: Invalid URL format!")
                return

    output_file = args.output or generate_filename(url)

    # Display configuration
    print()
    print(f"Target website: {url}")
    print(f"Output file: {output_file}")
    if args.filter:
        print(f"Keyword filter: {', '.join(args.filter)}")
    if args.exclude:
        print(f"Excluded domains: {', '.join(args.exclude)}")
    if args.method:
        print(f"HTTP methods: {', '.join(args.method)}")
    if args.status:
        print(f"Status filter: {args.status}")
    if args.regex:
        print(f"URL regex: {args.regex}")
    if args.append:
        print(f"Append mode: enabled")
    print()

    # In interactive mode, wait for user confirmation
    if not args.url:
        print("Press Enter to open the page in browser and start monitoring...")
        print("(Data will be automatically saved after closing the browser)")
        print()
        print("Tip: Use CLI arguments for more features, run python monitor.py -h for help")
        print()
        input()

    print("\n" + "="*60)
    print("Starting monitoring...")
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
    print("Monitoring complete!")
    print("="*60)


if __name__ == "__main__":
    main()
