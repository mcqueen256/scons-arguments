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
Tests importing argument modules with SConsArguments.ImportArguments() when
module name clashes with other existing (already imported) module
"""

import TestSCons

##############################################################################
# ImportArguments(): Test 1 - import from SConsArguments/foo.py
##############################################################################
test = TestSCons.TestSCons()
test.dir_fixture('../../../SConsArguments', 'site_scons/SConsArguments')
test.write('site_scons/foo.py',
"""
# foo.py
def foo():
    pass
""")
test.write('site_scons/SConsArguments/foo.py',
"""
# SConsArguments/foo.py
def arguments():
    return {
        'arg1' : {'help' : 'This is arg1'},
        'arg2' : {'help' : 'This is arg2'}
    }
""")
test.write('SConstruct',
"""
# SConstruct
import foo
from SConsArguments import ImportArguments

foo.foo()


env = Environment()
var = Variables()
args = ImportArguments('foo').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('arg1: $arg1'))
    print(env.subst('arg2: $arg2'))
""")

test.run(['--help'])
lines = [ 'arg1: This is arg1', 'arg2: This is arg2' ]
test.must_contain_all_lines(test.stdout(), lines)

test.run(['arg1=A', 'arg2=B'])
lines = [ 'arg1: A', 'arg2: B' ]
test.must_contain_all_lines(test.stdout(), lines)

test.run(['arg1=X', 'arg2=$arg1'])
lines = [ 'arg1: X', 'arg2: X' ]

test.must_contain_all_lines(test.stdout(), lines)

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
