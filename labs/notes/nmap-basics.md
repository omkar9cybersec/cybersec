# Nmap - Network Scanning

## What is Nmap?
Nmap (Network Mapper) is a free open-source tool used for
network discovery and security auditing.

## Basic Scans
```bash
nmap 192.168.1.1              # basic scan
nmap 192.168.1.0/24           # scan entire network
nmap -iL targets.txt          # scan from file
```

## Port Scans
```bash
nmap -p 80 192.168.1.1        # scan specific port
nmap -p 1-1000 192.168.1.1    # scan port range
nmap -p- 192.168.1.1          # scan all 65535 ports
```

## Detection Scans
```bash
nmap -sV 192.168.1.1          # service version detection
nmap -O 192.168.1.1           # OS detection
nmap -A 192.168.1.1           # aggressive (OS + version + scripts)
```

## Stealth Scans
```bash
nmap -sS 192.168.1.1          # SYN stealth scan
nmap -sU 192.168.1.1          # UDP scan
nmap -T0 192.168.1.1          # slowest - hardest to detect
nmap -T5 192.168.1.1          # fastest scan
```

## Output
```bash
nmap -oN output.txt 192.168.1.1    # save normal output
nmap -oX output.xml 192.168.1.1    # save XML output
nmap -oA output 192.168.1.1        # save all formats
```

## Practical Example - What I did in my lab
```bash
db_nmap -sV 192.168.18.138    # scanned Windows Server 2022
```
### Results found
- Port 53   - DNS (Simple DNS Plus)
- Port 80   - HTTP (Microsoft IIS 10.0)
- Port 88   - Kerberos
- Port 135  - Windows RPC
- Port 389  - LDAP
- Port 443  - HTTPS
- Port 445  - SMB
- Port 3268 - LDAP (Global Catalog)
- Hostname  - WIN-HAD3JJ9TIS2
- Domain    - training.com
- OS        - Windows Server 2022
- MAC       - 00:0C:29:AA:AD:14 (VMware)
