import socket
import threading

#Core TCP Port Scanner
def scan_tcp_port(target:str,port: int, open_ports:list):
    """
    Scan a single TCP Port on the target host.
    Args:
    target (str): The target IP address or Hostname.
    port (int): Port number to scan.
    open_ports (list): Shared list to store open ports.
    """

    try:
        #Create a TCP socket
        sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        sock.settimeout(1)# 1 second timeout for resposiveness
        result = sock.connect_ex((target,port)) # 0 if port open

        if result == 0:
            open_ports.append(port)#Save open port
        sock.close()
    except Exception as e:
        #Avoid crashing if something goes wrong
        pass

def run_tcp_scan(target:str, start_port:int, end_port: int):
    """
    Run a multi-threaded TCP port scan.

    Args:
        target (str): The target IP address or hostname.
        start_port(int): Starting port number.
        end_port (int): Ending port number.

    Returns:
        list: A list of open ports.
    """
    open_ports = []
    threads = []

    for port in range(start_port, end_port + 1):
        #Each port gets its own thread
        t = threading.Thread(target = scan_tcp_port, args = (target, port,open_ports))
        threads.append(t)
        t.start()

    #Wait for all  threads to finish
    for t in threads:
        t.join()
    
    return sorted(open_ports)