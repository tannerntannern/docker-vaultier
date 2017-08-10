import smtplib
from email.mime.text import MIMEText

#
# A basic Mailtrap send_mail implementation.
#
def send_mail(from_email, to_emails, subject, plain_body, html_body):
    """
    Feel free to override me!

    :param from_email: The sender's email address.  NOTE that this may
        be flat-out incorrect, but it is what Vaultier thinks it is.
    :param to_emails: List of the recipients' email addresses.  Unlike
        from_email, this should be correct.
    :param subject: The email subject
    :param plain_body: Plain text version of the email body
    :param html_body: HTML version of the email body
    """

    # Mailtrap username and password goes here
    username = 'CHANGE ME'
    password = 'CHANGE ME'

    # Fix incorrect site url in message.  You can discard this code
    # and write your own cleaning code if you wish.
    wrong_domain = 'example.com'
    wrong_url = 'http://' + wrong_domain
    real_domain = 'example.com'     # your domain here
    real_url = 'https://' + real_domain

    plain_body = plain_body.replace(wrong_url, real_url)
    plain_body = plain_body.replace(wrong_domain, real_domain)
    html_body = html_body.replace(wrong_url, real_url)
    html_body = html_body.replace(wrong_domain, real_domain)
    from_email = from_email.replace(wrong_domain, real_domain)

    # Build message
    msg = MIMEText(plain_body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)

    # The actual mail send
    server = smtplib.SMTP('mailtrap.io', 2525)
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg.as_string())
    server.quit()
