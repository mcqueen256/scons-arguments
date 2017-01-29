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
Tests 'fortran' module
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
args = ImportArguments('fortran').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('FORTRAN: $FORTRAN'))
    print(env.subst('SHFORTRAN: $SHFORTRAN'))
    print(env.subst('FORTRANFLAGS: $FORTRANFLAGS'))
    print(env.subst('FORTRANMODDIR: $FORTRANMODDIR'))
    print(env.subst('FORTRANPATH: $FORTRANPATH'))
    print(env.subst('SHFORTRANFLAGS: $SHFORTRANFLAGS'))
""")

test.run(['--help'])
lines = [
    'FORTRAN: The default Fortran compiler for all versions of Fortran',
    'SHFORTRAN: The default Fortran compiler used for generating shared-library objects',
    'FORTRANFLAGS: General user-specified options that are passed to the Fortran compiler',
    'FORTRANMODDIR: Directory location where the Fortran compiler should place any module files it generates',
    'FORTRANPATH: The list of directories that the Fortran compiler will search for include files and (for some compilers) module files',
    'SHFORTRANFLAGS: Options that are passed to the Fortran compiler to generate shared-library objects'
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('FORTRAN=myfortran')
test.must_contain_all_lines(test.stdout(), ['FORTRAN: myfortran'])
test.run('SHFORTRAN=myshfortran')
test.must_contain_all_lines(test.stdout(), ['SHFORTRAN: myshfortran'])
test.run(['FORTRANFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['FORTRANFLAGS: --flag1 --flag2'])
test.run(['FORTRANMODDIR=mod/dir'])
test.must_contain_all_lines(test.stdout(), ['FORTRANMODDIR: mod/dir'])
test.run(['FORTRANPATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['FORTRANPATH: foo/path bar/path'])
test.run(['SHFORTRANFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['SHFORTRANFLAGS: --flag1 --flag2'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
