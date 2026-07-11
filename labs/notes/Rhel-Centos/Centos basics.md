### 1 - System Information & OS Version
Confirm the operating system version, kernel, and architecture details.

```bash
cat /etc/redhat-release
cat /etc/os-release
hostnamectl
```

## 2 — Check current boot target

```bash
# Check current default boot target
systemctl get-default

# List all currently active target units
systemctl list-units --type=target --state=active
```
## 3 - Package management with DNF

```bash
# Update all system packages
sudo dnf update

# Install a specific package (e.g., vim)
sudo dnf install vim

# Remove an installed package
sudo dnf remove vim

# Search for a package in the repositories
dnf search htop

# List all installed packages
dnf list installed

# Get detailed information about a specific package
dnf info vim

# Check for available system updates without installing them
dnf check-update
```
## 4 - DNF Module Streams & Repositories

```bash
# List available module streams (alternate versions of software)
dnf module list

# Enable a specific stream and install (example: Node.js 18)
sudo dnf module enable nodejs:18
sudo dnf install nodejs

# List enabled repos
dnf repolist

# Add EPEL repo (extra packages)
sudo dnf install epel-release

# Manually add a custom repo
sudo dnf config-manager --add-repo <URL>
```
