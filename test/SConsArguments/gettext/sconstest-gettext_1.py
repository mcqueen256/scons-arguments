#
# Copyright (c) 2012-2017 by Pawel Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), todeal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

__docformat__ = "restructuredText"

"""
Tests 'gettext' module
"""

import TestSCons

test = TestSCons.TestSCons()
test.dir_fixture('../../../SConsArguments', 'site_scons/SConsArguments')
test.write('SConstruct',
"""
# SConstruct
from SConsArguments import ImportArguments

env = Environment()
var = Variables()
args = ImportArguments('gettext').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('MSGFMT: $MSGFMT'))
    print(env.subst('MSGFMTFLAGS: $MSGFMTFLAGS'))
    print(env.subst('MSGINIT: $MSGINIT'))
    print(env.subst('MSGINITFLAGS: $MSGINITFLAGS'))
    print(env.subst('MSGMERGE: $MSGMERGE'))
    print(env.subst('MSGMERGEFLAGS: $MSGMERGEFLAGS'))
    print(env.subst('XGETTEXT: $XGETTEXT'))
    print(env.subst('XGETTEXTFLAGS: $XGETTEXTFLAGS'))
    print(env.subst('XGETTEXTPATH: $XGETTEXTPATH'))
""")

test.run(['--help'])
lines = [
    'MSGFMT: The msgfmt executable',
    'MSGFMTFLAGS: General user options passed to msgfmt',
    'MSGINIT: The msginit executable',
    'MSGINITFLAGS: General user options passed to msginit',
    'MSGMERGE: The msgmerge executable',
    'MSGMERGEFLAGS: General user options passed to msgmerge',
    'XGETTEXT: The xgettext executable',
    'XGETTEXTFLAGS: General user flags passed to xgettext.',
    'XGETTEXTPATH: List of directories, where xgettext will look for source files',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('MSGFMT=mymsgfmt')
test.must_contain_all_lines(test.stdout(), ['MSGFMT: mymsgfmt'])
test.run(['MSGFMTFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['MSGFMTFLAGS: --flag1 --flag2'])
test.run('MSGINIT=mymsginit')
test.must_contain_all_lines(test.stdout(), ['MSGINIT: mymsginit'])
test.run(['MSGINITFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['MSGINITFLAGS: --flag1 --flag2'])
test.run('MSGMERGE=mymsgmerge')
test.must_contain_all_lines(test.stdout(), ['MSGMERGE: mymsgmerge'])
test.run(['MSGMERGEFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['MSGMERGEFLAGS: --flag1 --flag2'])
test.run('XGETTEXT=myxgettext')
test.must_contain_all_lines(test.stdout(), ['XGETTEXT: myxgettext'])
test.run(['XGETTEXTFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['XGETTEXTFLAGS: --flag1 --flag2'])
test.run(['XGETTEXTPATH=first/path:second/path'])
test.must_contain_all_lines(test.stdout(), ['XGETTEXTPATH: first/path second/path'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
