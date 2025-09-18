import argparse
from .scanner import run_tcp_scan, grab_banner
from .utils import save_to_json, save_to_csv

def parse_args():
    parser = argparse.ArgumentParser(description="PyNmaplite - Lightweight port & service scanner")
    parser.add_argument("--target", required=True, help="Target IP or hostname")
    parser.add_argument("--start", type=int,default=1,help="start port (default 1)")
    parser.add_argument("--end", type=int, default=1024,help="End Port (default 1024)")
    parser.add_argument("--banners", action="store_true", help="Attempt to Grab service banners for open ports")
    parser.add_argument("--json", action="store_true", help="save results to JSON")
    parser.add_argument("--csv", action="store_true", help="Save results to CSV")
    return parser.parse_args()

def main():
    args = parse_args()
    target = args.target
    start_port = args.start
    end_port = args.end

    print(f"\n[+] Scanning {target} from port {start_port} to {end_port}...\n")
    open_ports = run_tcp_scan(target, start_port, end_port)

    if not open_ports:
        print("[-] No open ports found.")
        return
    
    results = []
    print("[+] Open ports found:")
    for port in open_ports:
        banner = grab_banner(target, port) if args.banners else "Unknown"
        print(f"-Port {port} | Banner:{banner}")

    #Save if requested
    if args.json:
        save_to_json(results)
    if args.csv:
        save_to_csv(results)
