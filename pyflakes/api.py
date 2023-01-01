"""
API for the command-line I{pyflakes} tool.
"""
import ast
import os
import platform
import re
import sys

import traceback

from pyflakes import checker, __version__
from pyflakes import reporter as modReporter

__all__ = ['check', 'checkPath', 'checkRecursive', 'iterSourceCode', 'main']

PYTHON_SHEBANG_REGEX = re.compile(br'^#!.*\bpython(3(\.\d+)?|w)?[dmu]?\s')


def check(codeString, filename, reporter=None):
    """
    Check the Python source given by C{codeString} for flakes.

    @param codeString: The Python source to check.
    @type codeString: C{str}

    @param filename: The name of the file the source came from, used to report
        errors.
    @type filename: C{str}

    @param reporter: A L{Reporter} instance, where errors and warnings will be
        reported.

    @return: The number of warnings emitted.
    @rtype: C{int}
    """
    if reporter is None:
        reporter = modReporter._makeDefaultReporter()
    # First, compile into an AST and handle syntax errors.
    try:
        tree = ast.parse(codeString, filename=filename)
    except SyntaxError as e:
        reporter.syntaxError(filename, e.args[0], e.lineno, e.offset, e.text)
        return 1
    except Exception:
        reporter.unexpectedError(filename, 'problem decoding source')
        return 1
    # Okay, it's syntactically valid.  Now check it.
    messages = []
    try:
        # custom checkers first
        for custom_checker in getCustomCheckers():
            c_checker = custom_checker.Checker(filename)
            messages += c_checker.messages
        # standard checker then
        s_checker = checker.Checker(tree, filename)
        messages += s_checker.messages
    except Exception as msg:
        reporter.unexpectedError(filename, str(traceback.print_exc()))
        return 1

    messages.sort(key=lambda m: m.lineno)

    # keep pyflakes silent -> good in Makefiles
    if os.environ.get('PYFLAKES_SILENT', 'NO') != 'YES':
        for msg in messages:
            reporter.flake(msg)
        
    # return code : number of errors -> good in Makefiles
    return len([msg for msg in messages if msg.severity == msg.ERROR]) # only the real errors
    return len(messages)
    

def getCustomCheckers():
    """
    Returns a list of modules which are "checkers".
    A "checker" module is a python file containing a "Checker" class. It must
    be in a python folder module of the same name.
    Names are specified in the __all__ if the __init__.py file
    
    tree:
        pyflakes
          + custom_checkers
              + <my checker 1>
                  + __init__.py
                  + checker.py      # this module is returned in a list
                  + messages.py
              + <my checker 2>
                  + __init__.py
                  + checker.py      # this module is returned in a list
                  + messages.py
    
    @return: list of custom checker modules
    """
    checker_modules = []
    
    try:
        from pyflakes import custom_checkers
    except Exception:
        return []
    
    for custom_checker_str in custom_checkers.__all__ :
        try:
            custom_checker_folder = "pyflakes.custom_checkers." +  custom_checker_str
            mod = __import__(custom_checker_folder, fromlist=[custom_checker_str] )

            custom_checker_module = custom_checker_folder + ".checker"
            mod = __import__(custom_checker_module, fromlist=["checker"] )
            
            checker_modules.append(mod)

        except Exception as msg:
            print(str(msg))
        finally:
            pass

    return checker_modules


def checkPath(filename, reporter=None):
    """
    Check the given path, printing out any warnings detected.

    @param reporter: A L{Reporter} instance, where errors and warnings will be
        reported.

    @return: the number of warnings printed
    """
    if reporter is None:
        reporter = modReporter._makeDefaultReporter()
    try:
        with open(filename, 'rb') as f:
            codestr = f.read()
    except OSError as e:
        reporter.unexpectedError(filename, e.args[1])
        return 1
    return check(codestr, filename, reporter)


def isPythonFile(filename):
    """Return True if filename points to a Python file."""
    if filename.endswith('.py'):
        return True

    # Avoid obvious Emacs backup files
    if filename.endswith("~"):
        return False

    max_bytes = 128

    try:
        with open(filename, 'rb') as f:
            text = f.read(max_bytes)
            if not text:
                return False
    except OSError:
        return False

    return PYTHON_SHEBANG_REGEX.match(text)


def iterSourceCode(paths):
    """
    Iterate over all Python source files in C{paths}.

    @param paths: A list of paths.  Directories will be recursed into and
        any .py files found will be yielded.  Any non-directories will be
        yielded as-is.
    """
    for path in paths:
        if os.path.isdir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    if isPythonFile(full_path):
                        yield full_path
        else:
            yield path


def checkRecursive(paths, reporter):
    """
    Recursively check all source files in C{paths}.

    @param paths: A list of paths to Python source files and directories
        containing Python source files.
    @param reporter: A L{Reporter} where all of the warnings and errors
        will be reported to.
    @return: The number of warnings found.
    """
    warnings = 0
    for sourcePath in iterSourceCode(paths):
        warnings += checkPath(sourcePath, reporter)
    return warnings


def _exitOnSignal(sigName, message):
    """Handles a signal with sys.exit.

    Some of these signals (SIGPIPE, for example) don't exist or are invalid on
    Windows. So, ignore errors that might arise.
    """
    import signal

    try:
        sigNumber = getattr(signal, sigName)
    except AttributeError:
        # the signal constants defined in the signal module are defined by
        # whether the C library supports them or not. So, SIGPIPE might not
        # even be defined.
        return

    def handler(sig, f):
        sys.exit(message)

    try:
        signal.signal(sigNumber, handler)
    except ValueError:
        # It's also possible the signal is defined, but then it's invalid. In
        # this case, signal.signal raises ValueError.
        pass


def _get_version():
    """
    Retrieve and format package version along with python version & OS used
    """
    return ('%s Python %s on %s' %
            (__version__, platform.python_version(), platform.system()))


def main(prog=None, args=None):
    """Entry point for the script "pyflakes"."""
    import argparse

    # Handle "Keyboard Interrupt" and "Broken pipe" gracefully
    _exitOnSignal('SIGINT', '... stopped')
    _exitOnSignal('SIGPIPE', 1)

    parser = argparse.ArgumentParser(prog=prog,
                                     description='Check Python source files for errors')
    parser.add_argument('-V', '--version', action='version', version=_get_version())
    parser.add_argument('path', nargs='*',
                        help='Path(s) of Python file(s) to check. STDIN if not given.')
    args = parser.parse_args(args=args).path
    reporter = modReporter._makeDefaultReporter()
    if args:
        warnings = checkRecursive(args, reporter)
    else:
        warnings = check(sys.stdin.read(), '<stdin>', reporter)
    raise SystemExit(warnings > 0)
