"""
Provide the class Message and its subclasses.
"""

from pyflakes.messages import Message


class DummyMessage1(Message):
    message = "dummy message1 (%s)"

    def __init__(self, filename, node, indic):
        Message.__init__(self, filename, node)
        self.message_args = (indic,)
        
class DummyMessage2(Message):
    message = "dummy message2 (%s)"

    def __init__(self, filename, node, indic):
        Message.__init__(self, filename, node)
        self.message_args = (indic,)