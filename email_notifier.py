import os
import smtplib
import zipfile
import configparser
from datetime import date
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

config = configparser.ConfigParser()
config.read('config.ini')

load_dotenv()

def send_email(subject, body, attachments=None):
    sender_email = os.getenv('sender_email')
    receiver_email = ['sunilghimire64@gmail.com', 'info@sunilghimire.com.np']
    password = os.getenv('password')

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = ", ".join(receiver_email)

    text = MIMEText(body)
    message.attach(text)

    if attachments:
        print(attachments)
        for f in attachments:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=os.path.basename(f)
                )
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(f)}"'
                message.attach(part)

    server = smtplib.SMTP(host='smtp.corp.netapp.com', port=587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

def main_program():
    # Your main program logic goes here
    print("Main program started")
    print('Running EMAIL NOTIFICATION PROGRAM')
    print("Main program finished")

if __name__ == '__main__':
    # Send email notification before running the main program
    subject = f"Monthly Performance Script Running | {str(date.today())}"
    body = "Performance Script program is about to start"
    send_email(subject, body)
    attachments = [config.get('path', 'log_path'), config.get('path', 'sample_txt')]
    updated_attachments = []
    
    for attachment in attachments:
        if attachment.endswith('.log'):
            zip_file = zipfile.ZipFile(f'{os.path.splitext(attachment)[0]}.zip', 'w', zipfile.ZIP_DEFLATED)
            zip_file.write(attachment)
            zip_file.close()
            updated_attachments.append(f'{os.path.splitext(attachment)[0]}.zip')
        else:
            updated_attachments.append(attachment)
    main_program()
    print('Running EMAIL NOTIFICATION PROGRAM')
    subject = f"Monthly Performance Script Running | {str(date.today())}"
    body = "Performance Script program has finished running"
    send_email(subject, body, updated_attachments)

