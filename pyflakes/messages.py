"""
Provide the class Message and its subclasses.
"""


class Message(object):
    message = ''
    message_args = ()

    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4
    
    ignoreHint = '' # for false message : annotate code
    reporting = True # for unittests : disable temporary some messages
    severity = INFO
    
    def __init__(self, filename, loc):
        self.filename = filename
        self.lineno = loc.lineno
        self.col = getattr(loc, 'col_offset', 0)

    def __str__(self):
        return '%s:%s: %s' % (self.filename, self.lineno,
                              self.message % self.message_args)
    
    @classmethod
    def lineWithIgnoreHint(cls, line, *args, **kwargs):
        if cls.ignoreHint and cls.ignoreHint in line:
            return True
        else:
            return False
    
class UnusedImport(Message):
    message = "imported module %r not used"

    ignoreHint = "pyflakes:ignore-msg#imported module not used"

    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class RedefinedWhileUnused(Message):
    message = 'redefinition of unused %r from line %r'

    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class RedefinedInListComp(Message):
    message = 'list comprehension redefines %r from line %r'

    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class ImportShadowedByLoopVar(Message):
    message = 'import %r from line %r shadowed by loop variable'

    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class ImportStarNotPermitted(Message):
    message = "'from %s import *' only allowed at module level"

    def __init__(self, filename, loc, modname):
        Message.__init__(self, filename, loc)
        self.message_args = (modname,)


class ImportStarUsed(Message):
    message = "'from %s import *' used; unable to detect undefined names"

    def __init__(self, filename, loc, modname):
        Message.__init__(self, filename, loc)
        self.message_args = (modname,)


class ImportStarUsage(Message):
    message = "%r may be undefined, or defined from star imports: %s"

    def __init__(self, filename, loc, name, from_list):
        Message.__init__(self, filename, loc)
        self.message_args = (name, from_list)


class UndefinedName(Message):
    message = '(E) undefined name %r'

    ignoreHint = "pyflakes:ignore-msg#undefined name"

    severity = Message.ERROR
    
    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class DoctestSyntaxError(Message):
    message = 'syntax error in doctest'

    def __init__(self, filename, loc, position=None):
        Message.__init__(self, filename, loc)
        if position:
            (self.lineno, self.col) = position
        self.message_args = ()


class UndefinedExport(Message):
    message = '(E) undefined name %r in __all__'

    severity = Message.ERROR
    
    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class UndefinedLocal(Message):
    message = '(E) local variable %r {0} referenced before assignment'

    default = 'defined in enclosing scope on line %r'
    builtin = 'defined as a builtin'
    
    severity = Message.ERROR
    
    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        if orig_loc is None:
            self.message = self.message.format(self.builtin)
            self.message_args = name
        else:
            self.message = self.message.format(self.default)
            self.message_args = (name, orig_loc.lineno)


class DuplicateArgument(Message):
    message = '(E) duplicate argument %r in function definition'

    severity = Message.ERROR
    
    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class MultiValueRepeatedKeyLiteral(Message):
    message = 'dictionary key %r repeated with different values'

    def __init__(self, filename, loc, key):
        Message.__init__(self, filename, loc)
        self.message_args = (key,)


class MultiValueRepeatedKeyVariable(Message):
    message = 'dictionary key variable %s repeated with different values'

    def __init__(self, filename, loc, key):
        Message.__init__(self, filename, loc)
        self.message_args = (key,)


class LateFutureImport(Message):
    message = 'from __future__ imports must occur at the beginning of the file'

    def __init__(self, filename, loc, names):
        Message.__init__(self, filename, loc)
        self.message_args = ()


class FutureFeatureNotDefined(Message):
    """An undefined __future__ feature name was imported."""
    message = 'future feature %s is not defined'

    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class UnusedVariable(Message):
    """
    Indicates that a variable has been explicitly assigned to but not actually
    used.
    """
    message = 'local variable %r is assigned to but never used'

    ignoreHint = "pyflakes:ignore-msg#unused variable"
    
    severity = Message.WARNING
    
    def __init__(self, filename, loc, names):
        Message.__init__(self, filename, loc)
        self.message_args = (names,)


class ReturnWithArgsInsideGenerator(Message):
    """
    Indicates a return statement with arguments inside a generator.
    """
    message = '\'return\' with argument inside generator'


class ReturnOutsideFunction(Message):
    """
    Indicates a return statement outside of a function/method.
    """
    message = '\'return\' outside function'


class YieldOutsideFunction(Message):
    """
    Indicates a yield or yield from statement outside of a function/method.
    """
    message = '\'yield\' outside function'


# For whatever reason, Python gives different error messages for these two. We
# match the Python error message exactly.


class ContinueOutsideLoop(Message):
    """
    Indicates a continue statement outside of a while or for loop.
    """
    message = '\'continue\' not properly in loop'


class BreakOutsideLoop(Message):
    """
    Indicates a break statement outside of a while or for loop.
    """
    message = '\'break\' outside loop'


class ContinueInFinally(Message):
    """
    Indicates a continue statement in a finally block in a while or for loop.
    """
    message = '\'continue\' not supported inside \'finally\' clause'


class DefaultExceptNotLast(Message):
    """
    Indicates an except: block as not the last exception handler.
    """
    message = 'default \'except:\' must be last'


class TwoStarredExpressions(Message):
    """
    Two or more starred expressions in an assignment (a, *b, *c = d).
    """
    message = 'two starred expressions in assignment'


class TooManyExpressionsInStarredAssignment(Message):
    """
    Too many expressions in an assignment with star-unpacking
    """
    message = 'too many expressions in star-unpacking assignment'


class AssertTuple(Message):
    """
    Assertion test is a tuple, which are always True.
    """
    message = 'assertion is always true, perhaps remove parentheses?'


class ForwardAnnotationSyntaxError(Message):
    message = 'syntax error in forward annotation %r'

    def __init__(self, filename, loc, annotation):
        Message.__init__(self, filename, loc)
        self.message_args = (annotation,)


class CommentAnnotationSyntaxError(Message):
    message = 'syntax error in type comment %r'

    def __init__(self, filename, loc, annotation):
        Message.__init__(self, filename, loc)
        self.message_args = (annotation,)


class RaiseNotImplemented(Message):
    message = "'raise NotImplemented' should be 'raise NotImplementedError'"


class InvalidPrintSyntax(Message):
    message = 'use of >> is invalid with print function'
    
        
# 1.6.0.1 messages


class UnusedFunctionArgument(Message):
    message = "function parameter %r not used"
    
    def __init__(self, filename, node, names):
        Message.__init__(self, filename, node)
        self.message_args = (names,)
