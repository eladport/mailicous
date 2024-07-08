import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
smtp_server = 'localhost'
smtp_port = 25  # Change to 25 if you're using the standard SMTP port
sender_email = 'sender_test@example.com'
receiver_email = 'recipient_test@example.com'
subject_benign = 'Benign Email'
body_benign = """
                Hello my dear company,
                Just wanted to take a minute to say to you all what a great quarter we had!
                Sales are better than ever, and our product keeps evolving!
                Keep on the good work!
                Yours sincerely,
                    Steve,
                    HR department
       """
subject_malicious = 'malicious mail'
SAFE_PLACEHOLDER = "<<safe_placeholder>>"
# splitted with safe placeholder to avoid clicking
MAL_URL = "https://url" + SAFE_PLACEHOLDER + "z.fr/q2Py"

MALICIOUS_EMAIL_CONTENT = f"""
                        Hey all!
                        unfortunatly our wonderful boss is leaving us for another company,
                        he gave us a nice goodbye present right here:
                        {MAL_URL.replace(SAFE_PLACEHOLDER, "")}
                        please get in and help yourself!
                        """

# Create the MIME email
msg_benign = MIMEMultipart()
msg_benign['From'] = sender_email
msg_benign['To'] = receiver_email
msg_benign['Subject'] = subject_benign
msg_benign.attach(MIMEText(body_benign, 'plain'))

msg_malicious = MIMEMultipart()
msg_malicious['From'] = sender_email
msg_malicious['To'] = receiver_email
msg_malicious['Subject'] = subject_malicious
msg_malicious.attach(MIMEText(MALICIOUS_EMAIL_CONTENT, 'plain'))

try:
    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection if using port 587
    
    # send benign mail
    server.sendmail(sender_email, receiver_email, msg_benign.as_string())
    print(sender_email, receiver_email, msg_benign.as_string())
    
    # send malicious mail
    server.sendmail(sender_email, receiver_email, msg_malicious.as_string())
    print(sender_email, receiver_email, msg_malicious.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()