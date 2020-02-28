#!/usr/bin/python3

# models.py: defines the models used throughout Postale
# Written by Arthur Lafrance in February 2020


class Mailbox:
    def __init__(self, url: str, addr: str, password: str):
        self.url = url

        self.addr = addr
        self.password = password

    def export(self) -> tuple:
        '''Export the Mailbox to a tuple of field values, ready to be used in SQL'''

        return (self.url, self.addr, self.password)

    def __eq__(self, mailbox) -> bool:
        if type(mailbox) == Mailbox:
            return self.url == mailbox.url and self.addr == mailbox.addr and self.password == mailbox.password
        else:
            return NotImplemented

    def __str__(self) -> str:
        return f'{self.url}: {self.addr} - {self.password}'

    @staticmethod
    def from_data(data: tuple):
        url, addr, password = data
        
        return Mailbox(url, addr, password)


class Message:
    def __init__(self, sender: str, recipients: [str], subject: str, content: str, is_draft=False):
        self.sender = sender
        self.recipients = recipients

        self.subject = subject
        self.content = content

        self.is_draft = is_draft

    @staticmethod
    def from_data(data: tuple, recipients: [str]):
        sender, subject, content, is_draft = data
        
        return Message(sender, recipients, subject, content, is_draft)