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
Tests 'ar' module
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
args = ImportArguments('ar').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('AR: $AR'))
    print(env.subst('ARFLAGS: $ARFLAGS'))
    print(env.subst('RANLIB: $RANLIB'))
    print(env.subst('RANLIBFLAGS: $RANLIBFLAGS'))
""")

test.run(['--help'])
lines = [
    'AR: The static library archiver',
    'ARFLAGS: General options passed to the static library archiver',
    'RANLIB: The archive indexer',
    'RANLIBFLAGS: General options passed to the archive indexer'
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('AR=myar')
test.must_contain_all_lines(test.stdout(), ['AR: myar'])
test.run(['ARFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['ARFLAGS: --flag1 --flag2'])
test.run('RANLIB=myranlib')
test.must_contain_all_lines(test.stdout(), ['RANLIB: myranlib'])
test.run(['RANLIBFLAGS=--flag3 --flag4'])
test.must_contain_all_lines(test.stdout(), ['RANLIBFLAGS: --flag3 --flag4'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
