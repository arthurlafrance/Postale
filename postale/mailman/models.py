#!/usr/bin/python3

# models.py: defines the models used throughout Postale
# Written by Arthur Lafrance in February 2020


class Mailbox:
    def __init__(self, id: int, url: str, addr: str, password: str):
        self.id = id

        self.url = url
        self.addr = addr
        self.password = password

    def export(self) -> tuple:
        '''Export the Mailbox to a tuple of field values, ready to be used in SQL'''

        return (self.url, self.addr, self.password)

    def __eq__(self, mailbox) -> bool:
        if type(mailbox) == Mailbox:
            return self.id == mailbox.id and self.export() == mailbox.export()
        else:
            return NotImplemented

    def __str__(self) -> str:
        return f'{self.url}: {self.addr} - {self.password}'

    def __repr__(self) -> str:
        return f'Mailbox({self.id}, {self.url}, {self.addr}, {self.password})'

    @staticmethod
    def from_data(id: int, data: tuple):
        url, addr, password = data
        
        return Mailbox(id, url, addr, password)


class Message:
    def __init__(self, id: int, sender: str, recipients: [str], subject: str, content: str, is_draft=False):
        self.id = id

        self.sender = sender
        self.recipients = recipients

        self.subject = subject
        self.content = content

        self.is_draft = is_draft

    def export(self) -> tuple:
        '''Export the Message to a tuple of field values, ready to be used in SQL'''

        return (self.sender, self.subject, self.content, 1 if self.is_draft else 0)

    def __eq__(self, message) -> bool:
        if type(message) == Message:
            return self.id == message.id and self.export() == message.export() and self.recipients == message.recipients
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f'Message({self.id}, {repr(self.sender)}, {self.recipients}, {repr(self.subject)}, {repr(self.content)}, {self.is_draft})'

    @staticmethod
    def from_data(id: int, data: tuple, recipients: [str]):
        sender, subject, content, is_draft = data
        
        return Message(id, sender, recipients, subject, content, is_draft == 1)