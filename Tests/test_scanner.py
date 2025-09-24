import socket
import threading 
import time 
import pytest

from PyNmaplite.scanner import run_tcp_scan, grab_banner

def _start_dummy_server(port, banner=None, http=False):
    """
    Start a simple TCP server in a background thread. 
    If banner is provided -> sends banner immediately after accept.
    If http is True -> reads a request and returns a simple HTTP response.
    Returns:(thread, shutdown_event)
    """

    shutdown = threading.Event()

    def server():
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1",port))
        srv.listen(1)
        srv.settimeout(0.5)

        try:
            while not shutdown.is_set():
                try:
                    conn, addr = srv.accept()
                except socket.timeout:
                    continue
                try:
                    if banner:
                        #send banner immediately
                        conn.sendall((banner + "\r\n").encode())
                        conn.close()
                        continue
                    if http:
                        # read request, send simple response
                        data = conn.recv(4096)
                        resp = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK"
                        conn.sendall(resp.encode())
                        conn.close()
                        continue
                    # default: echo then close
                    data = conn.recv(1024)
                    conn.sendall(data)
                    conn.close()
                except Exception:
                    try:
                        conn.close()
                    except Exception:
                        pass
        finally:
            srv.close()

    th = threading.Thread(target=server, daemon=True)
    th.start()
    #give server time to bind
    time.sleep(0.1)
    return th, shutdown

def test_run_tcp_scan_finds_open_port():
    port = 40001
    th, shutdown = _start_dummy_server(port)
    try:
        found = run_tcp_scan("127.0.0.1", port,port)
        assert port in found, "Scanner should detect the open port"
    finally:
        shutdown.set()
        th.join(timeout=1)
    
def test_grab_banner_returns_sent_banner():
    port = 40002
    banner_text = "TEST-SERVICE-1.0"
    th, shutdown = _start_dummy_server(port, bannner=banner_text)
    try:
        b = grab_banner("127.0.0.1", port)
        assert banner_text in b, f"Expected banner to contain '{banner_text}', got:{b}"
    finally:
        shutdown.set()
        th.join(timeout=1)

def test_grab_banner_http():
    port = 40003
    th, shutdown = _start_dummy_server(port, http = True)
    try:
        b = grab_banner("127.0.0.1",port)
        # grep for HTTP response line; our grab_banner returns  first non-empty header line
        assert ("HTTP/1.1 200" in b) or ("HTTP/1.0 200" in b) or ("HTTP/1.1" in b) or ("HTTP/" in b)
    finally:
        shutdown.set()
        th.join(timeout=1)

def test_closed_port_not_found():
    #Choose a port unlikely to be open(no server started)
    port = 40004
    found = run_tcp_scan("127.0.0.1", port,port)
    assert port not in found
    

