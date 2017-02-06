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
Tests 'cvs' module
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
args = ImportArguments('cvs').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('CVS: $CVS'))
    print(env.subst('CVSCOFLAGS: $CVSCOFLAGS'))
    print(env.subst('CVSFLAGS: $CVSFLAGS'))
""")

test.run(['--help'])
lines = [
    'CVS: The CVS executable',
    'CVSCOFLAGS: Options that are passed to the CVS checkout subcommand',
    'CVSFLAGS: General options that are passed to CVS'
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('CVS=mycvs')
test.must_contain_all_lines(test.stdout(), ['CVS: mycvs'])
test.run(['CVSCOFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['CVSCOFLAGS: --flag1 --flag2'])
test.run(['CVSFLAGS=--flag3 --flag4'])
test.must_contain_all_lines(test.stdout(), ['CVSFLAGS: --flag3 --flag4'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4: