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
Tests 'f90' module
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
args = ImportArguments('f90').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('F90: $F90'))
    print(env.subst('SHF90: $SHF90'))
    print(env.subst('F90FLAGS: $F90FLAGS'))
    print(env.subst('F90PATH: $F90PATH'))
    print(env.subst('SHF90FLAGS: $SHF90FLAGS'))
""")

test.run(['--help'])
lines = [
    'F90: The Fortran 90 compiler',
    'SHF90: The Fortran 90 compiler used for generating shared-library objects',
    'F90FLAGS: General user-specified options that are passed to the Fortran 90 compiler',
    'F90PATH: The list of directories that the Fortran 90 compiler will search for include directories',
    'SHF90FLAGS: Options that are passed to the Fortran 90 compiler to generated shared-library objects',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('F90=myf90')
test.must_contain_all_lines(test.stdout(), ['F90: myf90'])
test.run('SHF90=myshf90')
test.must_contain_all_lines(test.stdout(), ['SHF90: myshf90'])
test.run(['F90FLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['F90FLAGS: --flag1 --flag2'])
test.run(['F90PATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['F90PATH: foo/path bar/path'])
test.run(['SHF90FLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHF90FLAGS: --flag1 --flag2'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
