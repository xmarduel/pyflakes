

import pycodestyle

from pyflakes.custom_checkers.indentation_checker import messages


class Checker(object):
    '''
    '''            
    def __init__(self, filename):
        '''
        '''
        self.messages = [] # init
        
        if messages.BadIndentation.reporting == False:
            return
        
        self.checkindent(filename) # fill report of BadIndentation messages

    def checkindent(self, filename):
        '''
        '''
        class DummyNode:
            # for PyFlakes Messages Compatibility
            def __init__(self, lineno):
                self.lineno = lineno
            
        class StringReport(pycodestyle.StandardReport):
            '''
            '''
            def get_file_results(self):
                pass # no default print
            def print_msg(self, msg):
                line_number, offset, code, text, doc = msg
                print(self._fmt % {
                    'path': self.filename,
                    'row': self.line_offset + line_number, 
                    'col': offset + 1,
                    'code': code, 
                    'text': text,
                })
 
        pep8opts = pycodestyle.StyleGuide(
            select=['W191', 'E901'],  # only those related to tab/indentation
            max_line_length=100,
            format='pylint'
        ).options

        report = StringReport(pep8opts)
        
        checker = pycodestyle.Checker(filename, options=pep8opts, report=report)
        checker.check_all()
        for msg in checker.report._deferred_print:
            #checker.report.print_msg(msg)
            lineno, offset, code, text, doc = msg
            self.messages.append(
                messages.BadIndentation(filename, 
                                        DummyNode(lineno+report.line_offset),
                                        text))
