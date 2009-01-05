#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Localizer, Zope product that provides internationalization services
# Copyright (C) 2001 Andr�s Marzal Varo
#               2001-2002 J. David Ib��ez <j-david@noos.fr>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

"""
zgettext.py is a script that parses DTML files and generates .pot and .po
files, and then generates .mo files from the .po files.

Future (XXX):
  zgettext should provide a similar interface to xgettext, it just should
  detect dtml and zpt files, parse them, and call xgettext for the rest.

  another script should do the wrap up to easily create multilingual products,
  or maybe we could avoid this and just use make

  maybe even parse_po_file could disappear as it is now, and instead use the
  gettext tools

Anyway, the trend is to levereage the gettext tools as much as posible.
"""

__version__ = "$Revision$"


import codecs, os, re, sys, tempfile, time



def create_mo_files():
    for filename in [ x for x in os.listdir('locale') if x.endswith('.po') ]:
        language = filename[:-3]
        os.system('msgfmt locale/%s.po -o locale/%s.mo' % (language, language))


def unescape(s):
    s2 = ''
    state = 0
    for x in s:
        if state == 0:
            if x == '\\':
                state = 1
            else:
                s2 = s2 + x
        else:
            s2 = s2 + eval("'\%s'" % x)
            state = 0

    return s2


def parse_po_file(content):
    """
    Parses a PO file.

    XXX
    It's only used from MessageCatalog.py, maybe it should be moved there.
    Maybe the implementation could be changed to use the gettext tools.
    """
    # The regular expressions
    com = re.compile('^#.*')
    msgid = re.compile(r'^ *msgid *"(.*[^\\]*)"')
    msgstr = re.compile(r'^ *msgstr *"(.*[^\\]*)"')
    re_str = re.compile(r'^ *"(.*[^\\])"')
    blank = re.compile(r'^\s*$')
    quote_esc = re.compile(r'\\"')

    trans = {}
    pointer = 0
    state = 0
    COM, MSGID, MSGSTR = [], [], []
    while pointer < len(content):
        line = content[pointer]
        # print 'STATE:', state, 'LANGUAGE', language
        # print 'LINE:', content[pointer].strip()
        if state == 0:
            COM, MSGID, MSGSTR = [], [], []
            if com.match(line):
                COM.append(line.strip())
                state = 1
                pointer = pointer + 1
            elif msgid.match(line):
                line = msgid.match(line).group(1)
                MSGID.append(unescape(line))
                state = 2
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise 'ParseError', 'state 0, line %d\n' % (pointer + 1)
        elif state == 1:
            if com.match(line):
                COM.append(line.strip())
                state = 1
                pointer = pointer + 1
            elif msgid.match(line):
                line = msgid.match(line).group(1)
                MSGID.append(unescape(line))
                state = 2
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise 'ParseError', 'state 1, line %d\n' % (pointer + 1)
        elif state == 2:
            if com.match(line):
                COM.append(line.strip())
                state = 2
                pointer = pointer + 1
            elif re_str.match(line):
                line = re_str.match(line).group(1)
                MSGID.append(unescape(line))
                state = 2
                pointer = pointer + 1
            elif msgstr.match(line):
                line = msgstr.match(line).group(1)
                MSGSTR.append(unescape(line))
                state = 3
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise 'ParseError', 'state 2, line %d\n' % (pointer + 1)
        elif state == 3:
            if com.match(line) or msgid.match(line):
                # print "\nEn", language, "detected", MSGID
                trans[tuple(MSGID)] = (COM, MSGSTR)
                state = 0
            elif re_str.match(line):
                line = re_str.match(line).group(1)
                MSGSTR.append(unescape(line))
                state = 3
                pointer = pointer + 1
            elif blank.match(line):
                pointer = pointer + 1
            else:
                raise 'ParseError', 'state 3, line %d\n' % (pointer + 1)

    # Detect the encoding
    if trans.has_key(('',)):
        for x in trans[('',)][1]:
            if x.startswith('Content-Type: '):
                break
        x = x.strip()
        encoding = x.split('charset=')[-1]
    else:
        encoding = 'ascii'

    try:
        codecs.lookup(encoding)
    except LookupError:
        # Default encoding
        # XXX A warning should be issued
        encoding = 'utf8' 

    # the last also goes in
    if tuple(MSGID):
        trans[tuple(MSGID)] = (COM, MSGSTR)

    # Change (only) the translations to unicode strings
    for k, v in trans.items():
        trans[k] = (v[0], [ unicode(x, encoding) for x in v[1] ])

    return encoding, trans


def parse_generic(text, commands=('gettext', 'ugettext')):
    """
    Search for patterns like: gettext('message').

    XXX
    Originally it was used to parse Python code, but it fails to parse
    some of the Python strings, now xgettext is used instead. So currently
    this function is only used to parse DTML and ZPT; probably the regular
    expression could be simplified as in DTML and ZPT there're (maybe)
    less options for Python strings due to the syntax constrains of these
    languages.
    """
    r = []
    for command in commands:
        pattern = command + '\s*\(\s*(\'.*?[^\\\\]\'|\".*?[^\\\\]\")\s*\)'
        regex = re.compile(pattern, re.DOTALL)
        r.extend([ x[1:-1] for x in re.findall(regex, text) ])

    return r


def parse_dtml(text):
    """
    Extract the messages from a DTML template.
    """
    messages = parse_generic(text)

    # Search the "<dtml-gettext>message</dtml-gettext>" pattern
    regex = re.compile('<dtml-gettext(.*?)>(.*?)</dtml-gettext>', re.DOTALL)
    for parameters, message in re.findall(regex, text):
        if parameters.find('verbatim') == -1:
            message = ' '.join([ x.strip() for x in message.split() ])
        messages.append(message)

    return messages


def parse_zpt(text):
    """
    Extract the messages from a ZPT template.

    XXX It should be improved to parse the i18n namespace.
    """
    return parse_generic(text)


def do_all(filenames, languages):
    # Create the locale directory
    if not os.path.isdir('./locale'):
        try:
            os.mkdir('./locale')
        except OSError, msg:
            sys.stderr.write('Error: Cannot create directory "locale".\n%s\n'
                             % msg)
            sys.exit(1)

    # Create the pot file
    if not os.path.exists('locale/locale.pot'):
        f = open('locale/locale.pot', 'w')
        f.write("# SOME DESCRIPTIVE TITLE.\n")
        f.write("# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER\n")
        f.write("# This file is distributed under the same license as the PACKAGE package.\n")
        f.write("# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.\n")
        f.write("#\n")
        f.write("#, fuzzy\n")
        f.write('msgid ""\n')
        f.write('msgstr ""\n')
        f.write('"Project-Id-Version: PACKAGE VERSION\\n"\n')
        f.write('"POT-Creation-Date: %s\\n"\n'
                % time.strftime('%Y-%m-%d %H:%m+%Z', time.gmtime(time.time())))
        f.write('"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n')
        f.write('"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n')
        f.write('"Language-Team: LANGUAGE <LL@li.org>\\n"\n')
        f.write('"MIME-Version: 1.0\\n"\n')
        f.write('"Content-Type: text/plain; charset=CHARSET\\n"\n')
        f.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        f.close()

    # Filter and parse the DTML and ZPT files, the rest will be parsed
    # with xgettext.
    filenames2 = []
    messages = []
    for filename in filenames:
        filetype = filename.split('.')[-1]

        if filetype == 'dtml':
            text = open(filename).read()
            messages.extend(parse_dtml(text))
        elif filetype == 'zpt':
            text = open(filename).read()
            messages.extend(parse_zpt(text))
        else:
            filenames2.append(filename)

    filenames = []

    # Write a PO file with the messages from DTML and ZPT
    if messages:
        filename = tempfile.mktemp('.po')
        filenames.append(filename)

        f = open(filename, 'w')

        aux = []
        for message in messages:
            if message not in aux:
                f.write('msgid "%s"\n' % message)
                f.write('msgstr ""\n')
                f.write('\n')
            aux.append(message)
        f.close()

    # Parse the rest of the files
    if filenames2:
        filename = tempfile.mktemp('.po')
        filenames.append(filename)
        os.system('xgettext --omit-header --keyword=ugettext --keyword=N_ --output=%s %s' % (filename, ' '.join(filenames2)))


    # Create the POT file
    if filenames:
        filename = tempfile.mktemp('.po')
        os.system('msgcat --output-file=%s %s'
                  % (filename, ' '.join(filenames)))
        os.system('msgmerge -U locale/locale.pot %s' % filename)

        # Remove temporal files
        os.remove(filename)
        for filename in filenames:
            os.remove(filename)

    # Generate the PO files
    for language in languages:
        if os.path.exists('./locale/%s.po' % language):
            # a .po file already exist, merge it with locale.pot
            os.system('msgmerge -U locale/%s.po locale/locale.pot' % language)
        else:
            # po doesn't exist, just copy locale.pot
            text = open('./locale/locale.pot').read()
            open('./locale/%s.po' % language, 'w').write(text)




if __name__ == '__main__':
    # Parse the command line
    status = 0
    files = []
    langs = []
    for arg in sys.argv[1:]:
        if status == 0:
            if arg == '-h':
                status = 1
            elif arg == '-m':
                status = 2
            elif arg == '-l':
                status = 3
            else:
                files.append(arg)
                status = 4
        elif status == 1:
            status = 'Error'
            break
        elif status == 2:
            status = 'Error'
            break
        elif status == 3:
            langs.append(arg)
            status = 5
        elif status == 4:
            if arg == '-l':
                status = 3
            else:
                files.append(arg)
        elif status == 5:
            langs.append(arg)
        else:
            raise 'UknownStatus', str(status)

    # Action
    if status in (0, 1, 3, 'Error'):
        # Provide help if the line format is wrong or if the -h modifier
        # is provided
        print 'Usage:'
        print '  zgettext.py -h'
        print '    Shows this help message.'
        print '  zgettext.py [file file ... file] [-l languages]'
        print '    Parses all the specified files, creates the locale'
        print '    directory, creates the locale.pot file and the .po'
        print '    files of the languages specified.'
        print '  zgettxt.py -m'
        print '    Compiles all the .po files in the locale directory'
        print '    and creates the .mo files.'
        print
        print 'Examples:'
        print '  zgettext.py *.dtml -l ca es en'
        print '  zgettext.py -m'
    elif status == 2:
        create_mo_files()
    elif status in (4, 5):
        do_all(files, langs)
    else:
        raise 'UknownStatus', str(status)
