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
Tests 'f95' module
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
args = ImportArguments('f95').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('F95: $F95'))
    print(env.subst('SHF95: $SHF95'))
    print(env.subst('F95FLAGS: $F95FLAGS'))
    print(env.subst('F95PATH: $F95PATH'))
    print(env.subst('SHF95FLAGS: $SHF95FLAGS'))
""")

test.run(['--help'])
lines = [
    'F95: The Fortran 95 compiler',
    'SHF95: The Fortran 95 compiler used for generating shared-library objects',
    'F95FLAGS: General user-specified options that are passed to the Fortran 95 compiler',
    'F95PATH: The list of directories that the Fortran 95 compiler will search for include directories',
    'SHF95FLAGS: Options that are passed to the Fortran 95 compiler to generated shared-library objects',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('F95=myf95')
test.must_contain_all_lines(test.stdout(), ['F95: myf95'])
test.run('SHF95=myshf95')
test.must_contain_all_lines(test.stdout(), ['SHF95: myshf95'])
test.run(['F95FLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['F95FLAGS: --flag1 --flag2'])
test.run(['F95PATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['F95PATH: foo/path bar/path'])
test.run(['SHF95FLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHF95FLAGS: --flag1 --flag2'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
