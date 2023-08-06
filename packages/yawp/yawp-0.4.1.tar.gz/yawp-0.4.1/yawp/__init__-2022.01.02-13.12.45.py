#!/usr/bin/python3

'''Yet Another Word Processor, an automatic word processor for text and Python files

CONTENT

     1. Installation
     2. Help
     3. Introduction
     4. Logic
     5. Pretty Pictures
     6. Python Files
     7. An Example
     8. Messages
     9. History
    10. Author
    11. Arguments

1. INSTALLATION

Type from terminal:

    $ pip3 install yawp

2. HELP

Type from terminal:

    $ yawp -h

3. INTRODUCTION

The  name  "yawp"  means  Yet Another Word Processor, and yawp is a simple automatic word
processor for text files and Python files, with the following features:

    • yawp makes a timestamped backup of file to be processed, allowing "undo" operation
    • yawp works "in place", reading formatting and rewriting the file to be processed
    • yawp operation is driven only by the content of the file and by a few parameters
    • yawp justifies "text" at left and right in:
        • unindented paragraphs
        • dot-marked indented paragraphs
    • yawp  accepts  unjustified "pictures" (as schemas, tables and code examples) freely
      intermixed with text
    • yawp's "pretty pictures" feature allows you to sketch draft pictures with lines and
      arrowheads by '#' and '@' characters, which are automatically replaced by proper graphic characters
    • yawp uses an ad hoc policy with Python files, formatting the docstrings but not the
      Python code
    • yawp  is  "stable", if  after a run of yawp on a file you run yawp a second time on
      the same file with the same arguments then the file content doesn't change
      
As  an  example,  this  documentation  you're reading has been formatted by yawp. Another
example is in chapter 7.

4. LOGIC

Let's distinguish in four categories the file lines:

    • a line is an "empty line" if it contains no characters (note that in any input line
      all  trailing  blanks  are  stripped  away,  hence every input line containing only
      blanks becomes an empty line)
    • otherwise a line is a "dot line" if the first nonblank character is a dot character
      '.' or '•' followed by a blank (on output such a '.' is always replaced by a '•')
    • otherwise a line is an "indented line" if it starts with a blank character
    • otherwise a line is an "unindented line"

More exactly, the "dot characters" are:

    • '.' is Unicode "decimal point", Python chr(46) or '\\x2e'
    • '•' is Unicode "black small circle", Python chr(8226) or '\\u2022'

The yasf algorithm, driven by the input lines, oscillates between two states:

    • "picture state", where input lines are directly written out as they are
    • "text state", where input lines are accumulated into a paragraph buffer for further
      justification and writing at paragraph end

The picture state is the initial state. In this state, if the input is:

    • an empty line or an indented line: the line is written out as is
    • an  unindented  line:  text  state  is  entered, an unindented paragraph begins,
      the line is shrinked (initial and multiple  blanks  are  eliminated)  and assigned to the paragraph buffer, paragraph
      left indentation is set to zero
    • a  dot  line:  text  state  is  entered, an indented paragraph begins, the  line is shrinked and assigned to the
      paragraph  buffer, paragraph left indentation is set to the position of initial dot
      character plus two
    • end of input file: processing is terminated

When we are in text state, if the input line is:

    • an  empty  line:  the  paragraph  buffer  is  flushed  (justified,  written out and
      emptied), state goes back to picture state, the empty line is written out
    • an  indented or unindented line: the line is shrinked and appended to the paragraph
      buffer
    • a  dot  line:  paragraph buffer is flushed, a new paragraph is started, the line is
      shrinked and assigned to the paragraph buffer, paragraph left indentation is set to
      the position of initial dot plus two
    • end of input file: paragraph buffer is flushed, processing is ended

For sake of clarity, the following diagram illustrates states and transitions.

        empty line,                                                 unindented line,
        indented line:                                              indented line:
        write                                                       append
        ┌──────────┐                                                ┌──────────┐
        │          │                                                │          │
        │          │                                                │          │
        │    ┌─────┴─────┐ unindented line, dot line: assign  ┌─────┴─────┐    │
        └───▷│           ├───────────────────────────────────▷│           │◁───┘
             │  picture  │      empty line: flush, write      │  text     │
   ─────────▷│           │◁───────────────────────────────────┤           │
             │  state    │                                    │  state    │
             │           │                             ┌──────┤           │◁───┐
             └─────┬─────┘                             │      └─────┬─────┘    │
                   │                                   │            │          │
                   │                                   │            │          │
        ◁──────────┘                        ◁──────────┘            └──────────┘
        end of file:                        end of file:            dot line:
        stop                                flush, stop             flush, assign

Actions associated to transitions are:

    • "write": the input line is immediately written out as is
    • "assign":  the  input  line  is  shrinked  (initial,  multiple and final blanks are
      removed) and assigned to the paragraph buffer
    • "append": the input line is shrinked and appended to the paragraph buffer
    • "flush": the paragraph buffer is flushed (justified, written out and emptied)
    • "stop": execution is finished

5. PRETTY PICTURES

In a picture you can sketch draft pictures with lines and arrows by two special characters:

    . use '#' to draw horizontal and vertical lines
    . use '@' to mark an arrowhead

Such characters are (possibly) replaced by yawp with graphic characters, depending on the other characters around.

This feature is active in image mode only, so it does not work in paragraphs.

See examples in chapter 7.

6. PYTHON FILES

Python  files  deserve  a  special  treatment.  If  the textfile filename ends with '.py'
extension, then we suppose the file is a Python source, hence we are interested to format
docstrings and not Python code. So the formatting function is alternatively turned on and
off by switch lines. A "switch line" is a line containing a "\'\'\'" string.

Note that yawp never formats switch lines, formatting takes place from the line after the
"on" switch line until the line before the next "off" switch line.

So your Python file must follow some simple rules:

    • docstrings to be formatted must start and ended by "\'\'\'" and not '"""'
    • long strings not to be formatted must start and end with '"""' and not "\'\'\'"
    • a "\'\'\'" inside a string must be coded as "\\'\\'\\'"

An  error  in switch lines could format and destroy your Python code. A preliminary check
prints an error message and stops execution before file formatting if the total number of
switch  lines  is  odd. This should intercept 90% of errors, anyway after yawp processing
check the result and if needed go back to previous version by the -u/--undo yawp option.

7. AN EXAMPLE

An usage example with a Python file follows.

...

8. MESSAGES

All  messages  are  written  on  stderr,  in  order to avoid interference with -p/--print
option, which writes on stdout.

There are three types of messages:
    • "information messages" are written when -v/--verbose option is on:
        • Backup of file '...' into file '...'
        • Processing of file '...'
        • Restore of file '...' from file '...'
        • Content of file '...'
    • "warning  messages"  are  written  when  something  goes  wrong  but  execution can
      continue:
        • WARNING: Line ..., impossible to left-justify: '...' .
        • WARNING: Line ..., impossible to right-justify: '...'
        • WARNING: Line ... is too long: '...'
    • "error messages" are written when execution must be interrupted:
        • ERROR: File '...' not found, PROGRAM HALTED
        • ERROR: Backup file for file '...' not found', PROGRAM HALTED
        • ERROR: Python file '...', odd number of switch lines, PROGRAM HALTED

9. HISTORY

    • version 0.4.1
        • first version published on pypi.org

10. AUTHOR

Written by Carlo Alessandro Verre, carlo.alessandro.verre@gmail.com.

11. ARGUMENTS
'''

__version__ = '0.4.1'

__all__ = []

#----- imports -----

from fnmatch import fnmatchcase
from glob import glob
from os.path import join as joinpath, split as splitpath, abspath, expanduser, splitext, exists, isfile, isdir
from sys import exit, stderr
from time import localtime

#----- message functions -----

def inform(message):
    'print an information message and continue'
    print(message, file=stderr)

def warning(message):
    'print a warning message and continue'
    print(f'WARNING: {message}', file=stderr)

def error(message):
    'print an error message and exit'
    exit(f'ERROR: {message}, PROGRAM HALTED')

#----- path & file functions -----

def longpath(path='.'):
    return abspath(expanduser(path))

def shortpath(path='.'):
    path, home = longpath(path), longpath('~')
    return '~' + path[len(home):] if path.startswith(home) else path

def listfiles(pattern):
    "return a list of absolute paths to {pattern}-matching files, '**' in path is allowed"
    return [file for file in glob(longpath(pattern), recursive=True) if isfile(file)]

def listdirs(pattern):
    "return a list of absolute paths to {pattern}-matching dirs, '**' in path is allowed"
    return [dir for dir in glob(longpath(pattern), recursive=True) if isdir(dir)]

def newbackfile(file):
    'create a timestamped filename for backup of {file}'
    path, ext = splitext(longpath(file))
    return f'{path}-%04d.%02d.%02d-%02d.%02d.%02d{ext}' % localtime()[:6]

def oldbackfile(file):
    "return filename of the more recent timestamped backup of file {file}, or '' if not found"
    path, ext = splitext(longpath(file))
    return max(listfiles(f'{path}-????.??.??-??.??.??{ext}') or [''])

#----- string functions -----

def hold(string, charpattern, default=''):
    'hold {charpattern}-matching chars in {string} and replace not matching chars by {default}'
    return ''.join(char if fnmatchcase(char, charpattern) else default for char in string)

def chars(charpattern):
    'return a sorted string of all {charpattern}-matching characters'
    kernel = charpattern[1:-1]
    return ''.join(chr(j) for j in range(ord(min(kernel)), ord(max(kernel)) + 1)
                   if fnmatchcase(chr(j), charpattern))

def split(string, separator=None):
    'return [] if not string else string.split(separator)'
    return [] if not string else string.split(separator)

def replace(string, *oldsnews):
    'replace(string, a, b, c, d, ...) == string.replace(a, b).replace(c, d)...'
    for j in range(0, len(oldsnews), 2):
        string = string.replace(oldsnews[j], oldsnews[j+1])
    return string

def shrink(string, joinby=' ', splitby=None):
    'eliminate from {string} leading, multiple and trailing blanks'
    return joinby.join(string.split(splitby))

def findchar(string, pattern):
    'return index of first {pattern}-matching char found in {string}, -1 if not found'
    for j, char in enumerate(string):
        if fnmatchcase(char, pattern):
            return j
    else:
        return -1

def rfindchar(string, pattern):
    'return index of last {pattern}-matching char found in {string}, -1 if not found'
    for j, char in retroenum(string):
        if fnmatchcase(char, pattern):
            return j
    else:
        return -1

def chrs(jj):
    "return ''.join(chr(j) for j in jj)"
    return ''.join(chr(j) for j in jj)

def ords(string):
    'return [ord(char) for char in string]'
    return [ord(char) for char in string]

#----- sequence functions -----

def retroenum(sequence):
    'like enumerate(sequence), but backwards from last to first item'
    for j in range(len(sequence) - 1, -1, -1):
        yield j, sequence[j]

def find(sequence, item):
    'return index of first {item} found in {sequence}, -1 if not found'
    for j, itemj in enumerate(sequence):
        if itemj == item:
            return j
    else:
        return -1

def rfind(sequence, item):
    'return index of last {item} found in {sequence}, -1 if not found'
    for j, itemj in retroenum(sequence):
        if itemj == item:
            return j
    else:
        return -1

#----- end -----
