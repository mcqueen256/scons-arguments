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
Tests 'link' module
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
args = ImportArguments('link').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('LDMODULE: $LDMODULE'))
    print(env.subst('LDMODULEFLAGS: $LDMODULEFLAGS'))
    print(env.subst('LIBPATH: $LIBPATH'))
    print(env.subst('LINK: $LINK'))
    print(env.subst('LINKFLAGS: $LINKFLAGS'))
    print(env.subst('SHLIBVERSIONFLAGS: $SHLIBVERSIONFLAGS'))
    print(env.subst('SHLINK: $SHLINK'))
    print(env.subst('SHLINKFLAGS: $SHLINKFLAGS'))
""")

test.run(['--help'])
lines = [
    'LDMODULE: The linker for building loadable modules',
    'LDMODULEFLAGS: General user options passed to the linker for building loadable modules',
    'LIBPATH: The list of directories that will be searched for libraries',
    'LINK: The linker',
    'LINKFLAGS: General user options passed to the linker',
    'SHLIBVERSIONFLAGS: Extra flags added to $SHLINKCOM when building versioned SharedLibrary',
    'SHLINK: The linker for programs that use shared libraries',
    'SHLINKFLAGS: General user options passed to the linker for programs using shared libraries',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('LDMODULE=myldmodule')
test.must_contain_all_lines(test.stdout(), ['LDMODULE: myldmodule'])
test.run(['LDMODULEFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['LDMODULEFLAGS: --flag1 --flag2'])
test.run(['LIBPATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['LIBPATH: foo/path bar/path'])
test.run('LINK=mylink')
test.must_contain_all_lines(test.stdout(), ['LINK: mylink'])
test.run(['LINKFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['LINKFLAGS: --flag1 --flag2'])
test.run(['SHLIBVERSIONFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHLIBVERSIONFLAGS: --flag1 --flag2'])
test.run('SHLINK=myshlink')
test.must_contain_all_lines(test.stdout(), ['SHLINK: myshlink'])
test.run(['SHLINKFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHLINKFLAGS: --flag1 --flag2'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
