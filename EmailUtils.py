import codecs
import json
import smtplib
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formataddr

from email.mime.multipart import MIMEMultipart


class EmailUtil(object):

    def __init__(self, sender, receiver, msg_title, content, sender_server, port, From, To, mail_pass, files):
        self.sender = sender
        self.receiver = receiver
        self.msg_title = msg_title
        self.sender_server = sender_server
        self.port = port
        self.content = content
        self.From = From
        self.To = To
        self.mail_pass = mail_pass
        self.files = files

    def send(self):
        try:
            msg = MIMEMultipart()
            # todo
            msg['From'] = formataddr([self.From, self.sender])
            msg['To'] = formataddr([self.To, self.receiver])
            msg['Subject'] = self.msg_title
            txt = MIMEText(self.content, 'html', 'utf-8')
            msg.attach(txt)

            for file in self.files:
                file_name = file[0]
                file_path = file[1]
                if file_name.endswith('.pdf'):
                    f = codecs.open(file_path, 'rb')
                    content = f.read()
                    f.close()
                    attach = MIMEApplication(content)
                    attach.add_header('Content-Disposition', 'attachment', filename=file_name)
                    msg.attach(attach)
                if file_name.endswith('.png'):
                    with open(file_path, 'rb') as f:
                        mime = MIMEBase('image', 'png', filename=file_name)
                        mime.add_header('Content-Disposition', 'attachment', filename=file_name)
                        mime.add_header('Content-ID', '<0>')
                        mime.add_header('X-Attachment-Id', '0')

                        content = f.read()
                        f.close()
                        mime.set_payload(content)

                        encoders.encode_base64(mime)

                        msg.attach(mime)
            EmailUtil.server = smtplib.SMTP(self.sender_server, self.port, timeout=10)
            EmailUtil.server.ehlo()
            EmailUtil.server.starttls()
            EmailUtil.server.login(self.sender, self.mail_pass)
            EmailUtil.count = EmailUtil.count % 5
            response = EmailUtil.server.sendmail(self.sender, self.receiver, msg.as_string())
            print(response)
            EmailUtil.server.quit()
            return True

        except Exception as e:
            print(e)
            return False
