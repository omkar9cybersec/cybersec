# IDOR Lab — Ticket Booking Price Manipulation

## Objective
Exploit IDOR to manipulate ticket prices through parameter tampering.

## What is IDOR?
Insecure Direct Object Reference — when applications trust client-supplied parameters
without server-side validation, attackers can modify prices, IDs, or other sensitive data.

## Low Security Exploitation

### Attack
1. User orders 10 tickets at €15 each
2. Intercept request with Burp Suite
3. Modify `ticket_price=15` to `ticket_price=1`
4. Send modified request

### Result
✅ Booked 10 tickets for €10 instead of €150 (93% discount)

**Vulnerable Request:**

POST /booking/purchase
ticket_quantity=10&ticket_price=15&action=confirm

**Modified Request:**
POST /booking/purchase
ticket_quantity=10&ticket_price=1&action=confirm

## Medium Security Exploitation

### Attack
1. Server removes price parameter from client request
2. Attacker manually adds it back: `ticket_price=2`
3. Server still accepts it

### Result
✅ Booked 10 tickets for €20 instead of €150 (87% discount)

## Root Cause
- **Trust client input** — Server accepts price from client
- **No validation** — No check if price is valid
- **No authorization** — No verification of permission

## Fix

**Vulnerable Code:**
```php
$price = $_POST['ticket_price'];  // ❌ WRONG
$total = $price * $_POST['quantity'];
```

**Secure Code:**
```php
$PRICE = 15;  // ✅ Server-side only
$quantity = $_POST['quantity'];
$total = $PRICE * $quantity;
```

## Prevention Checklist
- ✅ Never trust client prices
- ✅ Calculate prices server-side only
- ✅ Validate all input
- ✅ Add authorization checks
- ✅ Log all transactions

## Tools Used
- Burp Suite
- Browser DevTools

## Status
✅ IDOR vulnerability successfully exploited
