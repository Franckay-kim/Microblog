from threading import Thread
from flask import render_template
from flask_mail import Message
from flask_babel import _
from app import app, mail


# send emails asynchronously
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# email sending wrapper function
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    # msg = Message("Hello, Reset your password",
    #               sender="from@example.com",
    #               recipients=["to@example.com"])
    # mail.send(msg)
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
