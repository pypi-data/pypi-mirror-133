#!/usr/bin/python3

#----- imports -----

from .__init__ import __version__ as version, __doc__ as description
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from warnings import simplefilter
from sys import argv

from .__init__ import inform, warning, error
from .__init__ import longpath, shortpath, listfiles, listdirs, newbackfile, oldbackfile
from .__init__ import hold, chars, split, replace, shrink, findchar, rfindchar, chrs, ords
from .__init__ import retroenum, find, rfind
from os import remove, rename
from os.path import isfile

#----- global data -----

class Args: pass # container for arguments
class Glob: pass # container for other global data

#----- constants -----

CODE, TEXT, PICT = 'ctp' # values for out.records[jline][0] == line kind

#----- classes -----

class Buf:
    'paragraph buffer'

    def __init__(buf):
        buf.string = ''
        buf.indent = 0

    def __len__(buf):
        return len(buf.string)

    def append(buf, string, indent=0):
        if buf.string:
            buf.string += ' ' + shrink(string)
        else:
            buf.string = shrink(string)
            buf.indent = indent

    def flush(buf):
        if buf.string:
            prefix = (buf.indent - 2) * ' ' + '• ' if buf.indent else ''
            while len(buf.string) > Args.width - buf.indent:
                jchar = rfind(buf.string[:Args.width-buf.indent+1], ' ')
                if jchar <= 0:
                    error(f'Line {Glob.jline}, impossible to left-justify: {buf.string!r}')
                string, buf.string = buf.string[:jchar], buf.string[jchar+1:]
                if not Args.left_only: string = expand(string, Args.width - buf.indent)
                out.append('t', prefix + string)
                prefix = buf.indent * ' '
            if buf.string:
                out.append('t', prefix + buf.string)
                buf.string = ''

buf = Buf()

class Out:
    'output buffer'

    def __init__(out):
        out.records = []

    def __len__(out):
        return len(out.records)

    def append(out, kind, line):
        out.records.append((kind, line))

    def __call__(out, jline, jchar):
        try:
            if jline < 0 or jchar < 0: return ' '
            kind, line = out.records[jline]
            return line[jchar] if kind == PICT else ' '
        except IndexError:
            return ' '

    def pretty_lines(out):
        chstr = '#─│┐│┘│┤──┌┬└┴├┼'
        #        0123456789ABCDEF
        chset = frozenset(chstr)
        for jline, record in enumerate(out.records):
            kind, line = record
            if kind == PICT:
                chars = list(line)
                for jchar, char in enumerate(chars):
                    if char in chset:
                        chars[jchar] = chstr[1 * (out(jline, jchar - 1) in chset) +
                                             2 * (out(jline + 1, jchar) in chset) +
                                             4 * (out(jline - 1, jchar) in chset) +
                                             8 * (out(jline, jchar + 1) in chset)]
                out.records[jline] = (kind, ''.join(chars))

    def pretty_arrows(out):
        chstr = '@▷△@▽@@@◁@@@@@@@'
        #        0123456789ABCDEF
        chset = frozenset(chstr)
        for jline, record in enumerate(out.records):
            kind, line = record
            if kind == PICT:
                chars = list(line)
                for jchar, char in enumerate(chars):
                    if char in chset:
                        chars[jchar] = chstr[1 * (out(jline, jchar - 1) == '─') +
                                             2 * (out(jline + 1, jchar) == '│') +
                                             4 * (out(jline - 1, jchar) == '│') +
                                             8 * (out(jline, jchar + 1) == '─')]
                out.records[jline] = (kind, ''.join(chars))

    def pretty_chapters(out):
        jline_toc = -1
        jline_cp1 = -1
        out.chapters = []
        levels = []
        for jline, record in enumerate(out.records):
            kind, line = record
            if (kind == TEXT and line and line == line.upper() and
                (jline == 0 or not out.records[jline-1][1]) and
                (jline == len(out.records) - 1 or not out.records[jline+1][1])):
                if jline_toc < 0 and line[0] != line[0].lower(): # find content line
                    jline_toc = jline
                    out.records[jline] = (kind, shrink(line))
                else:
                    level = chapter_level(line) # find chapter lines
                    if level > 0:
                        if level > len(levels) + 1: error(f'Wrong chapter level sequence: {line!r}')
                        elif level == len(levels) + 1: levels.append(1)
                        else: levels = levels[:level]; levels[-1] += 1
                        line = '.'.join(str(n) for n in levels) + '. ' + shrink(line[find(line, ' '):])
                        out.records[jline] = (TEXT, line)
                        out.chapters.append(Args.tab_blanks + line.title())
                        if jline_cp1 < 0: jline_cp1 = jline
        if jline_toc < 0: error('Table of content line not found')
        elif jline_cp1 < 0: error('Chapter title lines not found')
        elif jline_cp1 < jline_toc: error(f'Line {jline_cp1}: Chapter title line before content line: {out.records[jline_cp1][1]!r}')
        else:
            del out.records[jline_toc+1:jline_cp1] # delete old table of contents
            for chapter in [''] + out.chapters[::-1] + ['']: # insert new table of contents
                out.records.insert(jline_toc + 1, (TEXT, chapter))

    def rewrite(out, file):
        with open(file, 'w') as file_w:
            for kind, line in out.records:
                print(line, file=file_w)
                if Args.print: print(line)                

out = Out()

#----- functions -----

def expand(string, width):
    'insert blanks into shrinked {string} until len({string}) == {width}'
    if len(string) >= width:
        return string
    if ' ' not in string[1:]:
        error(f'Line {Glob.jline}, impossible to right-justify: {buf.string!r}')
        return string
    chars = list(string)
    jchar = 0
    while True:
        if chars[jchar] != ' ' and chars[jchar + 1] == ' ':
            chars.insert(jchar + 1, ' ')
            if len(chars) == width:
                return ''.join(chars)
        jchar = jchar + 1 if jchar < len(chars) - 2 else 0

def chapter_level(line):
    'return 1 2 3... for chapter titles, 0 otherwise'
    status, level = 0, 0
    for char in line:
        if status == 0:
            if '0' <= char <= '9': status = 1
            else: break
        elif status == 1:
            if '0' <= char <= '9': status = 1
            elif char == '.': level += 1; status = 2
            else: break
        elif status == 2:
            if '0' <= char <= '9': status = 1
            elif char == ' ': return level
            else: break
    return 0

#----- main -----

def yawp(argv):
    'Yet Another Word Processor, an automatic word processor for text and Python files'

    parser = ArgumentParser(prog='yawp', formatter_class=RawDescriptionHelpFormatter, description=description)
    parser.add_argument('-V', '--version', action='version', version=f'yawp {version}')
    parser.add_argument('-v', '--verbose', action='store_true', help='show what happens')
    parser.add_argument('-u', '--undo', action='store_true', help='don\'t format, restore file to the previous version (default: backup and format)')
    parser.add_argument('-t', '--tab-blanks', type=int, default=4, help='blanks replacing a tab char in input (default: 4)')
    parser.add_argument('-w', '--width', type=int, default=89, help='output line width (default: 89)')
    parser.add_argument('-l', '--left-only', action='store_true', help='justify at left only (default: at left and right)')
    parser.add_argument('-g', '--pretty-graphics', action='store_true', help="replace '#' and '@' in pictures with lines and arrowheads")
    parser.add_argument('-c', '--pretty-chapters', action='store_true', help="manage table of contents and chapter titles")
    parser.add_argument('-p', '--print', action='store_true', help='at end print formatted (or restored) file on stdout')
    parser.add_argument('file', help='file to be formatted (or restored if -u/--undo)')
    parser.parse_args(argv[1:], Args)
    Args.tab_blanks *= ' '
    Args.file = longpath(Args.file)
    
    if Args.undo: # restore: backfile --> Args.file
        backfile = oldbackfile(Args.file)
        if not backfile: error(f'Backup file for file {shortpath(Args.file)!r} not found')
        if Args.verbose: inform(f'Restore of file {shortpath(Args.file)!r} from file {shortpath(backfile)!r}')
        if isfile(Args.file): remove(Args.file)
        rename(backfile, Args.file)
        if Args.print:
            if Args.verbose: inform(f'Printing of file {shortpath(Args.file)!r}')
            for line in open(Args.file):
                print(line.replace('\t', Args.tab_blanks).rstrip())
    else:
        if not isfile(Args.file): error(f'File {shortpath(Args.file)!r} not found') # Args.file --> input
        input = [line.replace('\t', Args.tab_blanks).rstrip() for line in open(Args.file)]
        is_python_file = Args.file.endswith('.py')
        format = not is_python_file 
        
        for Glob.jline, line in enumerate(input): # input --> out.records
            is_switch_line = is_python_file and "\'\'\'" in line
            if is_switch_line: format = not format
            if is_switch_line or not format: # Python code
                buf.flush()
                out.append('c', line)
            elif not line: # empty line
                buf.flush()
                out.append('t', line)
            else:
                jdot = findchar(line, '[! ]')
                if jdot >= 0 and line[jdot:jdot+2] in ['• ','. ']: # dot line
                    buf.flush()
                    buf.append(line[jdot+2:], indent=jdot+2)
                elif line[0] == ' ': # indented line
                    if buf:
                        buf.append(line)
                    else:
                        if len(line) > Args.width: error(f'Line {Glob.jline} is too long: {line!r}')
                        out.append('p', line)
                else: # unindented line
                    buf.append(line)
        buf.flush()
        if is_python_file and format:
            error('Python file, odd number of switch lines')

        if Args.pretty_graphics:
            out.pretty_lines()
            out.pretty_arrows()
        if Args.pretty_chapters:
            out.pretty_chapters()

        backfile = newbackfile(Args.file) # backup: Args.file --> backfile
        if Args.verbose: inform(f'Backup of file {shortpath(Args.file)!r} into file {shortpath(backfile)!r}')
        rename(Args.file, backfile)

        if Args.verbose: inform(f'Rewriting file {shortpath(Args.file)!r}') # out.records --> Args.file
        if Args.verbose and Args.print: inform(f'Printing file {shortpath(Args.file)!r}')
        out.rewrite(Args.file)

def main():
    try:
        simplefilter('ignore')
        yawp(argv)
    except KeyboardInterrupt:
        print()

if __name__ == '__main__':
    main()

#----- end -----

