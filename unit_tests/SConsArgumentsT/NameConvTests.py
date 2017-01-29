""" `SConsArgumentsT.NameConvTests`

Unit tests for `SConsArguments.NameConv`
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
        nc = SConsArguments.NameConv._ArgumentNameConv()
        self.assertEquals(nc.name2env('FOO'), 'FOO')
        self.assertEquals(nc.name2var('FOO'), 'FOO')
        self.assertEquals(nc.name2opt('FOO'), 'foo')
        self.assertEquals(nc.name2option('FOO'), '--foo')

    def test__ArgumentNameConv_2(self):
        """Test _ArgumentNameConv with prefixes/suffixes"""
        nc = SConsArguments.NameConv._ArgumentNameConv(env_key_prefix = 'ENV_', env_key_suffix = '_VNE',
                                                       var_key_prefix = 'VAR_', var_key_suffix = '_RAV',
                                                       opt_key_prefix = 'OPT_', opt_key_suffix = '_TPO',
                                                       opt_prefix     = '-',
                                                       opt_name_prefix = 'on_', opt_name_suffix = '_no')
        self.assertEquals(nc.name2env('FOO'), 'ENV_FOO_VNE')
        self.assertEquals(nc.name2var('FOO'), 'VAR_FOO_RAV')
        self.assertEquals(nc.name2opt('FOO'), 'OPT_foo_TPO')
        self.assertEquals(nc.name2option('FOO'), '-on-foo-no')

    def test__ArgumentNameConv_3(self):
        """Test _ArgumentNameConv with prefixes/suffixes changed on existing object"""
        nc = SConsArguments.NameConv._ArgumentNameConv()
        nc.env_key_prefix = 'ENV_'
        nc.env_key_suffix = '_VNE'
        nc.var_key_prefix = 'VAR_'
        nc.var_key_suffix = '_RAV'
        nc.opt_key_prefix = 'OPT_'
        nc.opt_key_suffix = '_TPO'
        nc.opt_prefix     = '-'
        nc.opt_name_prefix = 'on_'
        nc.opt_name_suffix = '_no'
        self.assertEquals(nc.name2env('FOO'), 'ENV_FOO_VNE')
        self.assertEquals(nc.name2var('FOO'), 'VAR_FOO_RAV')
        self.assertEquals(nc.name2opt('FOO'), 'OPT_foo_TPO')
        self.assertEquals(nc.name2option('FOO'), '-on-foo-no')

    def test__ArgumentNameConv_4(self):
        """Test _ArgumentNameConv with custom lambdas"""
        nc = SConsArguments.NameConv._ArgumentNameConv(env_key_transform = lambda x : x.lower().capitalize(),
                                                       var_key_transform = lambda x : x.upper(),
                                                       opt_key_transform = lambda x : x.lower(),
                                                       opt_name_transform = lambda x : x.lower() + '-option' )
        self.assertEquals(nc.name2env('FOO'), 'Foo')
        self.assertEquals(nc.name2var('foo'), 'FOO')
        self.assertEquals(nc.name2opt('FOO'), 'foo')
        self.assertEquals(nc.name2option('FOO'), '--foo-option')

    def test__ArgumentNameConv_5(self):
        """Test _ArgumentNameConv with True instead of lambdas"""
        nc = SConsArguments.NameConv._ArgumentNameConv(env_key_transform = True,
                                                       var_key_transform = True,
                                                       opt_key_transform = True,
                                                       option_transform = True)
        self.assertEquals(nc.name2env('FOO'), 'FOO')
        self.assertEquals(nc.name2var('FOO'), 'FOO')
        self.assertEquals(nc.name2opt('FOO'), 'foo')
        self.assertEquals(nc.name2option('FOO'), '--foo')

    def test__ArgumentNameConv_6(self):
        """Test _ArgumentNameConv with False instead of lambdas"""
        nc = SConsArguments.NameConv._ArgumentNameConv(env_key_transform = False,
                                                       var_key_transform = False,
                                                       opt_key_transform = False,
                                                       option_transform = False)
        self.assertIs(nc.name2env('FOO'), None)
        self.assertIs(nc.name2var('FOO'), None)
        self.assertIs(nc.name2opt('FOO'), None)
        self.assertIs(nc.name2option('FOO'),  None)

    def test__ArgumentNameConv_name2dict_1(self):
        """Test _ArgumentNameConv.name2dict() with default settings"""
        nc = SConsArguments.NameConv._ArgumentNameConv()
        d = nc.name2dict('FOO')
        self.assertEqual(d, {'env_key' : 'FOO',
                             'var_key' : 'FOO',
                             'opt_key' : 'foo',
                             'option'  : '--foo'})

    def test__ArgumentNameConv_name2dict_2(self):
        """Test _ArgumentNameConv.name2dict() with custom prefixes"""
        nc = SConsArguments.NameConv._ArgumentNameConv(env_key_prefix = 'ENV_',
                                                       env_key_suffix = '_VNE',
                                                       var_key_prefix = 'VAR_',
                                                       var_key_suffix = '_RAV',
                                                       opt_key_prefix = 'OPT_',
                                                       opt_key_suffix = '_TPO',
                                                       opt_name_prefix = 'ON_',
                                                       opt_name_suffix = '_NO')
        d = nc.name2dict('FOO')
        self.assertEqual(d, {'env_key' : 'ENV_FOO_VNE',
                             'var_key' : 'VAR_FOO_RAV',
                             'opt_key' : 'OPT_foo_TPO',
                             'option'  : '--ON-foo-NO'})

    def test__ArgumentNameConv_name2dict_3(self):
        """Test _ArgumentNameConv.name2dict() with null transformers"""
        nc1 = SConsArguments.NameConv._ArgumentNameConv(env_key_transform = False,
                                                        var_key_transform = False,
                                                        opt_key_transform = False,
                                                        opt_name_transform = False)
        d1 = nc1.name2dict('FOO')
        self.assertEqual(d1, {})

        nc2 = SConsArguments.NameConv._ArgumentNameConv(env_key_transform = False,
                                                        var_key_transform = False,
                                                        opt_key_transform = False,
                                                        option_transform = False)
        d2 = nc2.name2dict('FOO')
        self.assertEqual(d2, {})

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
