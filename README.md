PyNmapLite-a lightweight, educational port service scanner written in python.The repo is meant for learning a small lab/ network auditing use-cases. it is not a replacement for Nmap, but is useful for building practical skills in sockets, threading, banner grabbing and result export.

## Project Goals
Teach core networking fundamentals, through code (TCP/UDP,ports,sockets).
Provide a portable, easy-to-read Python codebase you can extend.
Produce portfolio-ready deliverables (JSON/CSV results,README, tests).

# Folder Structure

## Features
Threaded TCP port scanning for speed.
Optional bannner grabbing for common  services (HTTP,SSH, etc).
Export scan output to JSON and CSV for further analysis.
Clean CLI interface using argparse.
Small readable codebase intended for learning and extension.

## Requirements
Python 3.8+ recommended


## Design notes(How it works)
The scanner attempts a TCP connnect() to each port in the requested range. if connect() succeeds, the port is considered open.
The scanner uses Python Threading to scan many ports concurrently to improve speed.
Banner grabbing attempts to read bytes from the newly opened socket. For Http(port 80) the scanner first sends a minimal GET request so the server replies with headers.

## Extending the project
Ideas for improvement you can implement:
UDP  scanning (careful: UDP scanning is noisy and different in bbehavior).
More intelligent service detection (send protocol-specific probes for FTP, SMTP, etc).
Timeout tuning and rate-limiting to avoid network congestion.
Add unit tests for parsing and saving functions.
Integrate a simple Flask dashboard to visualize results.

## Contributing 
1. Fork the repo
2. Create a feature branch (git checkout -b feat/your-feature)
3. Commit and push changes
4. Open a PR and Provide a description of your changes

# License
This repository is released under MIT license 

# Safety & Legal
Do not use this tool for unauthorised scanning. Unauthorised scanning may be illegal or violate acceptable use policies. Always obtain explicit permission before testing systems you do not own.

# Contact/Credit
Created as an educational project to learn practical cybersecurity tooling with python