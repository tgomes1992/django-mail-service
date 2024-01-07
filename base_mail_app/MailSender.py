import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class GmailFileSender:

    def __init__(self):
        self.sender_email = 'tt7.thiago@gmail.com'
        self.sender_password = os.environ.get("MAIL_PASSWORD")

    def send_email(self, to_email, subject, body, file_path):

        # Create the MIME object
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))

        # Attach the file
        attachment = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_path}')
        msg.attach(part)

        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log in to the sender's Gmail account
        server.login(self.sender_email, self.sender_password)

        # Send the email
        server.sendmail(self.sender_email, to_email, msg.as_string())

        # Quit the server
        server.quit()
