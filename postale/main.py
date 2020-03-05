#!/usr/bin/python3

# main.py: the main script for Postale, this file parses and runs commands
# Written by Arthur Lafrance in February 2020

import argparse


class PostaleManager:
    # manages the state of the postale app -- db functions, reading/writing/storing info, etc
    
    _COMMANDS = {
        'login' : self.login,
        'logout' : self.logout,

        'inbox' : self.inbox,
        'mailboxes' : self.mailboxes,
        'outbox' : self.outbox,
        'drafts' : self.drafts,
        'view' : self.view_message,

        'fetch' : self.fetch,
        'new' : self.new,
        'send' : self.send,
    }

    def exec_command(self, command: str, *args):
        '''Execute the command for the given arguments'''
        pass
        

    # Accounts
    def login(self, mailbox: str, addr: str, password: str):
        '''Add a new mailbox to Postale'''
        pass

    def logout(self, addr: str):
        '''Remove the given mailbox from Postale'''
        pass


    # Mailbox views
    def inbox(self, accounts: (str), unread_only=False):
        '''View the selected inbox(es), depending on the provided parameters'''
        pass

    def mailboxes(self):
        '''View a list of all mailboxes in Postale'''
        pass

    def outbox(self, accounts: (str)):
        '''View the selected outbox(es)'''
        pass

    def drafts(self, accounts: (str)):
        '''View the saved drafts for the selected account(s)'''
        pass

    def view_message(self, id: int):
        '''View the content of the message with the given ID'''
        pass


    # Mailbox I/O
    def fetch(self, accounts: (str)):
        '''Fetch any new messages from the selected account(s)'''
        pass

    def new_draft(self, addr: str):
        '''Create a new draft for the given mailbox'''
        pass

    def send(self, id: (int)):
        '''Send the message(s) based on the selected ID(s)'''
        pass


if __name__ == '__main__':
    pass