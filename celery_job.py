from app import create_app, db, mail
from app import User
from celery import Celery, schedules
from flask_mail import Message

app = create_app()
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def send_async_email(email_data):
    with app.app_context():
        msg = Message(email_data['subject'],
                      sender=email_data['sender'],
                      recipients=[email_data['recipient']])
        msg.body = email_data['body']
        mail.send(msg)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        schedules.crontab(minute='*/2'),
        send_email_to_all_users.s(),
    )

@celery.task
def send_email_to_all_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            email_data = {
                'subject': 'Visit the shopping site!!',
                'sender': 'ap539813@gmail.com',
                'recipient': user.email,
                'body': 'Visit the website to do some shopping!!'
            }
            send_async_email.delay(email_data)