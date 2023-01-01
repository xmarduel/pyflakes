
from pyflakes.custom_checkers.dummy_checker import messages


class Checker(object):
    '''
    '''
    class DummyNode:
        # for PyFlakes Messages Compatibility
        def __init__(self, lineno):
            self.lineno = lineno
            self.col_offset = 0
            
    def __init__(self, filename):
        '''
        '''
        self.messages = [] # init
        
        self.checkdummys(filename) # fill report of DummyMessage[1-2] messages

    def checkdummys(self, filename):
        '''
        '''
        return
        # test
        #self.messages.append(messages.DummyMessage1(filename, self.DummyNode(1), "dummy"))


