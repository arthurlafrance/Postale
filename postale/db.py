#!/usr/bin/python3

# db.py: manages database interaction in Postale
# Written by Arthur Lafrance in February 2020

import sqlite3

from mailman import models

class PostaleSQLiteClient:
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


    def __init__(self):
        connection = sqlite3.connect('postale.db')
        self.cursor = connection.cursor()

        self._setup_db()

    # Mailboxes
    def get_mailboxes(self, id=0, url='', addr='', password='') -> [models.Mailbox]:
        '''Get a list of all mailboxes'''
        
        self.cursor.execute('SELECT rowid, * FROM mailbox') # add WHERE
        rows = self.cursor.fetchall()

        mailboxes = []

        for row in rows:
            mailboxes.append(models.Mailbox.from_data(row[0], row[1:]))

        return mailboxes

    def get_mailbox_with_id(self, id: int) -> models.Mailbox:
        '''Get the mailbox with the given ID (a convenience method wrapping around get_mailboxes)'''

        result = get_mailboxes(self.cursor, id=id)
        return result[0] if len(result) > 0 else None

    def write_mailbox(self, mailbox: models.Mailbox):
        '''Add a mailbox to the database'''
        
        query = 'INSERT INTO mailbox(' + ', '.join(PostaleSQLiteClient._TABLES['mailbox']) + ') VALUES (' + ', '.join(['?'] * len(PostaleSQLiteClient._TABLES['mailbox'])) + ');'
        self.cursor.execute(query, mailbox.export())

    def delete_mailbox(self, mailbox: models.Mailbox):
        '''Remove a mailbox from the database'''
        
        query = 'DELETE FROM mailbox WHERE rowid=?;'
        self.cursor.execute(query, (mailbox.id,))


    # Messages
    def get_messages(self, mailboxes=None, criteria_goes_here=None) -> [models.Message]:
        '''Get all stored messages from the given mailbox(es) matching the given criteria'''

        self.cursor.execute('SELECT rowid, * FROM message;') # add WHERE
        rows = self.cursor.fetchall()

        messages = []

        for row in rows:
            message_id = row[0]
            recipients = self._get_recipients_for_message(message_id)

            messages.append(models.Message.from_data(message_id, row[1:], recipients))

        return messages

    def write_messages(self, messages: [models.Message]): # (or update_messages)
        '''Save the given messages to the database (or update them in the database if they exist)'''
        
        for message in messages:
            self.write_message(message)

    def write_message(self, message: models.Message): # saves new message or updates existing one
        '''Save the given message to the database, or update the existing message entry if it exists'''
        
        insert_query = 'INSERT INTO message(' + ', '.join(PostaleSQLiteClient._TABLES['message']) + ') VALUES(' + ', '.join(['?'] * len(PostaleSQLiteClient._TABLES['message'])) + ');'
        self.cursor.execute(insert_query, message.export())

        self._write_recipients_for_message(message.id, message.recipients)

    def delete_message(self, message: models.Message):
        '''Delete the given message from the database'''
        
        query = 'DELETE FROM message WHERE rowid=?;'
        self.cursor.execute(query, (message.id,))

        self._delete_recipients_for_message(message.id)

    def _get_recipients_for_message(self, message_id: int) -> [str]:
        '''Get a list of all recipients for the message with the given ID'''
        
        self.cursor.execute('SELECT address FROM recipient WHERE message=?;', (message_id,))
        return [row[0] for row in self.cursor.fetchall()]

    def _write_recipients_for_message(self, message_id: int, recipients: [str]):
        '''Write the recipient list into the database'''

        insert_query = 'INSERT INTO recipient(' + ', '.join(PostaleSQLiteClient._TABLES['recipient']) + ') VALUES(' + ', '.join(['?'] * len(PostaleSQLiteClient._TABLES['recipient'])) + ');'
        
        for recipient in recipients:
            self.cursor.execute(insert_query, (message_id, recipient))

    def _delete_recipients_for_message(self, message_id: int):
        '''Delete all recipients for the message with the given ID from the database'''

        query = 'DELETE FROM recipient WHERE message=?;'
        self.cursor.execute(query, (message_id,))


    # Logistics
    def _setup_db(self):
        '''Set up the database (if it was just created)'''
        
        table_exists_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        
        for table, fields in PostaleSQLiteClient._TABLES.items():
            self.cursor.execute(table_exists_query, (table,))
        
            if self.cursor.fetchone() == None:
                self._create_table(table)
            else:
                if self._get_schema_for_table(table) != PostaleSQLiteClient._TABLES[table]:
                    self.cursor.execute(f'DROP TABLE {table}')
                    _create_table(table)  

    def _create_table(self, table: str):
        '''Create the table with the given name'''

        create_query = f'CREATE TABLE {table}(' + ', '.join([field + ' ' + value for field, value in PostaleSQLiteClient._TABLES[table].items()]) + ');'
        self.cursor.execute(create_query)

    def _get_schema_for_table(self, table: str) -> {str : str}:
        '''Query and return the schema for the given table'''
        
        self.cursor.execute(f'PRAGMA TABLE_INFO({table});')
        return {schema[1] : schema[2] for schema in self.cursor.fetchall()}
