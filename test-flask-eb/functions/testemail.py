"""import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def generate_otp():
    return random.randint(100000, 999999)
def send_email(receiver_email):
    otp = generate_otp()
    sender_email = 'chintan222005@gmail.com'
    sender_password = 'iwuz nuqp szcw dtfr'
    subject = 'Test Email'
    message = f'This is a test email sent from Python. \n Your Otp is {otp}'
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject
    email_message.attach(MIMEText(message, 'plain'))
    smtp_server.send_message(email_message)
    smtp_server.quit()
    return otp
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

def send_email(receiver_email):
    # Define the JSON object you want to send
    json_body = {
        "name": "John Doe",
        "email": receiver_email,
        "message": "This is a test email containing JSON data.",
        "status": "success"
    }

    # Convert the JSON object to a string
    json_str = json.dumps(json_body, indent=4)

    # Email details
    sender_email = 'chintan222005@gmail.com'
    sender_password = 'iwuz nuqp szcw dtfr'  # Make sure to store this securely
    subject = 'Test Email with JSON Body'
    message = f'Here is the JSON data:\n\n{json_str}'

    # Setting up SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)

    # Create the email message
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject

    # Attach the JSON string as the email body
    email_message.attach(MIMEText(message, 'plain'))

    # Send the email
    smtp_server.send_message(email_message)
    smtp_server.quit()

    print(f"Email sent to {receiver_email}")

# Example usage
send_email('ankurvasani2585@gmail.com')
