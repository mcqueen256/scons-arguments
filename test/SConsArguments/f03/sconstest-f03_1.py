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
Tests 'f03' module
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
args = ImportArguments('f03').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('F03: $F03'))
    print(env.subst('SHF03: $SHF03'))
    print(env.subst('F03FLAGS: $F03FLAGS'))
    print(env.subst('F03PATH: $F03PATH'))
    print(env.subst('SHF03FLAGS: $SHF03FLAGS'))
""")

test.run(['--help'])
lines = [
    'F03: The Fortran 03 compiler',
    'SHF03: The Fortran 03 compiler used for generating shared-library objects',
    'F03FLAGS: General user-specified options that are passed to the Fortran 03 compiler',
    'F03PATH: The list of directories that the Fortran 03 compiler will search for include directories',
    'SHF03FLAGS: Options that are passed to the Fortran 03 compiler to generated shared-library objects',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('F03=myf03')
test.must_contain_all_lines(test.stdout(), ['F03: myf03'])
test.run('SHF03=myshf03')
test.must_contain_all_lines(test.stdout(), ['SHF03: myshf03'])
test.run(['F03FLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['F03FLAGS: --flag1 --flag2'])
test.run(['F03PATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['F03PATH: foo/path bar/path'])
test.run(['SHF03FLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHF03FLAGS: --flag1 --flag2'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
