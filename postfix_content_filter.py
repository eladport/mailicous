import sys
import email
import json
import requests
from email import policy
from email.parser import BytesParser
import logging

def email_to_json(email_message):
    def get_body(message):
        if message.is_multipart():
            for part in message.iter_parts():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            return message.get_payload(decode=True).decode('utf-8', errors='ignore')

    email_json = {
        "from": email_message["From"],
        "to": email_message["To"],
        "subject": email_message["Subject"],
        "date": email_message["Date"],
        "body": get_body(email_message)
    }

    return json.dumps(email_json, indent=4)

def main():
    logging.basicConfig(filename='/var/log/postfix_content_filter.log', level=logging.INFO)
    raw_email = sys.stdin.read()
    logging.info('Received message:\n%s', raw_email)
    email_message = BytesParser(policy=policy.default).parsebytes(raw_email.encode('utf-8'))
    email_json = email_to_json(email_message)
    logging.info('JSON message:\n%s', email_json)
    base_url = 'http://127.0.0.1:5000'

    # Credentials for authentication
    username = 'test'
    password = 'test'

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
        # Extract the access token from the response
        access_token = response.json()['access_token']
        #print(f"Access Token: {access_token}")
        headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
        }
        detection_server_url = "http://127.0.0.1:5000/analyze"
        response_email = requests.post(detection_server_url,headers=headers, data={
            'email': email_json
            })
        #print(email_json)

        # Process the response
        if response.text.strip() == 'REJECT':
            sys.exit(1)

        else:
            sys.exit(0)

    else:
        print(f"Failed to login: {response.json()}")


if __name__ == "__main__":
    main()