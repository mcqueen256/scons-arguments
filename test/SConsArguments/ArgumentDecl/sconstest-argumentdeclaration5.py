#
# Copyright (c) 2012-2015 by Pawel Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
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
Tests declaring variables with SConsArguments.ArgumentDeclaration()
"""

import TestSCons

##############################################################################
# ArgumentDeclaration(): Test 5 - test several calling conventions for ArgumentDeclaration().
##############################################################################
test = TestSCons.TestSCons()
test.dir_fixture('../../../SConsArguments', 'site_scons/SConsArguments')
test.write('SConstruct',
"""
# SConstruct
import SConsArguments
list = []
list.append( SConsArguments.ArgumentDeclaration(('env_x', 'env x default'),
                                         ('var_x','help var_x', 'var x default'),
                                         (('-x', '-xvar'), {'dest' : 'opt_x', 'default' : 'opt x default'})) )
list.append( SConsArguments.ArgumentDeclaration({'env_x': 'env x default'},
                                         {'key' : 'var_x', 'help' : 'help var_x', 'default' : 'var x default'},
                                         {'names' : ('-x', '-xvar'), 'dest' : 'opt_x', 'default' : 'opt x default'}) )
list.append( SConsArguments.ArgumentDeclaration({'env_x': 'env x default'},
                                         {'key' : 'var_x', 'help' : 'help var_x', 'default' : 'var x default'},
                                         {'names' : ('-x', '-xvar'), 'kw' : {'dest' : 'opt_x', 'default' : 'opt x default'}}) )
i = 0
for v in list:
    print "ARG[%d].has_decl(ENV): %r" % (i, v.has_decl(SConsArguments.ENV))
    print "ARG[%d].has_decl(VAR): %r" % (i, v.has_decl(SConsArguments.VAR))
    print "ARG[%d].has_decl(OPT): %r" % (i, v.has_decl(SConsArguments.OPT))
    print "ARG[%d].get_key(ENV): %r" % (i, v.get_key(SConsArguments.ENV))
    print "ARG[%d].get_key(VAR): %r" % (i, v.get_key(SConsArguments.VAR))
    print "ARG[%d].get_key(OPT): %r" % (i, v.get_key(SConsArguments.OPT))
    print "ARG[%d].get_default(ENV): %r" % (i, v.get_default(SConsArguments.ENV))
    print "ARG[%d].get_default(VAR): %r" % (i, v.get_default(SConsArguments.VAR))
    print "ARG[%d].get_default(OPT): %r" % (i, v.get_default(SConsArguments.OPT))
    i += 1
""")

test.run()

lines = [
  "ARG[0].has_decl(ENV): True",
  "ARG[0].has_decl(VAR): True",
  "ARG[0].has_decl(OPT): True",
  "ARG[0].get_key(ENV): 'env_x'",
  "ARG[0].get_key(VAR): 'var_x'",
  "ARG[0].get_key(OPT): 'opt_x'",
  "ARG[0].get_default(ENV): 'env x default'",
  "ARG[0].get_default(VAR): 'var x default'",
  "ARG[0].get_default(OPT): 'opt x default'",

  "ARG[1].has_decl(ENV): True",
  "ARG[1].has_decl(VAR): True",
  "ARG[1].has_decl(OPT): True",
  "ARG[1].get_key(ENV): 'env_x'",
  "ARG[1].get_key(VAR): 'var_x'",
  "ARG[1].get_key(OPT): 'opt_x'",
  "ARG[1].get_default(ENV): 'env x default'",
  "ARG[1].get_default(VAR): 'var x default'",
  "ARG[1].get_default(OPT): 'opt x default'",

  "ARG[2].has_decl(ENV): True",
  "ARG[2].has_decl(VAR): True",
  "ARG[2].has_decl(OPT): True",
  "ARG[2].get_key(ENV): 'env_x'",
  "ARG[2].get_key(VAR): 'var_x'",
  "ARG[2].get_key(OPT): 'opt_x'",
  "ARG[2].get_default(ENV): 'env x default'",
  "ARG[2].get_default(VAR): 'var x default'",
  "ARG[2].get_default(OPT): 'opt x default'",
]

test.must_contain_all_lines(test.stdout(), lines)

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
