
"""
Tests for L{pyflakes.scripts.pyflakes}.
"""

import os
import sys

import unittest
import xmlrunner

from pyflakes import messages as m
from pyflakes.test.harness import TestCase
from pyflakes.test.harness import skip, skipIf


class Test(TestCase):
    """
    """
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_global_declared_in_module_and_assigned_in_module(self):
        """
        use global var declared and assigned in module
        """
        self.flakes('''
        global g1 # global var declared
        g1 = 1    # ... and assigned
        class tutu:
            def __init__(self):
                self.b = g1
        ''')

    def test_global_declared_in_module_and_assigned_in_class(self):
        """
        use global var declared in module and assigned in class
        """
        self.flakes('''
        global g2 # global var declared
        #
        class tutu:
            def __init__(self):
                global g2 # declared in module
                g2 = 0    # ... and assigned here - is used as global assigned in lower scope...
                self.a = 0
        ''')
        
    def test_global_declared_in_class_and_assigned_in_class_used_in_other_method(self):
        """
        use global var declared in class and assigned in class, used in an other method
        """
        self.flakes('''
        class tutu:
            def __init__(self):
                global g3 # declared in class
                g3 = 2    # ... and assigned in class
                self.x = 0
            def action(self):
                a = g3
                self.x = a
        ''')
        
    @skipIf(1, 'pyflakes bug')
    def test_global_declared_too_late(self):
        """
        use global variable declared later-on
        """
        # You should declare the globals at the top : name is unknown...
        self.flakes('''
        class toto1:
            def __init__(self):
                self.b = 0
                self.a = g6   # g6 declared and assigned below 
        class toto2:
            def __init__(self):
                global g6     # declared in class
                g6 = 1        # and assigned here
                self.b = 1
        ''', m.UndefinedName)
              
    def test_globalInGlobalScope(self):
        """
        A global statement in the global scope is ignored.
        """
        self.flakes('''
        global x
        def foo():
            print(x)
        ''', m.UndefinedName)
        
    def test_globalInGlobalScope2(self):
        """
        A global statement in the global scope is not ignored if defined.
        """
        self.flakes('''
        global x
        x = 1
        def foo():
            print(x)
        ''')
        
    def test_globalInGlobalScope3(self):
        """
        A global statement in the global scope is not ignored if defined.
        """
        self.flakes('''
        global x
        x = 1
        class foo():
            def __init__(self):
                self.x = 0
                y = x
                self.x = y
        ''')
        
    def test_globalInClassScope(self):
        """
        A global statement in the class scope.
        """
        self.flakes('''
        class foo():
            global b
            b = None
            def __init__(self):
                global b
                b = 0
                self.x = -1
            def meth(self):
                self.x = b
        ''')
        
    @skipIf(1, 'pyflakes bug')
    def test_globalInClassInitFuncScope(self):
        """
        A global statement in the class scope.
        """
        self.flakes('''
        class foo():
            def __init__(self):
                global b
                b = 0
                self.x = -1
            def meth(self):
                self.x = b
        ''')                    

if __name__ == '__main__':
    if os.environ.get('PMF_XMLRUNNER_UNITTESTS', None) == "YES":
        unittest.main(testRunner=xmlrunner.XMLTestRunner(path='test-results', indic="test_global"))
    else:
        unittest.main()