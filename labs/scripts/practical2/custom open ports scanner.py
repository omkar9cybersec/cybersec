#!/usr/bin/env python3
import socket
import sys

def scan_port(host, port):
    """Scan a single port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            return True
        return False
    except:
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 port-scanner.py <host> [port]")
        print("Example: python3 port-scanner.py 192.168.1.1")
        print("Example: python3 port-scanner.py 192.168.1.1 80")
        sys.exit(1)
    
    host = sys.argv[1]
    
    if len(sys.argv) == 3:
        # Scan single port
        port = int(sys.argv[2])
        if scan_port(host, port):
            print(f"[+] Port {port} is OPEN")
        else:
            print(f"[-] Port {port} is CLOSED")
    else:
        # Scan common ports
        common_ports = [21, 22, 23, 80, 443, 445, 3306, 3389, 5432, 8080]
        print(f"[*] Scanning {host} for common ports...\n")
        
        for port in common_ports:
            if scan_port(host, port):
                print(f"[+] Port {port} is OPEN")

if __name__ == "__main__":
    main()
