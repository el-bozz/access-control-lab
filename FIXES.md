# Remediation Guide (How to secure the application)

### 1. Fixing the IDOR Vulnerability (`/order/<id>`)
**The Flaw:** The server fetches an order by ID without checking who owns it.
**The Fix:** The server must verify that the `user_id` of the requested order matches the `session['user_id']` of the logged-in user before displaying it.
```python
# Secure Code Example:
order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
if order and order['user_id'] == session['user_id']:
    return render_template('order.html', order=order)
else:
    return "Unauthorized", 403
# Secure Code Example:
if session.get('role') != 'admin':
    return "Access Denied: Admins Only", 403
