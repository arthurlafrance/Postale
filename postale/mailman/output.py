#!/usr/bin/python3

# mailman/output.py: handles mail-related output tasks (especially SMTP usage)
# Written by Arthur Lafrance in February 2020

import smtplib

import models

def authenticate(url: str, addr: str, password: str) -> bool:
    '''Authenticate the given user using SMTP, returning whether or not the login succeeds'''
    pass

def send_mail(message: models.Message):
    '''Send the given message using SMTP (identifying the correct mailbox to send from)'''
    pass