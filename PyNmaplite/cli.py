import argparse
from .scanner import run_tcp_scan

def main():
    parser = argparse.ArgumentParser(description="PyNmapLite - Python Port Scanner")
    parser.add_argument("--target", required=True, help="Target IP or hostname")
    parser.add_argument("--start", type=int, default=1, help="Start port(default 1)")
    parser.add_argument("--end", type=int, default=1024, help = "End port (default 1024)")

    args = parser.parse_args()

    print(f"\n[+] Scanning {args.target}  from port {args.start} to {args.end}...")
    open_ports = run_tcp_scan(args.target, args.start, args.end)

    if open_ports:
        print("\n[+] Open ports found:")
        for port in open_ports:
            print(f"  -Port {port}")
    else:
        print("\n[-] No open Ports Found.")