# Basic Kali Linux Commands

## 1. File System Navigation
```bash
pwd           # show current directory
ls            # list files
ls -la        # list with permissions and hidden files
cd /path      # change directory
cd ..         # go back one level
cd ~          # go to home directory
```

## 2. File Operations
```bash
touch file.txt          # create empty file
mkdir foldername        # create folder
cp file.txt /path/      # copy file
mv file.txt /path/      # move or rename file
rm file.txt             # delete file
rm -rf foldername       # delete folder forcefully
cat file.txt            # view file contents
nano file.txt           # edit file
```

## 3. Network Commands
```bash
ifconfig                # show network interfaces and IP
ip a                    # modern version of ifconfig
ping 192.168.1.1        # test connectivity
netstat -tulnp          # show open ports
ss -tlnp                # modern version of netstat
```

## 4. User Management
```bash
whoami                  # show current user
sudo su                 # switch to root
passwd                  # change password
adduser username        # add new user
id                      # show user ID and groups
```

## 5. Process Management
```bash
ps aux                  # show all running processes
top                     # live process monitor
kill PID                # kill process by ID
kill -9 PID             # force kill
pkill processname       # kill by name
```

## 6. File Permissions
```bash
chmod 777 file          # give all permissions
chmod +x file.sh        # make file executable
chown user:group file   # change file owner
ls -l                   # view permissions
```

## 7. Searching
```bash
find / -name file.txt         # find file by name
grep "text" file.txt          # search text in file
grep -r "text" /path/         # search recursively
locate filename               # fast file search
```

## 8. System Info
```bash
uname -a                # kernel and OS info
df -h                   # disk space usage
free -h                 # RAM usage
uptime                  # system uptime
history                 # command history
```
