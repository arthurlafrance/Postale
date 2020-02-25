#!/usr/bin/python3

# models.py: defines the models used throughout Postale
# Written by Arthur Lafrance in February 2020


class Mailbox:
    def __init__(self, mailbox: str, addr: str, password: str):
        self.mailbox = mailbox

        self.addr = addr
        self.password = password


class Message:
    def __init__(self, sender: str, recipients: [str], subject: str, content: str, is_draft=False):
        self.sender = sender
        self.recipients = recipients

        self.subject = subject
        self.content = content

        self.is_draft = is_draft