# library for making HTTP requests
# library for scheduling tasks in Python
# plyer for notification request
import requests 
import datetime 
import schedule 
import os
import time
import smtplib
from dotenv import load_dotenv
from plyer import notification
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pytz import timezone, utc


# Load environment variables from .env file
load_dotenv()

# CSUEB-Canvas URL and Token
Canvas_URL = 'https://csueb.instructure.com/'
Access_Token = os.environ.get('Access_Token')


# Email Configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

# Define the time zone for Canvas and your local time zone
canvas_tz = utc
local_tz = timezone('America/Los_Angeles')  # Change to your local time zone

def get_weekly_assignments():
    try:
        # Define the endpoint for fetching courses
        courses_url = f'{Canvas_URL}/api/v1/courses'
        headers = {'Authorization': f'Bearer {Access_Token}'}
        
        # requests.get sends GET request to the courses endpoint
        response = requests.get(courses_url, headers=headers)
        response.raise_for_status() # Raise HTTPError for bad responses
        courses = response.json()
    except requests.RequestException as e:
        print(f"Error fetching courses: {e}")
        return []
        
    due_assignments = [] # empty list to store assignments
    
    # Loop through courses
    for course in courses:
        # Ensure 'name' key exists in the 'course' dictionary
        course_name = course.get('name')
        if course_name:
            try:
                # Define the endpoint for fetching assignments for each course
                assignments_url = f'{Canvas_URL}/api/v1/courses/{course["id"]}/assignments'
                response = requests.get(assignments_url, headers=headers)
                response.raise_for_status()
                assignments = response.json()
            except requests.RequestException as e:
                print(f"Error fetching assignments for course {course['name']}: {e}")
                continue
                
            # check if assignment has a "due_at" date
            for assignment in assignments:
                if "due_at" in assignment and assignment["due_at"]:
                    try:
                        due_date = datetime.datetime.strptime(assignment["due_at"], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=utc)
                        due_date = due_date.astimezone(local_tz) # convert to local time zone
                        now = datetime.datetime.now(local_tz)
                        one_week = datetime.timedelta(weeks=1)
                        if now <= due_date <= now + one_week:
                            due_assignments.append({
                                'course': course['name'],
                                'name': assignment['name'],
                                'due_at': due_date
                            })
                    except ValueError as e:
                        print(f"Error parsing date for assignment {assignment['name']}: {e}")
                        continue
    return due_assignments

def format_due_date(due_date):
    return due_date.strftime('%A, %B %d, %Y at %I:%M %p')

def print_upcoming_assignments():
    try:
        # print the upcoming assignments
        assignments = get_weekly_assignments()
        if assignments:
            print("The following Assignments are due this Week:")
            for assignment in assignments:
                print(f"Course: {assignment['course']}, Assignment: {assignment['name']}, Due: {assignment['due_at']}")
        else:
            print("No assignments due this week!")
    except Exception as e:
        print(f"Error printing assignments: {e}")
        
def notify_upcoming_assignments():
    try:
        # handle the notifications
        assignments = get_weekly_assignments()
        if assignments:
            email_subject = "Upcoming Assignments Due This Week"
            email_body = """
            <html>
            <body>
            <h1>Upcoming Assignments Due This Week:</h1>
            <ul>
            """
            for assignment in assignments:
                email_body += f"""
                <li>
                    <strong>Course:</strong> {assignment['course']}<br>
                    <strong>Assignment:</strong> {assignment['name']}<br>
                    <strong>Due:</strong> {format_due_date(assignment['due_at'])}
                </li>
                <br><br>
                """
            email_body += """
            </ul>
            <p>Best regards,<br>Your Course Management System</p>
            <br>
            <footer>
            <small>Developed by Manuel Corporan</small>
            <br>
            <small>Copyright © 2024 Mcdev92. All rights reserved.</small>
            </footer>
            </body>
            </html>
            """    
            send_email(email_subject, email_body)
        else:
            send_email("No Assignments Due This Week", """
            <html>
            <body>
            <p>No assignments due this week.</p>
            <p>Best regards,<br>Your Course Management System</p>
            </body>
            </html>
            """)
    except Exception as e:
        print(f"Error notifying assignments: {str(e)}")

        
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = "Canvas Daily Notification <" + EMAIL_USER + ">"
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
        
# Initial call to fetch and display assignments
notify_upcoming_assignments()

