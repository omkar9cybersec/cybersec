# CSRF Attack in DVWA Lab

## Objective
Demonstrate and exploit a **Cross-Site Request Forgery (CSRF)** vulnerability in DVWA by forcing an authenticated user to change their password without consent using a malicious HTML file.

## What is CSRF?
A CSRF attack tricks a logged-in victim's browser into making unauthorized requests (like password changes) by submitting hidden forms. The attack succeeds because the browser automatically attaches session cookies to all requests to the vulnerable domain.

## Prerequisites
- DVWA running locally (vulnerable web application)
- Burp Suite Community Edition
- Firefox or Chrome browser
- Text editor (Notepad or similar)
- Session cookie from a logged-in DVWA account

## Lab Environment
- **Application:** DVWA (Damn Vulnerable Web Application)
- **Security Level:** Low (no anti-CSRF tokens)
- **Attack Vector:** GET-based password change request
- **Tools:** Burp Suite (Intercept + CSRF PoC Generator)

---

## Step-by-Step Exploitation

### Step 1: Initial Password Change via GET Request (00:01 - 00:52)
1. Log into DVWA with default credentials (admin/password)
2. Navigate to **CSRF** vulnerability section
3. Enter new password: `123`
4. Click **Change**
5. **Observation:** Password visible in URL as GET parameter (insecure design)
6. Log out and verify login with password `123` — **Success**

**Vulnerability Found:** Password change uses GET request instead of POST, making it URL-based and easily exploitable.

---

### Step 2: Capture Request with Burp Suite (00:52 - 01:49)
1. Open Burp Suite and enable **Proxy → Intercept**
2. Log back into DVWA
3. Change password to `1234`
4. Burp intercepts the request (shows GET parameter with new password)
5. Right-click the intercepted request
6. Select **Engagement Tools → Generate CSRF PoC**
7. Burp auto-generates an HTML form containing the vulnerable URL
8. **Copy the HTML code**

**Example PoC HTML Structure:**
```html
<html>
  <body>
    <form action="http://[DVWA-IP]/vulnerabilities/csrf/" method="GET">
      <input type="hidden" name="password_new" value="1234">
      <input type="hidden" name="passwd_submit" value="Change">
      <input type="submit" value="Submit">
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>
```

---

### Step 3: Create Malicious CSRF File (01:49)
1. Open **Notepad** (or text editor)
2. Paste the copied HTML PoC code
3. Save file as **`csrf.html`** (with .html extension)
4. Store on your local system (desktop or Downloads)
5. Turn off Burp **Intercept** to allow normal browsing

---

### Step 4: Verify Current Password State (01:49 - 02:48)
1. Manually change password to `quy` (dummy password to test attack)
2. Click **Change** without intercepting
3. Verify new password `quy` is set by attempting login
4. **Current state:** Password is `quy`, but PoC HTML still contains old password `1234`

---

### Step 5: Execute CSRF Attack (02:48 - 03:00)
**Critical Requirement:** The malicious HTML **must be opened in the same browser where the victim is logged in** (session cookie must be present).

1. Ensure you're still logged into DVWA in Firefox/Chrome
2. Right-click the **`csrf.html`** file on your desktop
3. Select **Open With → Firefox** (or your logged-in browser)
4. HTML form auto-submits via JavaScript (usually no visible popup)
5. **Result:** Password silently changes from `quy` back to `1234` without any user action

---

### Step 6: Verify Successful Attack (03:00 - 03:43)
1. Log out of DVWA
2. Try logging in with password `quy` (the one you set manually)
   - **Result:** Login Failed ❌
3. Try logging in with password `1234` (from the CSRF PoC)
   - **Result:** Login Successful ✅

**Conclusion:** CSRF attack successfully forced a password change without user consent.

---

## Key Vulnerabilities Identified

| Issue | Details |
|-------|---------|
| **GET-based Requests** | Password change uses GET instead of POST, making it URL-based |
| **No CSRF Token** | Application doesn't validate request origin with anti-CSRF tokens |
| **Session Cookies Auto-Attached** | Browser automatically includes cookies in hidden form submissions |
| **No SameSite Cookie Flag** | Cookies sent regardless of request origin |
| **No Referrer Validation** | Server doesn't check if request came from legitimate DVWA page |

---

## Attack Flow Diagram

```
Victim Logged into DVWA
        ↓
Attacker sends malicious csrf.html link
        ↓
Victim opens csrf.html in same browser
        ↓
Hidden form auto-submits to DVWA
        ↓
Browser attaches session cookie automatically
        ↓
Server processes password change (trusts cookie)
        ↓
Victim's password changed without consent ✓
```

---

## Mitigation Strategies

### 1. **Anti-CSRF Tokens (Primary Defense)**
- Generate unique token for each password change form
- Token must be submitted and validated server-side
- Token expires after single use

### 2. **Use POST Requests**
- Replace GET with POST for state-changing operations
- GET should only be used for retrieving data (read-only)

### 3. **SameSite Cookie Attribute**
```
Set-Cookie: session=abc123; SameSite=Strict
```
- Prevents browser from sending cookies on cross-site requests

### 4. **Custom Request Headers**
- Require `X-Requested-With: XMLHttpRequest` header
- Cross-site forms cannot set custom headers

### 5. **Referrer Validation**
- Verify `Referer` header matches your domain
- Reject requests from external sites

### 6. **Double-Submit Cookie Pattern**
- Require matching token in both cookie and form parameter
- Attacker can't read token from other sites

---

## Lab Takeaways

✅ **Learned:** CSRF exploits trust in session cookies, not weak passwords  
✅ **Learned:** Hidden form submission is invisible but effective  
✅ **Learned:** GET-based state changes are a major CSRF risk  
✅ **Learned:** Browser auto-attachment of cookies enables the attack  
✅ **Learned:** Burp Suite's PoC generator simplifies exploit development  

---

## Files Used
- `csrf.html` — Malicious CSRF payload (stored locally)
- DVWA CSRF page — Vulnerable endpoint
