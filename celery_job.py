from app import create_app, db, mail
from app import User, Ledger
from celery import Celery, schedules
from flask_mail import Message
from sqlalchemy import extract, func
from flask import render_template

from datetime import datetime, timedelta

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

    sender.add_periodic_task(
        schedules.crontab(minute='*/2'),
        send_monthly_activity_report.s(),
    )

# @celery.task
# def send_email_to_all_users():
#     with app.app_context():
#         users = User.query.all()
#         for user in users:
#             email_data = {
#                 'subject': 'Visit the shopping site!!',
#                 'sender': 'ap539813@gmail.com',
#                 'recipient': user.email,
#                 'body': 'Visit the website to do some shopping!!'
#             }
#             send_async_email.delay(email_data)

@celery.task
def send_async_email_report(email_data):
    with app.app_context():
        msg = Message(
            subject=email_data['subject'],
            sender=email_data['sender'],
            recipients=[email_data['recipient']],
            html=email_data['html_body']  
        )
        mail.send(msg)

@celery.task
def send_monthly_activity_report():
    with app.app_context():
        # Determine the last month
        today = datetime.utcnow()
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)

        print(first_day_last_month)
        print(last_day_last_month)

        # Query all users
        users = User.query.all()

        for user in users:
            # Query total expenditure for the last month for each user
            total_expenditure = db.session.query(func.sum(Ledger.rate * Ledger.quantity)).filter(
                Ledger.user_id == user.username,
                extract('year', Ledger.purchase_date) == first_day_last_month.year,
                extract('month', Ledger.purchase_date) == first_day_last_month.month
            ).scalar() or 0

            # Create a list of orders for the user in the last month
            orders = Ledger.query.filter(
                Ledger.user_id == user.username,
                Ledger.purchase_date >= first_day_last_month,
                Ledger.purchase_date <= last_day_last_month
            ).all()

            # Render an HTML template for the email body
            html_body = render_template('monthly_report.html', orders=orders, total_expenditure=total_expenditure)

            # Prepare email data
            email_data = {
                'subject': f'Monthly Activity Report for {first_day_last_month.strftime("%B %Y")}',
                'sender': 'ap539813@gmail.com',
                'recipient': user.email,
                'html_body': html_body
            }

            # Send the email
            send_async_email_report.delay(email_data)




@celery.task
def send_email_to_all_users():
    with app.app_context():
        today = datetime.utcnow().date()

        users = User.query.all()
        for user in users:
            # Check if the user has made a purchase today
            purchase_today = Ledger.query.filter(
                Ledger.user_id == user.username,
                db.func.date(Ledger.purchase_date) == today
            ).first()

            print(purchase_today)

            # If no purchase today, send an email
            if not purchase_today:
                email_data = {
                    'subject': 'Visit the shopping site!!',
                    'sender': 'ap539813@gmail.com',
                    'recipient': user.email,
                    'body': 'Visit the website to do some shopping!!'
                }
                send_async_email.delay(email_data)