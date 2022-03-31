#!/usr/bin/python2
import smtplib
import os, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(to, subject, text, fr="", f="", cc=[], bcc=[], server="localhost"):
    assert type(to)==list
    assert type(cc)==list
    assert type(bcc)==list

    message = MIMEMultipart()
    message['From'] = fr
    message['To'] = COMMASPACE.join(to)
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = subject
    message['Cc'] = COMMASPACE.join(cc)

    message.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(f, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    message.attach(part)

    addresses = []
    for x in to:
        addresses.append(x)
    for x in cc:
        addresses.append(x)
    for x in bcc:
        addresses.append(x)

    smtp = smtplib.SMTP(server, port=2025)
    smtp.sendmail('ryabov@infowatch.com', addresses, message.as_string())
    smtp.close()
m_body = """<!DOCTYPE html>
<html>
<body>

<h1>My First Heading</h1>

<p>My first paragraph.</p>

</body>
</html>"""

files = [fff for fff in os.listdir('.') if os.path.isfile(fff)]
for ff in files:
  print ff
  send_mail(['maps@2email.com',], ff, m_body, fr='maps@infowatch.com', f=sys.argv[1]+ff, server='ryabov-tm7.infowatch.ru')

print sys.argv
