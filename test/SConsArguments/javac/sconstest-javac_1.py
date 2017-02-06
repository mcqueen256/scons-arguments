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
Tests 'javac' module
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
args = ImportArguments('javac').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('JAVAC: $JAVAC'))
    print(env.subst('JAVACFLAGS: $JAVACFLAGS'))
    print(env.subst('JAVACLASSPATH: $JAVACLASSPATH'))
    print(env.subst('JAVASOURCEPATH: $JAVASOURCEPATH'))
    print(env.subst('JAVAH: $JAVAH'))
    print(env.subst('JAVAHFLAGS: $JAVAHFLAGS'))
""")

test.run(['--help'])
lines = [
    'JAVAC: The Java compiler',
    'JAVACFLAGS: General options that are passed to the Java compiler',
    'JAVACLASSPATH: Specifies the list of directories that will be searched for Java .class file',
    'JAVASOURCEPATH: Specifies the list of directories that will be searched for input .java file',
    'JAVAH: The Java generator for C header and stub files',
    'JAVAHFLAGS: General options passed to the C header and stub file generator for Java classes'
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('JAVAC=myjavac')
test.must_contain_all_lines(test.stdout(), ['JAVAC: myjavac'])
test.run('JAVAH=myjavah')
test.must_contain_all_lines(test.stdout(), ['JAVAH: myjavah'])
test.run(['JAVACFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['JAVACFLAGS: --flag1 --flag2'])
test.run(['JAVACLASSPATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['JAVACLASSPATH: foo/path bar/path'])
test.run(['JAVASOURCEPATH=foo/path:bar/path'])
test.must_contain_all_lines(test.stdout(), ['JAVASOURCEPATH: foo/path bar/path'])
test.run(['JAVAHFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['JAVAHFLAGS: --flag1 --flag2'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
