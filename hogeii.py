#!/usr/bin/env python3
"""
Hogeii Ultimate - Security Automation Framework
Main entry point for the hogeii security automation tool
"""

import argparse
import sys
from datetime import datetime
from sentinel import SentinelMonitor
from ugo_auto import UGOAuto


class HogeiiCore:
    """Main Hogeii automation engine"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.sentinel = SentinelMonitor(verbose=verbose)
        self.ugo = UGOAuto(verbose=verbose)
        self.start_time = datetime.now()

    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def run_scan(self, target=None):
        """Run security scan"""
        self.log("Starting Hogeii security scan...")

        # Start sentinel monitoring
        self.sentinel.start_monitoring()

        # Run UGO auto checks
        if target:
            self.log(f"Scanning target: {target}")
            self.ugo.scan_permissions(target)
        else:
            self.log("Running system-wide UGO auto scan...")
            self.ugo.auto_fix_permissions()

        self.log("Scan complete")

    def monitor(self):
        """Start continuous monitoring"""
        self.log("Starting continuous monitoring mode...")
        self.sentinel.continuous_monitor()

    def report(self):
        """Generate security report"""
        self.log("Generating security report...")
        self.sentinel.generate_report()
        self.ugo.generate_report()


def main():
    parser = argparse.ArgumentParser(
        description="Hogeii Ultimate - Security Automation Framework"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "-s", "--scan",
        metavar="TARGET",
        help="Run security scan on target"
    )
    parser.add_argument(
        "-m", "--monitor",
        action="store_true",
        help="Start continuous monitoring"
    )
    parser.add_argument(
        "-r", "--report",
        action="store_true",
        help="Generate security report"
    )
    parser.add_argument(
        "--ugo-auto",
        action="store_true",
        help="Run UGO auto permission fixes"
    )

    args = parser.parse_args()

    # Initialize Hogeii
    hogeii = HogeiiCore(verbose=args.verbose)

    if args.scan:
        hogeii.run_scan(target=args.scan)
    elif args.monitor:
        hogeii.monitor()
    elif args.report:
        hogeii.report()
    elif args.ugo_auto:
        hogeii.ugo.auto_fix_permissions()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
