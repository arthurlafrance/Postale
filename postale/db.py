#!/usr/bin/python3

# db.py: manages database interaction in Postale
# Written by Arthur Lafrance in February 2020

import sqlite3

from mailman import models


_TABLES = {
    'mailbox' : {
        'url' : 'VARCHAR(50)', 
        'address' : 'VARCHAR(100)', 
        'password' : 'VARCHAR(50)'
    },
    'message' : {
        'sender' : 'VARCHAR(100)',
        'subject' : 'VARCHAR(250)',
        'content' : 'TEXT(5000)',
    },
    'recipient' : {
        'message' : 'INTEGER',
        'address' : 'VARCHAR(100)',
    },
}



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

    _setup_db(cursor)

    return cursor


def _setup_db(cursor: sqlite3.Cursor):
    '''Set up the database (if it was just created)'''
    
    table_exists_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
    
    for table, fields in _TABLES.items():
        cursor.execute(table_exists_query, (table,))
    
        if cursor.fetchone() == None:
            _create_table(cursor, table)
        else:
            if _get_schema_for_table(cursor, table) != _TABLES[table]:
                cursor.execute(f'DROP TABLE {table}')
                _create_table(cursor, table)     


def _create_table(cursor: sqlite3.Cursor, table: str):
    '''Create the table with the given name'''

    create_query = f'CREATE TABLE {table}(' + ', '.join([field + ' ' + value for field, value in _TABLES[table].items()]) + ');'
    cursor.execute(create_query)


def _get_schema_for_table(cursor: sqlite3.Cursor, table: str) -> {str : str}:
    '''Query and return the schema for the given table'''
    
    cursor.execute(f'PRAGMA TABLE_INFO({table});')
    return {schema[1] : schema[2] for schema in cursor.fetchall()}