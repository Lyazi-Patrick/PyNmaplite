import json
import csv
from typing import List, Dict

def save_to_json(results:List[Dict], filename:str = "results/scan_results.json") -> None:
    """
    results:List of dicts like [{"port":22, "banner": "SSH-..."}]
    """
    #ensure directory exists is left to user
    with open(filename, "w",encoding="utf-8") as f:
        json.dump(results,f,indent=4, ensure_ascii=False)
    print(f"[+] Results saved to {filename}")

def save_to_csv(results:List[Dict], filename:str = "results/scan_results.csv") -> None:
    """
    Save list-of-dicts results to CSV. Fields: port, banner
    """
    with open(filename,"w",newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["port","banner"])
        writer.writeheader()
        writer.writerows(results)
    print(f"[+] Results saved to {filename}")