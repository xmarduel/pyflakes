
import os
import unittest
import xmlrunner

from pyflakes import messages as m
from pyflakes.test.harness import TestCase


class Test(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    #@skip("demonstrating skipping")
    def test_unusedCompare(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    x == y
''', m.NoEffectStatement)

    def test_unusedCompare2(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    z = 3
    x == (y == z)
''', m.NoEffectStatement, m.NoEffectStatement)

    def test_unusedCompare3(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    z = 3
    x == (not (y == z))
''', m.NoEffectStatement, m.NoEffectStatement)
          
    def test_unusedCompare4(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    z = 3
    not x == (y == z)
''', m.NoEffectStatement, m.NoEffectStatement)
        
    def test_usedCompare(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    if (x == y): pass
''')

    def test_usedCompare2(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    z = 3
    if x == (y == z): pass
''')
        
    def test_usedCompare3(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    z = 3
    x = (y == z)
    y = x
''')
        
    def test_usedCompare4(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    z = 3
    x = not (y == z)
    y = x
''')

    def test_usedCompare5(self):
        self.flakes('''
def toto():
    x = 1
    y = 2
    z = 3
    x = (y == z) and ( y == z )
    y = x
''')       
        
    def test_usedCompare_in_TrueIfCondElse_AssignRes(self):
        self.flakes('''
def toto():
    y = 2
    z = y
    x = True if (y == z) else False
    y = x
''')
        
    def test_usedCompare_in_TrueIfCondElse_NoAssignRes(self):
        self.flakes('''
def toto():
    y = 2
    z = y
    True if (y == z) else False
    y = z
''', m.NoEffectStatement)       


if __name__ == '__main__':
    if os.environ.get('PMF_XMLRUNNER_UNITTESTS', None) == "YES":
        unittest.main(testRunner=xmlrunner.XMLTestRunner(path='test-results', indic="test_comparestmts"))
    else:
        unittest.main()
