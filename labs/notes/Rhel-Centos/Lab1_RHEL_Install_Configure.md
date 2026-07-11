# Lab 1: Installing & Configuring RHEL/CentOS

**Course**: Cybersecurity & Forensics (Linux Foundation)
**VM**: RHEL/Rocky/AlmaLinux 8 or 9
**Level**: Beginner
**Duration**: ~2-3 hours

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: OS Verification](#step-1--os-verification)
3. [Step 2: Boot Targets (systemd)](#step-2--boot-targets-systemd)
4. [Step 3: Package Management (DNF)](#step-3--package-management-dnf)
5. [Step 4: Module Streams & Repositories](#step-4--module-streams--repositories)
6. [Step 5: The /boot Partition](#step-5--the-boot-partition)
7. [Step 6: Managing Services & Daemons](#step-6--managing-services--daemons)
8. [Step 7: Firewall Configuration](#step-7--firewall-configuration-firewalld)
9. [Step 8: SELinux Management](#step-8--selinux-management)
10. [Practical Lab: Combined Workflow](#practical-lab-combined-workflow)

---

## Prerequisites

- VMware/VirtualBox with RHEL, Rocky Linux, or AlmaLinux installed
- Internet connectivity (for package downloads)
- Sudo access (or root user)
- Basic terminal familiarity

---

## Step 1: OS Verification

Verify RHEL version and system information.

### Commands

```bash
# Check release version
cat /etc/redhat-release

# Detailed OS info (JSON format)
cat /etc/os-release

# Show OS, kernel, and architecture
hostnamectl
```

### Expected Output Example

```
Red Hat Enterprise Linux release 9.4 (Plow)
```

```
NAME="Red Hat Enterprise Linux"
VERSION_ID="9.4"
KERNEL="5.14.0-362.el9.x86_64"
ARCHITECTURE="x86_64"
```

### What This Tells You
- Distribution name and version
- Kernel version (security patches matter)
- CPU architecture (x86_64 = 64-bit Intel/AMD)

---

## Step 2: Boot Targets (systemd)

RHEL 7+ uses **systemd targets** instead of old runlevels (0-6).

### Systemd Targets vs SysV Runlevels

| Runlevel | Systemd Target | Purpose |
|----------|---|---|
| 0 | `poweroff.target` | Halt system |
| 1 | `rescue.target` | Single-user (maintenance) |
| 2-4 | `multi-user.target` | Multi-user text mode (server) |
| 5 | `graphical.target` | GUI mode (desktop) |
| 6 | `reboot.target` | Reboot |

### Commands

```bash
# Get current default boot target
systemctl get-default

# List all active targets
systemctl list-units --type=target --state=active

# List ALL available targets
systemctl list-units --type=target

# Switch to multi-user (text) mode NOW (no reboot)
sudo systemctl isolate multi-user.target

# Change default boot target permanently
sudo systemctl set-default multi-user.target
```

### Example Workflow

```bash
# Check what you're booting to
systemctl get-default
# Output: graphical.target

# Change to text-only (server mode)
sudo systemctl set-default multi-user.target

# Verify change
systemctl get-default
# Output: multi-user.target

# Reboot to apply
sudo reboot
```

---

## Step 3: Package Management (DNF)

**DNF** = Dandified Yum. RHEL 8+ package manager (replaces YUM).

### Basic Commands

```bash
# Update all packages
sudo dnf update

# Install a package
sudo dnf install <package>

# Remove a package
sudo dnf remove <package>

# Search for a package
dnf search <keyword>

# List installed packages
dnf list installed

# Get info about a package
dnf info <package>

# Check for available updates
dnf check-update
```

### Deep Dive: Each Command

**1. Update System**
```bash
sudo dnf update
```
- Downloads latest versions of all installed packages
- Includes security patches (critical)
- First-time can take 5-15 minutes
- Requires internet + valid repos

**2. Install Package**
```bash
sudo dnf install vim
```
- Installs package and dependencies
- Prompts for confirmation (`Y/n`)
- No output after completion = success

**3. Search for Package**
```bash
dnf search htop
```
- Searches package name and description
- Shows available versions
- Example output:
  ```
  htop.x86_64 : Interactive process viewer
  ```

**4. List Installed**
```bash
dnf list installed
```
- Shows all installed packages
- Large output (pipe to `grep` to filter)
  ```bash
  dnf list installed | grep vim
  ```

**5. Package Info**
```bash
dnf info vim
```
- Shows size, version, repo, description, dependencies
- Useful before installing large packages

**6. Check Updates**
```bash
dnf check-update
```
- Shows packages with available updates
- Does NOT install; just reports
- Run `dnf update` to apply

### Real-World Workflow

```bash
# 1. Search for a tool
dnf search nginx

# 2. Get detailed info
dnf info nginx

# 3. Install it
sudo dnf install nginx

# 4. Verify installation
dnf list installed | grep nginx

# 5. Check for updates later
dnf check-update nginx

# 6. Update if needed
sudo dnf update nginx
```

---

## Step 4: Module Streams & Repositories

**Modules** = Alternative versions of software (Python 3.9 vs 3.11, Node.js 16 vs 18, etc.)

### Commands

```bash
# List available module streams
dnf module list

# Enable a specific stream
sudo dnf module enable nodejs:18

# Install from enabled stream
sudo dnf install nodejs

# List enabled repos
dnf repolist

# Add EPEL repo (Extra Packages for Enterprise Linux)
sudo dnf install epel-release

# Manually add custom repo
sudo dnf config-manager --add-repo <URL>
```

### Deep Dive: Module Streams

**Why modules?**
- RHEL supports multiple versions of popular software
- Choose the version you need without waiting for OS updates

**Example: Node.js**
```bash
# See all Node versions available
dnf module list nodejs

# Output:
# nodejs          10 [d]            ...
# nodejs          12 [d]            ...
# nodejs          18                ...
# nodejs          20                ...

# Enable version 18
sudo dnf module enable nodejs:18

# Install it
sudo dnf install nodejs

# Verify
node --version
```

### Repositories

**Default repos**: BaseOS, AppStream (RHEL subscription)
**EPEL**: Extra Packages (free, community-maintained)

```bash
# See active repos
dnf repolist

# Add EPEL (extra tools)
sudo dnf install epel-release

# List repos again (EPEL now included)
dnf repolist
```

---

## Step 5: The /boot Partition

The `/boot` partition contains files needed to **start the OS before filesystem encryption kicks in**.

### What's Inside /boot

```bash
ls -l /boot
```

**Files you'll see:**
- `vmlinuz-5.14.0-362.el9.x86_64` = Linux kernel
- `initramfs-5.14.0-362.el9.x86_64.img` = Initial RAM filesystem (drivers for boot)
- `grub2/` = GRUB2 bootloader directory
- `grub2/grubenv`, `grub.cfg` = Boot menu config

### Why Separate Partition?

**1. Encryption**: If `/` is encrypted, `/boot` cannot be (bootloader reads it before decryption)
**2. Old BIOS limits**: Some old systems couldn't read large disks; small `/boot` at disk start solved this
**3. Multiple kernels**: Keep several kernel versions without filling root partition

### Commands

```bash
# View /boot contents
ls -l /boot

# Show partition layout
lsblk

# Show /boot size and usage
df -h /boot

# List kernel images
ls -la /boot/vmlinuz*

# List initramfs images
ls -la /boot/initramfs*
```

### Example Output

```
/dev/sda1        1M  use%  500M  /boot
```

**Typical size**: 500 MiB – 1 GiB

---

## Step 6: Managing Services & Daemons

A **service** (daemon) is a background process. Examples: SSH, Apache, firewall.

### What is systemctl?

`systemctl` controls services in systemd (RHEL 7+).

### Commands

```bash
# Check service status
systemctl status sshd

# Start service NOW (temporary)
sudo systemctl start sshd

# Stop service
sudo systemctl stop sshd

# Restart service
sudo systemctl restart sshd

# Enable service to auto-start at boot
sudo systemctl enable sshd

# Disable auto-start
sudo systemctl disable sshd

# Check if enabled
systemctl is-enabled sshd

# List all services
systemctl list-units --type=service

# View service logs
journalctl -u sshd -n 20
```

### Deep Dive: Key Commands

**1. Check Status**
```bash
systemctl status sshd
```
**Output tells you:**
- `Active: active (running)` = working
- `Active: inactive (dead)` = stopped
- `Enabled` or `disabled` = auto-start on boot?
- Process ID (PID)
- Recent log lines

**2. Start/Stop/Restart**
```bash
sudo systemctl start sshd    # Now (temp, lost on reboot)
sudo systemctl stop sshd
sudo systemctl restart sshd  # Stop + start (for config changes)
```
**No output = success**

**3. Enable (Persistent)**
```bash
sudo systemctl enable sshd
```
- Creates symlink: `/etc/systemd/system/multi-user.target.wants/sshd.service`
- Service auto-starts on boot
- **Important**: `enable` ≠ `start`. Do both if you want it running now AND on boot:
  ```bash
  sudo systemctl enable sshd
  sudo systemctl start sshd
  ```

**4. Disable**
```bash
sudo systemctl disable sshd
```
- Removes auto-start on boot
- If already running, stays running until reboot/stop

**5. Check if Enabled**
```bash
systemctl is-enabled sshd
```
- Returns: `enabled` or `disabled` (one word)
- Quick pre-reboot check

**6. View Logs**
```bash
journalctl -u sshd -n 20
```
- Last 20 lines of sshd logs
- Use for debugging failures
- Example error:
  ```
  Jan 15 10:30:45 server sshd[1235]: error: Could not load host key
  ```

### Real-World Workflow

```bash
# 1. Check if SSH is running
systemctl status sshd

# 2. Enable it to start at boot
sudo systemctl enable sshd

# 3. Start it now
sudo systemctl start sshd

# 4. Edit config file
sudo vi /etc/ssh/sshd_config

# 5. Restart to apply config
sudo systemctl restart sshd

# 6. Verify it restarted okay
systemctl status sshd

# 7. Check logs if something broke
journalctl -u sshd -n 50
```

---

## Step 7: Firewall Configuration (firewalld)

The **firewall** controls which network traffic is allowed in/out.

### Core Concepts

- **Zone** = network trust level (public, private, trusted)
- **Port** = network endpoint (SSH=22, HTTP=80, HTTPS=443)
- **Service** = predefined ports+protocols (http, https, ssh, ftp, etc.)

### Commands

```bash
# Check firewall status
sudo systemctl status firewalld

# Get firewall state
sudo firewall-cmd --state

# List all current rules
sudo firewall-cmd --list-all

# List available services
sudo firewall-cmd --get-services

# Add service PERMANENTLY
sudo firewall-cmd --permanent --add-service=http

# Add port PERMANENTLY
sudo firewall-cmd --permanent --add-port=8080/tcp

# Remove service
sudo firewall-cmd --permanent --remove-service=http

# MUST RELOAD after permanent changes
sudo firewall-cmd --reload

# Add rule temporarily (lost on reload/reboot)
sudo firewall-cmd --add-service=http
```

### Deep Dive: Key Commands

**1. Check Status**
```bash
sudo firewall-cmd --state
```
- Returns: `running` or `not running`
- Alternative: `sudo systemctl status firewalld`

**2. List All Rules**
```bash
sudo firewall-cmd --list-all
```
**Output example:**
```
public (active)
  target: default
  interfaces: ens192
  services: cockpit dhcpv6-client ssh
  ports: 8080/tcp
  icmp-block-inversion: no
```
**What you see:**
- `services` = allowed services
- `ports` = allowed ports
- `interfaces` = which network adapters apply

**3. Add Service Permanently**
```bash
sudo firewall-cmd --permanent --add-service=http
```
- Opens HTTP (port 80/tcp)
- `--permanent` = survives reboot
- **Must reload after:**
  ```bash
  sudo firewall-cmd --reload
  ```

**4. Add Port Permanently**
```bash
sudo firewall-cmd --permanent --add-port=8080/tcp
```
- Opens specific port
- Format: `port/protocol` (tcp or udp)
- Example: `3306/tcp` (MySQL)

**5. Temporary Add (Testing)**
```bash
sudo firewall-cmd --add-service=http
```
- No `--permanent` = lost on reload or reboot
- Use this to test before making permanent

**6. Reload (Apply Permanent Changes)**
```bash
sudo firewall-cmd --reload
```
- Applies all `--permanent` rules
- Does NOT drop existing connections (safe)
- Required after adding permanent rules

**7. List Available Services**
```bash
sudo firewall-cmd --get-services
```
- Shows predefined services: http, https, ssh, ftp, mysql, postgres, etc.
- Easier than remembering port numbers

### Real-World Workflow

```bash
# 1. Check firewall status
sudo systemctl status firewalld

# 2. See current rules
sudo firewall-cmd --list-all

# 3. Enable HTTP and HTTPS permanently
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# 4. Enable custom port (8080)
sudo firewall-cmd --permanent --add-port=8080/tcp

# 5. Apply changes
sudo firewall-cmd --reload

# 6. Verify
sudo firewall-cmd --list-all

# 7. Check firewalld logs if traffic still blocked
sudo journalctl -u firewalld -n 20
```

---

## Step 8: SELinux Management

**SELinux** = Security-Enhanced Linux. Mandatory access control that restricts even privileged processes.

### Modes

| Mode | Behavior |
|------|----------|
| **Enforcing** | Strictly blocks policy violations |
| **Permissive** | Logs violations but allows them (testing) |
| **Disabled** | SELinux turned off |

### Commands

```bash
# Current mode (one word)
getenforce

# Detailed status
sestatus

# Temporarily switch to Permissive
sudo setenforce 0

# Temporarily switch to Enforcing
sudo setenforce 1

# Make permanent (requires reboot)
sudo vi /etc/selinux/config
# Change: SELINUX=enforcing
```

### Deep Dive: Key Commands

**1. Check Current Mode**
```bash
getenforce
```
- Returns: `Enforcing`, `Permissive`, or `Disabled`
- Quick check

**2. Detailed Status**
```bash
sestatus
```
**Output example:**
```
SELinux status:                 enabled
Current mode:                   enforcing
Mode from config file:          enforcing
Policy version:                 33
```
**Key lines:**
- `Current mode` = what's running NOW
- `Mode from config file` = what loads on reboot
- Must match for consistency

**3. Temporary Mode Change**
```bash
sudo setenforce 0  # Permissive (logging)
sudo setenforce 1  # Enforcing (blocking)
```
- Lost on reboot
- Use for debugging: "Is SELinux blocking this?"

**4. Permanent Mode Change**
```bash
sudo vi /etc/selinux/config
```
Find:
```
SELINUX=enforcing
```
Change to:
```
SELINUX=permissive
```
**OR**
```
SELINUX=disabled
```
**Save and reboot:**
```bash
sudo reboot
```

**5. SELinux Logs**
```bash
sudo journalctl -u setroubleshoot -n 20
```
- Shows what SELinux blocked
- Helps identify policy violations

### Cybersecurity Context

SELinux prevents **privilege escalation**:
- Apache web server (user: `apache`) gets hacked
- SELinux prevents it from reading `/root/` or accessing other services
- Restricts network access to allowed ports only
- All violations logged for forensic analysis

### Real-World Workflow

```bash
# 1. Check current mode
getenforce

# 2. See detailed status
sestatus

# 3. Service X failing? Test if it's SELinux
sudo setenforce 0
# Try the service...
sudo setenforce 1

# 4. Check what was blocked
sudo journalctl -u setroubleshoot -n 20

# 5. Make permanent if needed
sudo vi /etc/selinux/config
# Change SELINUX=enforcing
sudo reboot
```

---

## Practical Lab: Combined Workflow

**Objective**: Install Apache web server, enable it, secure with firewall, and verify SELinux.

### Complete Lab Steps

```bash
# ===== STEP 1: INSTALL APACHE =====
sudo dnf install httpd

# ===== STEP 2: ENABLE & START SERVICE =====
sudo systemctl enable httpd
sudo systemctl start httpd
systemctl status httpd

# ===== STEP 3: OPEN FIREWALL FOR HTTP/HTTPS =====
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# ===== STEP 4: VERIFY FIREWALL =====
sudo firewall-cmd --list-all

# ===== STEP 5: CHECK SELINUX =====
getenforce

# ===== STEP 6: TEST WEB SERVER =====
curl http://localhost

# ===== STEP 7: CHECK LOGS =====
journalctl -u httpd -n 20
sudo firewall-cmd --list-all
sestatus
```

### Expected Results

```
Service httpd started and enabled ✓
Firewall allows HTTP/HTTPS ✓
SELinux in enforcing mode ✓
Web server responding to requests ✓
```

### Cleanup (Optional)

```bash
sudo systemctl stop httpd
sudo systemctl disable httpd
sudo firewall-cmd --permanent --remove-service=http
sudo firewall-cmd --permanent --remove-service=https
sudo firewall-cmd --reload
sudo dnf remove httpd
```

---

## Summary Checklist

- [ ] OS version verified
- [ ] Boot target understood
- [ ] DNF package commands practiced
- [ ] Module streams explored
- [ ] /boot partition examined
- [ ] Services managed (enable/disable/start/stop)
- [ ] Firewall rules applied
- [ ] SELinux mode checked
- [ ] Combined lab completed

---

## Next Steps

**Lab 2**: User & Group Management + File System Permissions  
**Lab 3**: Adding Disks, Partitions & LVM  
**Lab 4**: Monitoring Processes & Daemons  
**Lab 5**: SSH Server Configuration  

---

## Quick Reference

### Most-Used Commands

```bash
# System info
cat /etc/redhat-release
hostnamectl

# Packages
sudo dnf update
sudo dnf install <package>

# Services
sudo systemctl enable sshd
sudo systemctl start sshd
systemctl status sshd

# Firewall
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload

# SELinux
getenforce
sestatus
```

---

**Author**: Cybersecurity & Forensics Course  
**Last Updated**: 2024  
**Level**: Beginner  
