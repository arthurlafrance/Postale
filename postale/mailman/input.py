#!/usr/bin/python3

# mailman/input.py: handles mail-related input tasks (especially IMAP usage)
# Written by Arthur Lafrance in February 2020

import imaplib

import models

def authenticate(url: str, addr: str, password: str) -> bool:
    '''Authenticate the given user using IMAP, returning whether or not the login succeeds'''
    pass

def fetch_mail(mailbox: models.Mailbox):
    '''Fetch mail from the given mailbox using IMAP'''
    pass