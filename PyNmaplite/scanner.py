import socket
import ssl
import threading 
from typing import List

class PortScanner:
    """
    Simple class wrapper if you want object-oriented scanning later.
    This  class currently stores target + range and can perform a quick a quick scan.
    """
    def __init__(self,target: str, start_port: int = 1, end_port: int = 1024):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
    
    def scan(self) -> dict:
        """
        Convenience method: run threaded scan and return dict {port:'open}.
        """
        open_ports = {}
        ports = run_tcp_scan(self.target, self.start_port, self.end_port)
        for p in ports:
            open_ports[p] = "open"
        return open_ports
    
lock = threading.Lock()    
    
def scan_tcp_port(target:str,port:int,open_ports:List[int]) -> None:
    """
    Worker to test a single TCP port using connect_ex (non-blocking error code)
    Appends open ports to the shared open_ports list.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((target,port))
        if result == 0:
            with lock: #prevent race conditions 
                open_ports.append(port)
        sock.close()
    except Exception:
        #ignore network errors for individual ports
        pass

def run_tcp_scan(target:str, start_port:int, end_port:int) -> List[int]:
    """
    Multi-threaded TCP scan returning a sorted list of open ports.
    """
    open_ports:List[int] = []
    threads:List[threading.Thread] = []

    lock = threading.Lock()
    for port in range(start_port, end_port+1):
        t = threading.Thread(target = scan_tcp_port, args = (target,port,open_ports))
        t.daemon = True
        threads.append(t)
        t.start()

    #wait for all threads
    for t in threads:
        t.join()
    return sorted(open_ports)

def grab_banner(target:str, port:int) -> str:
    """
    Try to identify the service by asking for a banner or sending a minimal probe for common protocols.
    Returns a short string, or "Unknown" on failure.
    """
    try:
        #Basic TCP socket first
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target, port))

        #HTTP (plain) -> send an HTTP GET so server responds with headers
        if port in (80, 8080):
            http_req = f"GET/HTTP/1.1\r\nHost:{target}\r\nUser-Agent: PyNmaplite\r\nConnection:close\r\n\r\n"
            sock.send(http_req.encode())
            data = sock.recv(2048).decode(errors="ignore").strip()
            sock.close()
            # return first header line or a truncated header
            lines = [l for l in data.splitlines() if l.strip()]
            return lines[0] if lines else "HTTP (no header)"
        
        # HTTPS -> attempt simple SSL handshake and GET
        if port == 443:
            try:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname = target) as ssock:
                    # send GET after handshake
                    ssock.settimeout(2)
                    ssock.send(b"GET/HTTP/1.1\r\nHost: " + target.encode() + b"\r\nConnection:close\r\n\r\n")
                    data = ssock.recv(2048).decode(errors="ignore")
                    lines = [l for l in data.splitlines() if l.strip()]
                    return lines[0] if lines else "HTTPS (no header)"
            except Exception:
                #if SSL fails, ensure socket is closed and fall back
                try:
                    sock.close()
                except Exception:
                    pass
                return "HTTPS (handshake failed)"
            
        #FTP usually sends banner immediately (port 21)
        if port == 21:
            data = sock.recv(2048).decode(errors="ignore").strip()
            sock.close()
            return data.splitlines()[0] if data else "FTP (no banner)"
        
        # SSH usually sends banner immediately (port 22)
        if port == 22:
            data = sock.recv(2048).decode(errors="ignore").strip()
            sock.close()
            return data.splitlines()[0] if data else "SSH (no bannner)"

        # SMTP (25), POP3 (110), IMAP(143) often send initial banners
        if port in (25,110,143):
            data = sock.recv(2048).decode(errors = 'ignore').strip()
            sock.close() 
            return data.splitlines()[0] if data else "Service (no banner)"
        
        #Default attempt: try recv once (many services send a banner)
        try:
            data = sock.recv(2048).decode(errors="ignore").strip()
            sock.close()
            if data:
                return data.splitlines()[0]
        except socket.timeout:
            try:
                sock.close()
            except Exception:
                pass
            return "Unknown"
        except Exception:
            try:
                sock.close()
            except Exception:
                pass
            return "Unknown"
    except Exception:
        return "Unknown"