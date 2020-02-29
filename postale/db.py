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
        'sender' : 'VARCHAR(100)', # also have to store mailbox foreign key/rowid
        'subject' : 'VARCHAR(250)',
        'content' : 'TEXT(5000)',
        'is_draft' : 'INTEGER'
    },
    'recipient' : {
        'message' : 'INTEGER',
        'address' : 'VARCHAR(100)',
    },
}


# Logistics
def connect_to_db() -> sqlite3.Cursor:
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


    
# Mailboxes
def get_mailboxes(cursor: sqlite3.Cursor, id=-1, url='', addr='', password='') -> [models.Mailbox]:
    '''Get a list of all mailboxes'''
    
    cursor.execute('SELECT rowid, * FROM mailbox') # add WHERE
    rows = cursor.fetchall()

    mailboxes = []

    for row in rows:
        mailboxes.append(models.Mailbox.from_data(row[0], row[1:]))

    return mailboxes


def get_mailbox_with_id(cursor: sqlite3.Cursor, id=-1) -> models.Mailbox:
    '''Get the mailbox with the given ID (a convenience method wrapping around get_mailboxes)'''

    result = get_mailboxes(cursor, id=id)
    return result[0] if len(result) > 0 else None


def write_mailbox(cursor: sqlite3.Cursor, mailbox: models.Mailbox):
    '''Add a mailbox to the database'''
    
    query = 'INSERT INTO mailbox(' + ', '.join(_TABLES['mailbox']) + ') VALUES (' + ', '.join(['?'] * len(_TABLES['mailbox'])) + ');'
    cursor.execute(query, mailbox.export())


def delete_mailbox(cursor: sqlite3.Cursor, mailbox: models.Mailbox):
    '''Remove a mailbox from the database'''
    
    query = 'DELETE FROM mailbox WHERE rowid=?;'
    cursor.execute(query, (mailbox.id,))



# Messages
def get_messages(cursor: sqlite3.Cursor, mailboxes=None, criteria_goes_here=None) -> [models.Message]:
    '''Get all stored messages from the given mailbox(es) matching the given criteria'''

    cursor.execute('SELECT rowid, * FROM message;') # add WHERE
    rows = cursor.fetchall()

    messages = []

    for row in rows:
        message_id = row[0]
        recipients = _get_recipients_for_message(cursor, message_id)

        messages.append(models.Message.from_data(message_id, row[1:], recipients))

    return messages

def write_messages(cursor: sqlite3.Cursor, messages: [models.Message]): # (or update_messages)
    '''Save the given messages to the database (or update them in the database if they exist)'''
    
    for message in messages:
        write_message(cursor, message)


def write_message(cursor: sqlite3.Cursor, message: models.Message): # saves new message or updates existing one
    '''Save the given message to the database, or update the existing message entry if it exists'''
    
    insert_query = 'INSERT INTO message(' + ', '.join(_TABLES['message']) + ') VALUES(' + ', '.join(['?'] * len(_TABLES['message'])) + ');'
    cursor.execute(insert_query, message.export())

    _write_recipients_for_message(cursor, message.id, message.recipients)


def delete_message(cursor: sqlite3.Cursor, message: models.Message):
    '''Delete the given message from the database'''
    
    query = 'DELETE FROM message WHERE rowid=?;'
    cursor.execute(query, (message.id,))

    _delete_recipients_for_message(cursor, message.id)


def _get_recipients_for_message(cursor: sqlite3.Cursor, message_id: int) -> [str]:
    '''Get a list of all recipients for the message with the given ID'''
    
    cursor.execute('SELECT address FROM recipient WHERE message=?;', (message_id,))
    return [row[0] for row in cursor.fetchall()]


def _write_recipients_for_message(cursor: sqlite3.Cursor, message_id: int, recipients: [str]):
    '''Write the recipient list into the database'''

    insert_query = 'INSERT INTO recipient(' + ', '.join(_TABLES['recipient']) + ') VALUES(' + ', '.join(['?'] * len(_TABLES['recipient'])) + ');'
    
    for recipient in recipients:
        cursor.execute(insert_query, (message_id, recipient))


def _delete_recipients_for_message(cursor: sqlite3.Cursor, message_id: int):
    '''Delete all recipients for the message with the given ID from the database'''

    query = 'DELETE FROM recipient WHERE message=?;'
    cursor.execute(query, (message_id,))


