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
Tests 'cc' module
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
args = ImportArguments('cc').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('CC: $CC'))
    print(env.subst('SHCC: $SHCC'))
    print(env.subst('CCFLAGS: $CCFLAGS'))
    print(env.subst('CCPCHFLAGS: $CCPCHFLAGS'))
    print(env.subst('CCPDBFLAGS: $CCPDBFLAGS'))
    print(env.subst('CFLAGS: $CFLAGS'))
    print(env.subst('CPPDEFINES: $CPPDEFINES'))
    print(env.subst('CPPFLAGS: $CPPFLAGS'))
    print(env.subst('CPPPATH: $CPPPATH'))
    print(env.subst('SHCCFLAGS: $SHCCFLAGS'))
    print(env.subst('SHCFLAGS: $SHCFLAGS'))
""")

test.run(['--help'])
lines = [
    'CC: The C compiler',
    'CCFLAGS: General options that are passed to the C and C++ compilers',
    'CCPCHFLAGS: Options added to the compiler command line to support building with precompiled headers',
    'CCPDBFLAGS: Options added to the compiler command line to support storing debugging information in a Microsoft Visual C++ PDB file',
    'CFLAGS: General options that are passed to the C compiler (C only; not C++).',
    'CPPDEFINES: A platform independent specification of C preprocessor definitions',
    'CPPFLAGS: User-specified C preprocessor options',
    'CPPPATH: The list of directories that the C preprocessor will search for include directories',
    'SHCC: The C compiler used for generating shared-library objects',
    'SHCCFLAGS: Options that are passed to the C and C++ compilers to generate shared-library objects',
    'SHCFLAGS: Options that are passed to the C compiler (only; not C++) to generate shared-library objects',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('CC=mycc')
test.must_contain_all_lines(test.stdout(), ['CC: mycc'])
test.run(['CCFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['CCFLAGS: --flag1 --flag2'])
test.run(['CCPCHFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['CCPCHFLAGS: --flag1 --flag2'])
test.run(['CCPDBFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['CCPDBFLAGS: --flag1 --flag2'])
test.run(['CFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['CFLAGS: --flag1 --flag2'])
test.run(['CPPDEFINES=-DFOO -DBAR=2'])
test.must_contain_all_lines(test.stdout(), ['CPPDEFINES: -DFOO -DBAR=2'])
test.run(['CPPFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['CPPFLAGS: --flag1 --flag2'])
test.run(['CPPPATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['CPPPATH: foo/path bar/path'])
test.run('SHCC=myshcc')
test.must_contain_all_lines(test.stdout(), ['SHCC: myshcc'])
test.run(['SHCCFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHCCFLAGS: --flag1 --flag2'])
test.run(['SHCFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHCFLAGS: --flag1 --flag2'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
