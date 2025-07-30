# CDR-Portal
A Professional CDR portal For Telcom Industry 

📞 Teletalk CDR Access Portal
Teletalk CDR Access Portal is a secure web application for authorized staff to query Call Detail Records (CDR) and perform MSISDN/IMEI lookups with OTP-based authentication. Built with Flask (Python backend) and Vanilla JavaScript (frontend).

✨ Features
✅ Secure login with SMS OTP verification

✅ Dashboard with multiple query tools

14-Column CDR Search

MSISDN → IMEI lookup

IMEI → MSISDN lookup

LAC/Cell CDR lookup

CGI/MSISDN CDR lookup

Foreign number query

✅ CSV download of results

✅ Supports single and batch file uploads

✅ Server-side logging and verification

✅ Designed for internal use with secure SSH/Oracle DB integration

📂 Project Structure
project/
│
├── app.py              # Flask backend server
├── templates/
│   └── index.html      # Main HTML page with embedded JS
├── static/
│   ├── style.css       # CSS styles
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── ...
⚙️ Prerequisites
Python 3.8+

Flask

Oracle DB (or relevant DB)

SMS API credentials for sending OTPs

SSH access if using remote shell scripts

🚀 Setup & Run
cd teletalk-cdr-portal
2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Update your configuration
Set your DB, SMS API, and any SSH keys in app.py or environment variables.

5️⃣ Run the Flask app
flask run


🔐 How It Works
User enters their mobile number and requests an OTP.

The server generates an OTP and sends it via your configured SMS gateway.

User enters the OTP to verify and unlock the dashboard.

All searches hit Flask /api/* routes, run DB queries or scripts, and return results as JSON.

The frontend builds a dynamic HTML table and offers CSV download.

🛡️ Security Note
This project is intended for internal network only.

Use HTTPS in production.

Always verify phone numbers and logs server-side.

Limit access with SSH keys and IP whitelisting if needed.

🧑‍💻 Contributing
Pull requests are welcome! Please fork the repository and submit a PR with clear commit messages.

📜 License
MIT License. See LICENSE for more details.
