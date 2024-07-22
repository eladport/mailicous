import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
smtp_server = 'localhost'
smtp_port = 25  # Change to 25 if you're using the standard SMTP port
sender_email = 'bob@example.com'
receiver_email = 'alice@example.com'
dkim_signature = """v=1; a=rsa-sha256; c=relaxed/simple; d=example.com; s=default;
  t=1620244561; bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;
  h=From:To:Subject:Date:Message-ID;
  b=Ib2g1ozUSUyXIn4K5JZQkdxIgzH2nFP/E2kzOcItSLi9pWQXOHozNco76E/xyfiN1
   EN+6CI7gDfprN1FsOmkaerEqC/UHfPqIfa4JIRp8HU0w0sQ8j0BD8A/um8BsMGnElH
   p8WzVPOWvnt6L7E4u5O38A08Q/AlrNlXit+bVDeT48s="""
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
spf_result = 'pass (example.com: domain of sender@example.com designates 192.0.2.1 as permitted sender)'

subject_malicious = 'Crypto offer for 500$!!'

MALICIOUS_EMAIL_CONTENT = f"""
                        One time offer! this offer won't repeat!
                        """

# Create the MIME email
msg_benign = MIMEMultipart()
msg_benign['From'] = sender_email
msg_benign['To'] = receiver_email
msg_benign['Subject'] = subject_benign
msg_benign.attach(MIMEText(body_benign, 'plain'))
msg_benign['Received-SPF'] = f'{spf_result} receiver={receiver_email}; client-ip=192.0.2.1; envelope-from={sender_email}; helo=mail.sender.com;'
msg_benign['DKIM-Signature'] = dkim_signature

msg_malicious = MIMEMultipart()
msg_malicious['From'] = sender_email
msg_malicious['To'] = receiver_email
msg_malicious['Subject'] = subject_malicious
msg_malicious.attach(MIMEText(MALICIOUS_EMAIL_CONTENT, 'plain'))
msg_malicious['Received-SPF'] = f'{spf_result} receiver={receiver_email}; client-ip=192.0.2.1; envelope-from={sender_email}; helo=mail.sender.com;'
msg_malicious['DKIM-Signature'] = dkim_signature

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