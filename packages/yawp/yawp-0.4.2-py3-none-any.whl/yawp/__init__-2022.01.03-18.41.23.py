#!/usr/bin/python3

'''Yet Another Word Processor, an automatic word processor for text and Python files

    I sound my barbaric yawp over the roofs of the world
                                          (Walt Whitman)

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

The  name  "yawp"  here  means Yet Another Word Processor, and yawp is a simple automatic
word processor for text files and Python files, with the following features:

    • yawp makes a timestamped backup of file to be processed, allowing "undo" operation
    • yawp works "in place", reading formatting and rewriting the file to be processed
    • yawp operation is driven only by the content of the file and by a few parameters
    • yawp justifies "text" at left and right in:
        • unindented paragraphs
        • dot-marked indented paragraphs
    • yawp  accepts  unjustified "pictures" (as schemas, tables and code examples) freely
      intermixed with text
    • yawp's "pretty graphics" feature allows you to sketch draft pictures with lines and
      arrowheads  by  '#'  and '@' characters, which are automatically replaced by proper
      graphic characters
    • yawp's  "pretty  chapters"  feature ensures automatic multi-level chapter numbering
      and generation of table of contents
    • yawp  adopts  an ad hoc policy with Python files, formatting the docstrings but not
      the Python code
    • yawp  is  "stable",  if after a run of yawp on a file you run yawp a second time on
      the same file with the same arguments then the file content doesn't change

As  an  example,  this  documentation  you're  reading  has been formatted by yawp. Other
examples are scattered below.

4. LOGIC

"Pretty text" is an optional feature, it's activated by the -t/--pretty-text argument. If is not set,
then input lines are not justified, otherwise text justification takes place as follows.

Let's distinguish in four categories the file lines:

    • a line is an "empty line" if it contains no characters (note that in all input lines
      all  trailing  blanks  are  stripped  away,  hence every input line containing only
      blanks becomes an empty line)
    • otherwise a line is a "dot line" if the first nonblank character is a dot character
      '.' or '•' followed by a blank (on output such a '.' is always replaced by a '•')
    • otherwise a line is an "indented line" if it starts with a blank character
    • otherwise a line is an "unindented line"

More exactly, the "dot characters" are:

    • '.' is Unicode "decimal point", Python chr(46) or '\\x2e'
    • '•' is Unicode "black small circle", Python chr(8226) or '\\u2022'

The yawp algorithm, driven by the input lines, oscillates between two states:

    • "picture state", where input lines are directly written out as they are
    • "text state", where input lines are accumulated into a paragraph buffer for further
      justification and writing at paragraph end

The picture state is the initial state. In this state, if the input is:

    • an empty line or an indented line: the line is written out as is
    • an unindented line: text state is entered, an unindented paragraph begins, the line
      is  shrinked  (initial  and  multiple  blanks  are  eliminated) and assigned to the
      paragraph buffer, paragraph left indentation is set to zero
    • a  dot  line:  text  state  is  entered,  an indented paragraph begins, the line is
      shrinked and assigned to the paragraph buffer, paragraph left indentation is set to
      the position of initial dot character plus two
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

5. PRETTY GRAPHICS

"Pretty graphics" is an optional feature, it's activated by the -g/--pretty-graphics argument.

In  a  picture  you  can  sketch  draft  pictures  with  lines  and arrows by two special
characters:

    • use '#' to draw horizontal and vertical lines
    • use '@' to mark an arrowhead

Each  such  character  is  (possibly)  replaced  by yawp with a proper graphic character,
depending  on  the  other  four  characters  around (over, under, at left, and at right).
Isolated characters are not replaced.

This feature is active in image mode only, so it does not work in paragraphs.

An example:

    $ cat graphics.txt
           #############      
           # x - y     #      
         x #   #############               ######
           #   # x & y #   #               #N#N2#
           #############   # y             ######
               #     y - x #               #0# 0#
               #############               #1# 1#
                                           #2# 4#
                #####     #####            #3# 9#
          #####@# A #####@# B #@#####      #4#16#
                #####     #####     #      #5#25#
                  @         #       #      #6#36#
                  #         #       #      #7#49#
                  #         @       #      #8#64#
                #####     #####     #      #9#81#
          @###### D #@##### C #@#####      ######
                #####     #####
    $ yawp -v -w55 -g -p graphics.txt
    ... Backup of file '~/graphics.txt' into file '~/graphics-2022.01.03-17.14.27.txt'
    ... Rewriting file '~/graphics.txt'
    ... Printing file '~/graphics.txt'
           ┌───────────┐
           │ x - y     │
         x │   ┌───────┼───┐               ┌─┬──┐
           │   │ x & y │   │               │N│N2│
           └───┼───────┘   │ y             ├─┼──┤
               │     y - x │               │0│ 0│
               └───────────┘               │1│ 1│
                                           │2│ 4│
                ┌───┐     ┌───┐            │3│ 9│
          ─────▷│ A ├────▷│ B │◁────┐      │4│16│
                └───┘     └─┬─┘     │      │5│25│
                  △         │       │      │6│36│
                  │         │       │      │7│49│
                  │         ▽       │      │8│64│
                ┌─┴─┐     ┌───┐     │      │9│81│
          ◁─────┤ D │◁────┤ C │◁────┘      └─┴──┘
                └───┘     └───┘
    $ 

5. PRETTY CHAPTERS

"Pretty chapters" is an optional feature, it's activated by the -c/--pretty-chapters argument.
If set, it ensures automatic multi-level chapter numbering
      and generation of table of contents.

If pretty chapters is active, the file must contain:

    . a "content line", containing the title of the table of content
    . one or more "chapter lines", containing a multi-level numbering and a chapter title

A line is a content line if:

    . is the first line or is preceded by an empty line
    . is followed by an empty line
    . starts with an uppercase letter
    . contains uppercase letters and blanks only

A content line must precede all chapter lines. Examples:

    . 'CONTENT'
    . 'TABLE OF CONTENT'
    . 'INDEX OF CHAPTERS'

A line is a chapter line if:

    . is preceded by an empty line
    . is the last line or is followed by an empty line
    . contains:
        . one or more unsigned decimal integer constants, each followed by a '.' dot
        . a blank
        . a chapter title, containig any character but underscore letters

The "level" of chapter line is the count of number-dot couples in its prefix, examples:

    . '12345. A LEVEL-1 CHAPTER LINE'
    . '1.345. A LEVEL-2 CHAPTER LINE'
    . '0.0.0. A LEVEL-3 CHAPTER LINE'

Chapter lines must follow two sequence rules:

    . first chapter line must be a level-1 chapter line
    . each other chapter line can have a level between 1 and the level of the previous chapter line plus 1

Numbers in input don't matter, they are replaced by the right ones, only the level matters.

Lines between the content line and the first chapter line are suppose to contain the old table of content, hence they are deleted and replaced by the new automatically
generated table of content.

This feature is active in text mode only, so it does not work in pictures. For what has been said we can observe that each content line or chapter line must be a one-line unindented paragraph.

An example:

    $ cat chapters.txt
        TITLE OF DOCUMENT

    TABLE OF CONTENTS

        (old table of content
         will be replaced
         by the new one)

    0. AAA AAA

    ...

    32.33. BBB BBB

    0.0. CCC CCC

    0. DDD DDD

    0.0. EEE EEE

    0.0.0. FFF FFF

    0.0. GGG GGG
    $ yawp -v -w55 -c -p chapters.txt
    ... Backup of file '~/chapters.txt' into file '~/chapters-2022.01.03-17.01.14.txt'
    ... Rewriting file '~/chapters.txt'
    ... Printing file '~/chapters.txt'
        TITLE OF DOCUMENT

    TABLE OF CONTENTS

        1. Aaa Aaa
        1.1. Bbb Bbb
        1.2. Ccc Ccc
        2. Ddd Ddd
        2.1. Eee Eee
        2.1.1. Fff Fff
        2.2. Ggg Ggg

    1. AAA AAA

    ...

    1.1. BBB BBB

    1.2. CCC CCC

    2. DDD DDD

    2.1. EEE EEE

    2.1.1. FFF FFF

    2.2. GGG GGG
    $ 

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

An example:

    $ cat pycode.py
    #!/usr/bin/python3

    \'\'\' Text in "on" switch line is not formatted.
    This is a one-line unindented paragraph.

    This is a multi-line unindented paragraph.
    This is a multi-line unindented paragraph.
    This is a multi-line unindented paragraph.

        This is a picture, it remains as is.
                This is a picture, it remains as is.
            This is a picture, it remains as is.

        . This is a multi-line indented paragraph.
    This is a multi-line indented paragraph.
        This is a multi-line indented paragraph.
            . This is another multi-line indented paragraph.
    This is another multi-line indented paragraph.
        This is another multi-line indented paragraph.
    \'\'\' # Text in "off" switch line is not formatted.

    def double(x): # Python code is not formatted.
        \'\'\'
    This is another multi-line unindented paragraph.
    This is another multi-line unindented paragraph.
    This is another multi-line unindented paragraph.
    \'\'\'
        return x + x # Python code is not formatted.
    $ yawp -v -w55 -p pycode.py
    ... Backup of file '~/pycode.py' into file '~/pycode-2022.01.03-16.49.27.py'
    ... Rewriting file '~/pycode.py'
    ... Printing file '~/pycode.py'
    #!/usr/bin/python3

    \'\'\' Text in "on" switch line is not formatted.
    This is a one-line unindented paragraph.

    This  is  a  multi-line unindented paragraph. This is a
    multi-line  unindented  paragraph. This is a multi-line
    unindented paragraph.

        This is a picture, it remains as is.
                This is a picture, it remains as is.
            This is a picture, it remains as is.

        • This  is a multi-line indented paragraph. This is
          a   multi-line  indented  paragraph.  This  is  a
          multi-line indented paragraph.
            • This    is    another   multi-line   indented
              paragraph.   This   is   another   multi-line
              indented    paragraph.    This   is   another
              multi-line indented paragraph.
    \'\'\' # Text in "off" switch line is not formatted.

    def double(x): # Python code is not formatted.
        \'\'\'
    This  is  another multi-line unindented paragraph. This
    is  another  multi-line  unindented  paragraph. This is
    another multi-line unindented paragraph.
    \'\'\'
        return x + x # Python code is not formatted.
    $ 

8. MESSAGES

All  messages  are  written  on  stderr,  in  order to avoid interference with -p/--print
option, which writes on stdout.

There are two types of messages:
    • "information messages" say what's going on if -v/--verbose argument is set:
        • ... Backup of file '...' into file '...'
        • ... Restore of file '...' from file '...'
        • ... Processing of file '...'
        • ... Printing of file '...'
    • "error  messages"  are  written  when  execution  must be interrupted, in this case
      backup is not performed and file is not rewritten:
        • !!! File '...' not found, program halted
        • !!! Backup file for file '...' not found', program halted
        • !!! Line ..., impossible to left-justify: '...', program halted
        • !!! Line ..., impossible to right-justify: '...', program halted
        • !!! Line ... is too long: '...', program halted
        • !!! Python file, odd number of switch lines, program halted

9. HISTORY

    • version 0.4.1
        • first version published on pypi.org

10. AUTHOR

Written by Carlo Alessandro Verre, carlo.alessandro.verre@gmail.com.

11. ARGUMENTS

If -u is set then -w -l -g and -c are allowed but have no effect.

Note that -g and -c are indipendent, each can be set or not.
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
    print(f'... {message}', file=stderr)

def warning(message):
    'print a warning message and continue'
    print(f'??? {message}', file=stderr)

def error(message):
    'print an error message and exit'
    exit(f'!!! {message}, program halted')

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
