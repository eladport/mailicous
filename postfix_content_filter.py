import sys
import email
import json
import requests
from email import policy
from email.parser import BytesParser
from email.mime.text import MIMEText
from email import encoders
import smtplib
import logging

def email_to_json(email_message):
    def get_body(message):
        if message.is_multipart():
            payloads = []
            for part in message.iter_parts():
            
                # skip on the first content type because we need the second
                if "===============" not in part.get_content_type():
                
                    # return content type and body
                    payloads.append((part.get_content_type(),part.get_payload(decode=True).decode('utf-8', errors='ignore')))
            return payloads
        else:
            return [(message.get_content_type(),message.get_payload(decode=True).decode('utf-8', errors='ignore'))]
    
    # parse content type and body in case of a message with attachment
    email_content = get_body(email_message)
    content_type = email_content[0][0]
    body = email_content[0][1]
    attachment = []
    
    # in case of multiple attachments, add them to a list
    if len(email_content) > 1:
        for i in range(1,len(email_content)):
            attachment.append(((email_content[i][0]),(base64.b64encode(email_content[i][1].encode())).decode()))
    
    email_json = {
        "from": email_message["From"],
        "to": email_message["To"],
        "subject": email_message["Subject"],
        "date": email_message["Date"],
        "DKIM-Signature": email_message['DKIM-Signature'],
        "Received-SPF": email_message['Received-SPF'],
        "Content-Type": content_type,
        "body": body,
        "attachment": attachment
    }

    # return mail fields as json, accept unicode characters
    return json.dumps(email_json, indent=4,ensure_ascii=False)

def send_rejection_email(sender):
    msg = MIMEText(f"Your email has been rejected.")
    msg["Subject"] = "Email Rejected"
    msg["From"] = "noreply@example.com"
    msg["To"] = sender

    with smtplib.SMTP("localhost") as server:
        server.sendmail("noreply@example.com", [sender], msg.as_string())
        
def main():
    logging.basicConfig(filename='/var/log/postfix_content_filter.log', level=logging.INFO)
    raw_email = sys.stdin.read()
    logging.info('Received mail:\n%s', raw_email)
    
    # parse the email and select the intresting fields as JSON
    email_message = BytesParser(policy=policy.default).parsebytes(raw_email.encode('utf-8'))
    email_json = email_to_json(email_message)
    base_url = 'http://127.0.0.1:5000'

    # Credentials for authentication
    username = 'poc@user.com'
    password = 'POCPass123!'

    # Login endpoint URL
    login_url = f'{base_url}/login'

    # JSON data for login request
    login_data = {
        'username': username,
        'password': password
    }

    # Send POST request to login endpoint
    response = requests.post(login_url, json=login_data)

    # Check if login was successful
    if response.status_code == 200:

        #Extract the access token from the response
        access_token = response.json()['access_token']
        headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
        }
        detection_server_url = "http://127.0.0.1:5000/analyze"
        response_email = requests.post(detection_server_url,headers=headers, data={
            'email': email_json
            })


        # Process the response
        logging.info("response:%s\n", response_email.json())
        if response_email.json()['verdict'] == 'REJECT':
            logging.info('Verdict: Reject\n')
            #send_rejection_email(response_email.json()['from'])
            sys.exit(1)

        else:
            logging.info('Verdict: Accept\n')
            sys.exit(0)

    else:
        print(f"Failed to login: {response.json()}")


if __name__ == "__main__":
    main()