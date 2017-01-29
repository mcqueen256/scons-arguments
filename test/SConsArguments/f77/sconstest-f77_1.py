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
Tests 'f77' module
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
args = ImportArguments('f77').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('F77: $F77'))
    print(env.subst('SHF77: $SHF77'))
    print(env.subst('F77FLAGS: $F77FLAGS'))
    print(env.subst('F77PATH: $F77PATH'))
    print(env.subst('SHF77FLAGS: $SHF77FLAGS'))
""")

test.run(['--help'])
lines = [
    'F77: The Fortran 77 compiler',
    'SHF77: The Fortran 77 compiler used for generating shared-library objects',
    'F77FLAGS: General user-specified options that are passed to the Fortran 77 compiler',
    'F77PATH: The list of directories that the Fortran 77 compiler will search for include directories',
    'SHF77FLAGS: Options that are passed to the Fortran 77 compiler to generated shared-library objects',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('F77=myf77')
test.must_contain_all_lines(test.stdout(), ['F77: myf77'])
test.run('SHF77=myshf77')
test.must_contain_all_lines(test.stdout(), ['SHF77: myshf77'])
test.run(['F77FLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['F77FLAGS: --flag1 --flag2'])
test.run(['F77PATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['F77PATH: foo/path bar/path'])
test.run(['SHF77FLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHF77FLAGS: --flag1 --flag2'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
