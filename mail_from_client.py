import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
smtp_server = 'localhost'
smtp_port = 25  # Change to 25 if you're using the standard SMTP port
sender_email = 'sender_test@example.com'
receiver_email = 'recipient_test@example.com'
subject = 'Test Email'
body = 'This is a test email sent from Python.'

# Create the MIME email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

try:
    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection if using port 587
    # server.login('your_username', 'your_password')  # Use this if authentication is required
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()