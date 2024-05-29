# canvas-notification 👨🏻‍💻
This project is a Python-based notification system designed to fetch upcoming assignments from the Canvas Learning Management System (LMS) and send email notifications about these assignments to my personal email. The script uses environment variables for configuration and supports daily scheduling.

## Installation 🏗️

### Prerequisites
* Python 3.6+ --> https://www.python.org/downloads/
* requests -->  For making HTTP requests to the Canvas API.
* schedule -->  For scheduling tasks.
* plyer -->  For desktop notifications.
* python-dotenv -->  For managing environment variables.
* smtplib -->  For sending emails.
* email -->  For constructing email messages.

## Setup
1. Clone the repo:
    bash<br>git clone https://github.com/MCdev92/canvas-notification.git<br>
2. Create a virtual environment and activate it
python3 -m venv venv
    `source venv/bin/activate  # On Windows, use venv\Scripts\activate`
3. Install the required pachages:
    `pip install requests schedule plyer python-dotenv`
4. Create a .env file in the project root and add your environment variables:
    `touch .env`

Add the following lines to the .env file:
* EMAIL_USER="your_email@gmail.com"
* EMAIL_PASSWORD="your_email_password"
* Access_Token="your_canvas_access_token"
* RECIPIENT_EMAIL="recipient_email@example.com"

# Troubleshooting
* Environment Variables Not Loaded: Ensure that the .env file is in the correct directory and that the variables are correctly named and spelled.
* Email Not Sent: Check your email configuration and ensure that your email account allows less secure apps if using Gmail. Alternatively, consider using an app-specific password.

# Future Enhancements 
* Add error handling for API requests.
* Improve email formatting. ✅
* Add desktop notifications using the plyer library.
* Extend the script to handle other Canvas API endpoints (e.g., grades, announcements).

# Demo
![alt text](cn.gif)



