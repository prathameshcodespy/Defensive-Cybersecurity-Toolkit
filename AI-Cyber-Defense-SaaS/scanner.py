import socket
from concurrent.futures import ThreadPoolExecutor

def scan_ports(target, start_port, end_port):
    open_ports = []

    def scan(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            sock.close()
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"
                open_ports.append((port, service))
        except:
            pass

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan, range(start_port, end_port + 1))

    return open_ports
