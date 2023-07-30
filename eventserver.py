from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import smtplib
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Replace the following values with your email credentials
EMAIL_FROM = 'hamza2272001@gmail.com'
EMAIL_TO = 'hamzakhan22072001@gmail.com'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Load or create the credentials
creds_file = 'gmail_credentials.json'
creds = None
if os.path.exists(creds_file):
    creds = Credentials.from_authorized_user_file(creds_file, SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open(creds_file, 'w') as creds_json:
        creds_json.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)

@app.route('/register', methods=['GET'])
def register():
    try:
        name = request.args.get('name')
        contact_number = request.args.get('contact_number')
        cnic = request.args.get('cnic')
        event_type = request.args.get('event_type')
        event_venue = request.args.get('event_venue')
        event_date = request.args.get('eventDate')
        event_start_time = request.args.get('eventStartTime')
        event_end_time = request.args.get('eventEndTime')
        number_of_guests = request.args.get('numberOfGuests')
        payment = request.args.get('paymentOption')

        body = f"Name: {name}\nContact Number: {contact_number}\nCNIC: {cnic}\nEvent Type: {event_type}\n" \
               f"Event Venue: {event_venue}\nEvent Date: {event_date}\nEvent Start Time: {event_start_time}\n" \
               f"Event End Time: {event_end_time}\nNumber of Guests: {number_of_guests}\nPayment Option: {payment}"

        msg = MIMEText(body)
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = "Automated Event Registration Form Submission"

        # Send the email using the Gmail API
        message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
        service.users().messages().send(userId='me', body=message).execute()

        return jsonify({'message': 'Form data sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
