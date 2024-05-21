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


def get_weekly_assignments():
    # Define the endpoint for fetching courses
    courses_url = f'{Canvas_URL}/api/v1/courses'
    headers = {'Authorization': f'Bearer {Access_Token}'}
    
    # requests.get sends GET request to the courses endpoint
    response = requests.get(courses_url, headers=headers)  
    courses = response.json()

    due_assignments = [] # empty list to store assignments
    
    # Loop through courses
    for course in courses:
        # Define the endpoint for fetching assignments for each course
        assignments_url = f'{Canvas_URL}/api/v1/courses/{course["id"]}/assignments'
        response = requests.get(assignments_url, headers=headers)
        assignments = response.json()
        
        # check if assignment has a "due_at" date
        for assignment in assignments:
            if "due_at" in assignment and assignment["due_at"]:
                due_date = datetime.datetime.strptime(assignment["due_at"], '%Y-%m-%dT%H:%M:%SZ')
                now = datetime.datetime.utcnow()
                one_week = datetime.timedelta(weeks=1)
                if now <= due_date <= now + one_week:
                    due_assignments.append({
                        'course': course['name'],
                        'name': assignment['name'],
                        'due_at': due_date
                    })
    return due_assignments

def print_upcoming_assignments():
    # print the upcoming assignments
    assignments = get_weekly_assignments()
    if assignments:
        print("The following Assignments are due this Week:")
        for assignment in assignments:
            print(f"Course: {assignment['course']}, Assignment: {assignment['name']}, Due: {assignment['due_at']}")
    else:
        print("No assignments due this week!")

def notify_upcoming_assignments():
    # handle the notifications
    assignments = get_weekly_assignments()
    if assignments:
        email_subject = "Upcoming Assignments Due This Week"
        email_body = "&lt;h1&gt;Upcoming Assignments Due This Week:&lt;/h1&gt;"
        for assignment in assignments:
            email_body += f"&lt;p&gt;Course: {assignment['course']}, Assignment: {assignment['name']}, Due: {assignment['due_at']}&lt;/p&gt;"
        send_email(email_subject, email_body)
    else:
        send_email("No Assignments Due This Week", "No assignments due this week.")

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
    server.quit()

# Schedule the task to run weekly
schedule.every().day.at("07:00").do(notify_upcoming_assignments)

# Initial call to fetch and display assignments
notify_upcoming_assignments()

# Keep the script running to check the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
    