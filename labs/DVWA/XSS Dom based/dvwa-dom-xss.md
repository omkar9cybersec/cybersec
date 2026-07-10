# DVWA - DOM-Based XSS (Low & Medium)

**Objective:** Exploit DOM-based Cross-Site Scripting in DVWA's `xss_d` module at Low and Medium security levels, and bypass a tag-blacklist filter.

**Environment:**
- Target: DVWA (Damn Vulnerable Web Application), module `XSS (DOM)`
- Method: GET request, `default` parameter (language selector)

---

## Low Security

**Steps:**
1. Navigate to `XSS (DOM)`, select a language (e.g., English).
2. URL reflects choice: `?default=English`
3. View page source — confirm `English` is inserted directly into the DOM with no sanitization.
4. Inject payload in the `default` parameter:
   ```
   <script>alert(1)</script>
   ```
5. Alert box fires — sanitization bypassed.

**Result:** ✅ Popup triggered, confirming unsanitized DOM write.

---

## Medium Security

**Steps:**
1. Repeat the same `<script>` payload.
2. No alert fires.
3. View page source — filter explicitly strips `<script>` tags (blacklist, not encoding).
4. Bypass: close the `<option>` element, then inject a non-`<script>` payload using an event handler:
   ```
   </option></select><svg/onload="alert(1)"
   ```
5. Alert box fires — filter bypassed.

**Result:** ✅ Popup triggered via `<svg onload>`, confirming the filter only blocks `<script>` tags and not other JS-executing vectors.

---

## Vulnerability Explanation

DOM-based XSS occurs when client-side JavaScript writes attacker-controlled input (URL parameter, fragment, etc.) directly into the DOM without sanitization or encoding. Unlike reflected/stored XSS, no server round-trip is required — the payload never has to reach the server unsanitized, only the DOM.

At Medium level, DVWA applies a **blacklist filter** that strips the literal string `<script>`. This is insufficient because many other HTML elements/attributes can execute JavaScript (`onload`, `onerror`, `onclick`, `<img>`, `<svg>`, `<body onpageshow>`, etc.).

## Impact

- Arbitrary JavaScript execution in the victim's browser session
- Session/cookie theft, credential harvesting via fake forms, keylogging
- Actions performed in the context of the logged-in user (CSRF-like abuse)

## Remediation

- Use context-aware output encoding (HTML entity encoding) instead of tag blacklisting
- Sanitize/validate input against an allowlist, not a denylist
- Avoid unsafe DOM sinks (`innerHTML`, `document.write`) — use `textContent` / safe DOM APIs
- Implement a strict Content Security Policy (CSP) to block inline script execution
- Use frameworks with built-in auto-escaping (React, Angular) where possible

## Tools Used

- DVWA (target application)
- Browser (view-source, manual payload injection)

## Status

✅ Exploited — Low and Medium security levels bypassed
