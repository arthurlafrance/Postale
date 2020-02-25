#!/usr/bin/python3

# db.py: manages database interaction in Postale
# Written by Arthur Lafrance in February 2020

import sqlite3

from mailman import models


# Accounts
def add_mailbox(mailbox: models.Mailbox):
    '''Add a mailbox to the database'''
    pass

def remove_mailbox(mailbox: models.Mailbox):
    '''Remove a mailbox from the database'''
    pass

def get_mailboxes() -> [models.Mailbox]:
    '''Get a list of all mailboxes'''
    pass

def get_mailbox(identifying_fields_go_here) -> models.Mailbox:
    '''Get the mailbox matching the given criteria, if it exists'''
    pass


# Messages/drafts
def get_messages(*mailboxes: [str]) -> [models.Message]:
    '''Get all stored messages from the given mailbox(es)'''
    pass

def select_messages(criteria_goes_here) -> [models.Message]: # (with criteria)
    '''Select all stored messages from the given mailbox(es) matching the given criteria'''
    pass

def save_messages(messages: [models.Message]): # (or update_messages)
    '''Save the given messages to the database (or update them in the database if they exist)'''
    pass 

def save_message(message: models.Message): # saves new message or updates existing one
    '''Save the given message to the database, or update the existing message entry if it exists'''
    pass


# Logistics
def _connect_to_db() -> sqlite3.Cursor:
    '''Connect to the local Postale SQLite database and return the corresponding cursor'''
    connection = sqlite3.connect('postale.db')
    cursor = connection.cursor()

    _setup_db()

    return cursor

def _setup_db():
    '''Set up the database (if it was just created)'''

    # check if each table exists, if correct fields are present
    #   if not, create/update any missing tables
    pass