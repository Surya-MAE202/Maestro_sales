import datetime
from sqlalchemy.orm import Session
import random
from app.core.config import settings
from datetime import datetime, timedelta, date, time
import string
from app.core.config import settings
from app.models import *
from sqlalchemy import or_, and_
from pyfcm import FCMNotification
import sys
import math
import os
import shutil
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import smtplib
from email_validator import validate_email, EmailNotValidError
import tracemalloc
from email.mime.text import MIMEText


async def send_mail(receiver_email, message):  # Demo
    sender_email = "maestronithishraj@gmail.com"
    receiver_email = receiver_email
    password = "ycjanameheveewtb"

    msg = MIMEText(message)

    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Maestro Sales & Management"

    # msg = str(message)
    print(msg)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.ehlo()
    # server.starttls()
    # server.login(sender_email, password)
    # server.sendmail(sender_email, receiver_email, msg)
    # server.quit()

    return True



def pagination(row_count=0, page=1, size=10):
    current_page_no = page if page >= 1 else 1

    total_pages = math.ceil(row_count / size)

    if current_page_no > total_pages:
        current_page_no = total_pages

    limit = current_page_no * size
    offset = limit - size

    if limit > row_count:
        limit = offset + (row_count % size)

    limit = limit - offset

    if offset < 0:
        offset = 0

    return [limit, offset]


def get_pagination(row_count=0, current_page_no=1, default_page_size=10):
    current_page_no = current_page_no if current_page_no >= 1 else 1

    total_pages = math.ceil(row_count / default_page_size)

    if current_page_no > total_pages:
        current_page_no = total_pages

    limit = current_page_no * default_page_size
    offset = limit - default_page_size

    if limit > row_count:
        limit = offset + (row_count % default_page_size)

    limit = limit - offset

    if offset < 0:
        offset = 0

    return [total_pages, offset, limit]


def paginate(page, size, data, total):
    reply = {"items": data, "total": total, "page": page, "size": size}
    return reply


def paginate_for_file_count(page, size, data, total, file_count):
    reply = {"items": data, "total": total, "page": page,
             "file_count": file_count, "size": size}
    return reply