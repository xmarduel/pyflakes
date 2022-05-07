"""
Provide the class Message and its subclasses.
"""

from pyflakes.messages import Message


class BadIndentation(Message):
    message = "bad indentation (%s)"

    def __init__(self, filename, node, indic):
        Message.__init__(self, filename, node)
        self.message_args = (indic,)