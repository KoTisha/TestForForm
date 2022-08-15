# from celery import task
from testforform.celery import app
from django.core.mail import EmailMessage

@app.task
def send_email(title, message, file=None):
    email = EmailMessage(
        title,
        message,
        'admin@example.com',
        ['admin@example.com'],
    )

    if file:
        try:
            email.attach(file.name, file.read(),file.content_type)
        except:
            return "Attachment error"
    email.send()
    return 'OK!'