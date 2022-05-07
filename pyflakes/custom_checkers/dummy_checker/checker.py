#
'''
COPYRIGHT (C)

 PROJECT:   PyFlakes
 AUTHOR:    xam
 MODULE:    $RCSfile: indentchecker.py,v $
 VERSION:   $Revision: 1.4 $
 DATE:      $Date: 2011/11/19 16:24:54 $
 COMMITTER  $Author: xavier $

 MODULE DESCRIPTION:
      
'''

from pyflakes.custom_checkers.dummy_checker import messages


class Checker(object):
    '''
    '''
    class DummyNode:
        # for PyFlakes Messages Compatibility
        def __init__(self, lineno):
            self.lineno = lineno
            
    def __init__(self, filename):
        '''
        '''
        self.messages = [] # init
        
        if messages.DummyMessage1.reporting == False and messages.DummyMessage1.reporting == False :
            return
        
        self.checkdummys(filename) # fill report of DummyMessage[1-2] messages

    def checkdummys(self, filename):
        '''
        '''
        return
        # test
        #self.messages.append(messages.DummyMessage1(filename, self.DummyNode(1), "dummy"))


