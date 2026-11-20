# Access Control Security Lab (Mini-SOC)

## Overview
This is a deliberately vulnerable web application built entirely on an Android phone using Termux, Python, and Flask. It serves as a training lab to demonstrate, exploit, and understand critical web security vulnerabilities, specifically focusing on the OWASP Top 10 (#1: Broken Access Control).

## Architecture
*   **Backend:** Python (Flask)
*   **Database:** SQLite
*   **Frontend:** HTML/CSS (Bootstrap 5 Dark Mode)
*   **Environment:** Termux (Android)

## Intentionally Built Vulnerabilities
This application contains three specific flaws for educational purposes:
1.  **IDOR (Insecure Direct Object Reference):** Users can view other users' orders by changing the ID in the URL.
2.  **Parameter Tampering:** The profile update form trusts client-side input, allowing a user to change their role to 'admin'.
3.  **Broken Access Control:** The `/admin` route only checks if a user is logged in, not if they have admin privileges.

## How to Run
1. Install requirements: `pip install flask requests`
2. Initialize the database: `python init_db.py`
3. Start the server: `python app.py`
4. Access the app at `http://localhost:5000`
5. Run the attack script: `python exploit.py`

## Disclaimer
This application is for educational purposes only. Do not deploy this in a production environment.
