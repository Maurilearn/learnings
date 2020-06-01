import smtplib

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


def send_mail(toaddr, subject, body):
    try:
        from flask import current_app
        fromaddr = current_app.config['SMTP_MAIN_MAIL']
        toaddr = toaddr
        thesub = subject
        thebody = body
        thepassword = current_app.config['SMTP_PASS']
        domsmtp = current_app.config['SMTP_HOST']
        smtpport = current_app.config['SMTP_PORT'] #needs integer not string

        msg = MIMEMultipart('alt text here')
        msg.set_charset('utf8')
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = Header(thesub,'utf8')
        _attach = MIMEText(thebody.encode('utf8'),'html','UTF-8')
        msg.attach(_attach)
        try:
            server = smtplib.SMTP(domsmtp, smtpport)
        except ConnectionRefusedError:
            print('Mail could not be sent!')
            return
        if domsmtp != 'localhost':
            server.starttls()
            server.login(fromaddr, thepassword)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)

        server.quit()
    except Exception as e:
        print(e)
