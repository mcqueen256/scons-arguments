""" `SConsArgumentsT.NameConvTests`

Unit tests for SConsArguments.NameConv
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2015-2016 by Pawel Tomulik
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

import SConsArguments.NameConv
import unittest

#############################################################################
class Test__ArgumentNameConv(unittest.TestCase):
    def test__ArgumentNameConv_1(self):
        """Test default _ArgumentNameConv instance"""
        tr = SConsArguments.NameConv._ArgumentNameConv()
        self.assertEquals(tr.env_key_transform('FOO'), 'FOO')
        self.assertEquals(tr.var_key_transform('FOO'), 'FOO')
        self.assertEquals(tr.opt_key_transform('FOO'), 'foo')
        self.assertEquals(tr.option_transform('FOO'), '--foo')

    def test__ArgumentNameConv_2(self):
        """Test _ArgumentNameConv with prefixes/suffixes"""
        tr = SConsArguments.NameConv._ArgumentNameConv(env_key_prefix = 'ENV_', env_key_suffix = '_VNE',
                                                       var_key_prefix = 'VAR_', var_key_suffix = '_RAV',
                                                       opt_key_prefix = 'OPT_', opt_key_suffix = '_TPO',
                                                       opt_prefix     = '-',
                                                       opt_name_prefix = 'on_', opt_name_suffix = '_no')
        self.assertEquals(tr.env_key_transform('FOO'), 'ENV_FOO_VNE')
        self.assertEquals(tr.var_key_transform('FOO'), 'VAR_FOO_RAV')
        self.assertEquals(tr.opt_key_transform('FOO'), 'OPT_foo_TPO')
        self.assertEquals(tr.option_transform('FOO'), '-on-foo-no')

    def test__ArgumentNameConv_3(self):
        """Test _ArgumentNameConv with prefixes/suffixes changed on existing object"""
        tr = SConsArguments.NameConv._ArgumentNameConv()
        tr.env_key_prefix = 'ENV_'
        tr.env_key_suffix = '_VNE'
        tr.var_key_prefix = 'VAR_'
        tr.var_key_suffix = '_RAV'
        tr.opt_key_prefix = 'OPT_'
        tr.opt_key_suffix = '_TPO'
        tr.opt_prefix     = '-'
        tr.opt_name_prefix = 'on_'
        tr.opt_name_suffix = '_no'
        self.assertEquals(tr.env_key_transform('FOO'), 'ENV_FOO_VNE')
        self.assertEquals(tr.var_key_transform('FOO'), 'VAR_FOO_RAV')
        self.assertEquals(tr.opt_key_transform('FOO'), 'OPT_foo_TPO')
        self.assertEquals(tr.option_transform('FOO'), '-on-foo-no')

    def test__ArgumentNameConv_4(self):
        """Test _ArgumentNameConv with custom lambdas"""
        tr = SConsArguments.NameConv._ArgumentNameConv(env_key_transform = lambda x : x.lower().capitalize(),
                                                       var_key_transform = lambda x : x.upper(),
                                                       opt_key_transform = lambda x : x.lower(),
                                                       option_transform = lambda x : '--' + x.lower() + '-option' )
        self.assertEquals(tr.env_key_transform('FOO'), 'Foo')
        self.assertEquals(tr.var_key_transform('foo'), 'FOO')
        self.assertEquals(tr.opt_key_transform('FOO'), 'foo')
        self.assertEquals(tr.option_transform('FOO'), '--foo-option')

    def test__ArgumentNameConv_5(self):
        """Test _ArgumentNameConv with True instead of lambdas"""
        tr = SConsArguments.NameConv._ArgumentNameConv(env_key_transform = True,
                                                       var_key_transform = True,
                                                       opt_key_transform = True,
                                                       option_transform = True)
        self.assertEquals(tr.env_key_transform('FOO'), 'FOO')
        self.assertEquals(tr.var_key_transform('FOO'), 'FOO')
        self.assertEquals(tr.opt_key_transform('FOO'), 'foo')
        self.assertEquals(tr.option_transform('FOO'), '--foo')

    def test__ArgumentNameConv_6(self):
        """Test _ArgumentNameConv with False instead of lambdas"""
        tr = SConsArguments.NameConv._ArgumentNameConv(env_key_transform = False,
                                                       var_key_transform = False,
                                                       opt_key_transform = False,
                                                       option_transform = False)
        self.assertIs(tr.env_key_transform('FOO'), None)
        self.assertIs(tr.var_key_transform('FOO'), None)
        self.assertIs(tr.opt_key_transform('FOO'), None)
        self.assertIs(tr.option_transform('FOO'),  None)

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test__ArgumentNameConv
               ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
