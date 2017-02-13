""" `SConsArgumentsT.ArgumentsTests`

Unit tests for `SConsArguments.Arguments`
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2015 by Pawel Tomulik
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

import SConsArguments.Arguments
import unittest

# The mock module does not come as a part of python 2.x stdlib, it has to be
# installed separatelly. Here we detect whether mock is present and if not,
# we skip all the tests that use mock.
_mock_missing = True
try:
    # Try unittest.mock first (python 3.x) ...
    import unittest.mock as mock
    _mock_missing = False
except ImportError:
    try:
        # ... then try mock (python 2.x)
        import mock
        _mock_missing = False
    except ImportError:
        # mock not installed
        pass

#############################################################################
class Test__Arguments(unittest.TestCase):

    @classmethod
    def _decls_mock_1(cls):
        # decls0 is a substitute of _ArgumentDeclarations instance, with only keys()
        # method defined
        decls = mock.Mock(name = 'decls0')
        decls.keys = mock.Mock(name = 'keys', return_value = ['k','e','y','s'])
        return decls

    @classmethod
    def _decls_mock_2(cls):
        decls = cls._decls_mock_1()
        return cls._mock_decls_supp_dicts_2(decls)

    @classmethod
    def _decls_mock_3(cls):
        decls = cls._decls_mock_1()
        return cls._mock_decls_supp_dicts_3(decls)

    @classmethod
    def _decls_mock_4(cls):
        decls = cls._decls_mock_1()
        return cls._mock_decls_supp_dicts_4(decls)

    @classmethod
    def _decls_mock_5(cls):
        decls = cls._decls_mock_1()
        return cls._mock_decls_supp_dicts_5(decls)

    @classmethod
    def _arguments_mock_4_UpdateEnvironment(cls):
        args = SConsArguments.Arguments._Arguments(cls._decls_mock_1())
        args.update_env_from_vars = mock.Mock(name = 'update_env_from_vars')
        args.update_env_from_opts = mock.Mock(name = 'update_env_from_opts')
        return args

    @classmethod
    def _mock_decls_supp_dicts_2(cls, decls):
        def get_rename_dict(xxx):   return "rename_dict[%d]" % xxx
        def get_resubst_dict(xxx):  return "resubst_dict[%d]" % xxx
        def get_irename_dict(xxx):  return "irename_dict[%d]" % xxx
        def get_iresubst_dict(xxx): return "iresubst_dict[%d]" % xxx
        decls.get_rename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_rename_dict)
        decls.get_irename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_irename_dict)
        decls.get_resubst_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_resubst_dict)
        decls.get_iresubst_dict = mock.Mock(name = 'get_iresubst_dict',  side_effect = get_iresubst_dict)
        return decls

    @classmethod
    def _mock_decls_supp_dicts_3(cls, decls):
        def get_rename_dict(xxx):   return None
        def get_resubst_dict(xxx):  return None
        def get_irename_dict(xxx):  return None
        def get_iresubst_dict(xxx): return None
        decls.get_rename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_rename_dict)
        decls.get_irename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_irename_dict)
        decls.get_resubst_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_resubst_dict)
        decls.get_iresubst_dict = mock.Mock(name = 'get_iresubst_dict',  side_effect = get_iresubst_dict)
        return decls

    @classmethod
    def _mock_decls_supp_dicts_4(cls, decls):
        def get_rename_dict(xxx):
            return  [ {'a' : 'env_a'},    {'a' : 'var_a'},    {'a' : 'opt_a'}    ][xxx]
        def get_resubst_dict(xxx):
            return  [ {'a' : '${env_a}'}, {'a' : '${var_a}'}, {'a' : '${opt_a}'} ][xxx]
        def get_irename_dict(xxx):
            return  [ {'env_a' : 'a'},    {'var_a' : 'a'},    {'opt_a' : 'a'}    ][xxx]
        def get_iresubst_dict(xxx):
            return  [ {'env_a' : '${a}'}, {'var_a' : '${a}'}, {'opt_a' : '${a}'} ][xxx]
        decls.get_rename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_rename_dict)
        decls.get_irename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_irename_dict)
        decls.get_resubst_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_resubst_dict)
        decls.get_iresubst_dict = mock.Mock(name = 'get_iresubst_dict',  side_effect = get_iresubst_dict)
        return decls

    @classmethod
    def _mock_decls_supp_dicts_5(cls, decls):
        def get_rename_dict(xxx):
            return  [
                {'k' : 'env_k', 'e' : 'env_e', 'y' : 'env_y', 's' : 'env_s'},
                {'k' : 'var_k', 'e' : 'var_e', 'y' : 'var_y', 's' : 'var_s'},
                {'k' : 'opt_k', 'e' : 'opt_e', 'y' : 'opt_y', 's' : 'opt_s'}
            ][xxx]
        def get_resubst_dict(xxx):
            return  [
                {'k' : '${env_k}', 'e' : '${env_e}', 'y' : '${env_y}', 's' : '${env_s}'},
                {'k' : '${var_k}', 'e' : '${var_e}', 'y' : '${var_y}', 's' : '${var_s}'},
                {'k' : '${opt_k}', 'e' : '${opt_e}', 'y' : '${opt_y}', 's' : '${opt_s}'}
            ][xxx]
        def get_irename_dict(xxx):
            return  [
                {'env_k' : 'k', 'env_e' : 'e', 'env_y' : 'y', 'env_s' : 's' },
                {'var_k' : 'k', 'var_e' : 'e', 'var_y' : 'y', 'var_s' : 's' },
                {'opt_k' : 'k', 'opt_e' : 'e', 'opt_y' : 'y', 'opt_s' : 's' }
            ][xxx]
        def get_iresubst_dict(xxx):
            return  [
                {'env_k' : '${k}','env_e' : '${e}',  'env_y' : '${y}', 'env_s' : '${s}' },
                {'var_k' : '${k}','var_e' : '${e}',  'var_y' : '${y}', 'var_s' : '${s}' },
                {'opt_k' : '${k}','opt_e' : '${e}',  'opt_y' : '${y}', 'opt_s' : '${s}' },
            ][xxx]
        decls.get_rename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_rename_dict)
        decls.get_irename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_irename_dict)
        decls.get_resubst_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_resubst_dict)
        decls.get_iresubst_dict = mock.Mock(name = 'get_iresubst_dict',  side_effect = get_iresubst_dict)
        return decls

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___init___1(self):
        """_Arguments.__init__(decls) should call decls.keys() and self.__init_supp_dicts(decls)"""
        decls = self._decls_mock_1()
        with mock.patch.object(SConsArguments.Arguments._Arguments, '_Arguments__init_supp_dicts', autospec=True) as m:
            args = SConsArguments.Arguments._Arguments(decls)
            try:
                m.assert_called_once_with(args, decls)
                decls.keys.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))
        self.assertIsInstance(args, SConsArguments.Arguments._Arguments)
        self.assertEqual(args._Arguments__keys, ['k', 'e', 'y', 's'])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___init___2(self):
        """_Arguments.__init__(decls) should initialize its iternal dicts"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_2())
        self.assertEqual(args._rename_dict, ['rename_dict[0]', 'rename_dict[1]', 'rename_dict[2]'])
        self.assertEqual(args._resubst_dict, ['resubst_dict[0]', 'resubst_dict[1]', 'resubst_dict[2]'])
        self.assertEqual(args._irename_dict, ['irename_dict[0]', 'irename_dict[1]', 'irename_dict[2]'])
        self.assertEqual(args._iresubst_dict, ['iresubst_dict[0]', 'iresubst_dict[1]', 'iresubst_dict[2]'])


    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___reset_supp_dicts(self):
        """<_Arguments>.__reset_supp_dicts() should reset internal dicts to {}"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_2())
        args._Arguments__reset_supp_dicts()
        self.assertEqual(args._rename_dict, [{},{},{}])
        self.assertEqual(args._resubst_dict, [{},{},{}])
        self.assertEqual(args._irename_dict, [{},{},{}])
        self.assertEqual(args._iresubst_dict, [{},{},{}])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___init_supp_dicts(self):
        """<_Arguments>.__init_supp_dicts(decls) should initialize internal dicts appropriately"""
        decls = self._decls_mock_3()
        args = SConsArguments.Arguments._Arguments(decls)
        self.assertEqual(args._rename_dict, [None, None, None])
        self.assertEqual(args._resubst_dict, [None, None, None])
        self.assertEqual(args._irename_dict, [None, None, None])
        self.assertEqual(args._iresubst_dict, [None, None, None])
        self._mock_decls_supp_dicts_2(decls)
        args._Arguments__init_supp_dicts(decls)
        self.assertEqual(args._rename_dict, ['rename_dict[0]', 'rename_dict[1]', 'rename_dict[2]'])
        self.assertEqual(args._resubst_dict, ['resubst_dict[0]', 'resubst_dict[1]', 'resubst_dict[2]'])
        self.assertEqual(args._irename_dict, ['irename_dict[0]', 'irename_dict[1]', 'irename_dict[2]'])
        self.assertEqual(args._iresubst_dict, ['iresubst_dict[0]', 'iresubst_dict[1]', 'iresubst_dict[2]'])

    def XxxEnvProxy_test(self, x):
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        env = { 'env_a' : 'A', 'env_b' : 'B'}
        with mock.patch('SConsArguments.Arguments._ArgumentsProxy', return_value = 'ok') as ProxyClass:
            if x == 'var_':
                proxy = args.VarEnvProxy(env)
            elif x == 'opt_':
                proxy = args.OptEnvProxy(env)
            else:
                proxy = args.EnvProxy(env)

            try:
                ProxyClass.assert_called_once_with(env, { '%sa' % x : 'env_a' }, {'%sa' % x : '${env_a}'}, {'env_a' : '%sa' % x}, {'env_a' : '${%sa}' % x})
            except AssertionError as e:
                self.fail(str(e))
            self.assertEqual(proxy, 'ok')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_VarEnvProxy(self):
        """_Arguments(decls).VarEnvProxy(env) should _ArgumentsProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('var_')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_OptEnvProxy(self):
        """_Arguments(decls).OptEnvProxy(env) should _ArgumentsProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('opt_')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_EnvProxy(self):
        """_Arguments(decls).EnvProxy(env) should _ArgumentsProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_keys(self):
        """_Arguments(decls).get_keys() should return attribute __keys"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
        self.assertEqual(args.get_keys(), ['k','e','y','s'])
        # expect a copy of __keys, not __keys
        self.assertIsNot(args.get_keys(), args._Arguments__keys)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_key_ENV_x(self):
        """_Arguments(decls).get_key(ENV, 'x') should be raise KeyError"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_key(SConsArguments.Arguments.ENV, 'x')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_key_VAR_x(self):
        """_Arguments(decls).get_key(VAR, 'x') should be raise KeyError"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_key(SConsArguments.Arguments.VAR, 'x')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_key_OPT_x(self):
        """_Arguments(decls).get_key(OPT, 'x') should be raise KeyError"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_key(SConsArguments.Arguments.OPT, 'x')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_key_123_a(self):
        """_Arguments(decls).get_key(123, 'a') should be raise KeyError"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        with self.assertRaises(IndexError):
            args.get_key(123, 'a')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_key_ENV_a(self):
        """_Arguments(decls).get_key(ENV, 'a') should == 'env_a'"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_key(SConsArguments.Arguments.ENV, 'a'), 'env_a')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_key_VAR_a(self):
        """_Arguments(decls).get_key(VAR, 'a') should == 'var_a'"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_key(SConsArguments.Arguments.VAR, 'a'), 'var_a')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_key_OPT_a(self):
        """_Arguments(decls).get_key(OPT, 'a') should == 'opt_a'"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_key(SConsArguments.Arguments.OPT, 'a'), 'opt_a')

    def test_get_key_1(self):
        """_Arguments(decls).get_key(ns, 'foo') test 1"""
        decls = SConsArguments.DeclareArguments(
            foo = { 'env_key' : 'ENV_FOO', 'var_key' : 'VAR_FOO', 'opt_key' : 'OPT_FOO', 'option' : '--foo' },
            bar = { 'env_key' : 'ENV_BAR', 'var_key' : 'VAR_BAR', 'opt_key' : 'OPT_BAR', 'option' : '--bar' }
        )
        args = decls.Commit()
        self.assertEqual(args.get_key(SConsArguments.Arguments.ENV, 'foo'), 'ENV_FOO')
        self.assertEqual(args.get_key(SConsArguments.Arguments.VAR, 'foo'), 'VAR_FOO')
        self.assertEqual(args.get_key(SConsArguments.Arguments.OPT, 'foo'), 'OPT_FOO')
        self.assertEqual(args.get_key(SConsArguments.Arguments.ENV, 'bar'), 'ENV_BAR')
        self.assertEqual(args.get_key(SConsArguments.Arguments.VAR, 'bar'), 'VAR_BAR')
        self.assertEqual(args.get_key(SConsArguments.Arguments.OPT, 'bar'), 'OPT_BAR')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_env_key_x(self):
        """_Arguments(decls).get_env_key('x') should raise KeyError"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_env_key('x')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_env_key_a(self):
        """_Arguments(decls).get_env_key('a') should == 'env_a'"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_env_key('a'), 'env_a')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_var_key_x(self):
        """_Arguments(decls).get_var_key('x') should raise KeyError"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_var_key('x')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_var_key_a(self):
        """_Arguments(decls).get_var_key('a') should == 'var_a'"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_var_key('a'), 'var_a')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_opt_key_x(self):
        """_Arguments(decls).get_opt_key('x') should raise KeyError"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_opt_key('x')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_opt_key_a(self):
        """_Arguments(decls).get_opt_key('a') should == 'opt_a'"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_opt_key('a'), 'opt_a')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_update_env_from_vars_1(self):
        """_Arguments(decls).update_env_from_vars('env', variables)"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', return_value = 'proxy123')
        with mock.patch('SConsArguments.Arguments._VariablesWrapper') as WrapperClass:
            wrapper = WrapperClass.return_value
            wrapper.Update = mock.Mock(name = 'Update')
            args.update_env_from_vars('env', 'variables')
            try:
                WrapperClass.assert_called_once_with('variables')
                args.VarEnvProxy.assert_called_once_with('env')
                wrapper.Update.assert_called_once_with('proxy123',None)
            except AssertionError as e:
                self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_update_env_from_vars_2(self):
        """_Arguments(decls).update_env_from_vars('env', variables, 'arg')"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', return_value = 'proxy123')
        with mock.patch('SConsArguments.Arguments._VariablesWrapper') as WrapperClass:
            wrapper = WrapperClass.return_value
            wrapper.Update = mock.Mock(name = 'Update')
            args.update_env_from_vars('env', 'variables', 'args2')
            try:
                WrapperClass.assert_called_once_with('variables')
                args.VarEnvProxy.assert_called_once_with('env')
                wrapper.Update.assert_called_once_with('proxy123','args2')
            except AssertionError as e:
                self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_update_env_from_opts_1(self):
        """_Arguments(decls).update_env_from_opts('env')"""
        proxy = { 'env1' : {} }
        def OptEnvProxy(arg): return proxy[arg]
        args = SConsArguments.Arguments._Arguments(self._decls_mock_4())
        args.OptEnvProxy = mock.Mock(name = 'OptEnvProxy', side_effect = OptEnvProxy)
        with mock.patch('SCons.Script.Main.GetOption', side_effect = lambda key : 'val_%s' % key) as GetOption:
            args.update_env_from_opts('env1')
            try:
                GetOption.assert_called_once_with('opt_a')
            except AssertionError as e:
                self.fail(str(e))
            self.assertEqual(proxy['env1']['opt_a'], 'val_opt_a')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_UpdateEnvironment_1(self):
        """_Arguments(decls).UpdateEnvironment('env') never calls update_env_from_{vars,opts}"""
        args = self._arguments_mock_4_UpdateEnvironment()
        args.UpdateEnvironment('env')
        try:
            args.update_env_from_vars.assert_not_called()
            args.update_env_from_opts.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_UpdateEnvironment_2(self):
        """_Arguments(decls).UpdateEnvironment('env','variables1') calls update_env_from_vars('env', 'variables1') once"""
        args = self._arguments_mock_4_UpdateEnvironment()
        args.UpdateEnvironment('env', 'variables1')
        try:
            args.update_env_from_vars.assert_called_once_with('env', 'variables1', None)
            args.update_env_from_opts.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_UpdateEnvironment_3(self):
        """_Arguments(decls).UpdateEnvironment('env',None,True) calls update_env_from_opts('env') once"""
        args = self._arguments_mock_4_UpdateEnvironment()
        args.UpdateEnvironment('env', None, True)
        try:
            args.update_env_from_vars.assert_not_called()
            args.update_env_from_opts.assert_called_once_with('env')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_UpdateEnvironment_4(self):
        """_Arguments(decls).UpdateEnvironment('env','variables1',True) calls update_env_from_{opts,vars} once"""
        args = self._arguments_mock_4_UpdateEnvironment()
        args.UpdateEnvironment('env', 'variables1', True)
        try:
            args.update_env_from_vars.assert_called_once_with('env', 'variables1', None)
            args.update_env_from_opts.assert_called_once_with('env')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_SaveVariables(self):
        """_Arguments(decls).SaveVariables(variables, 'filename1', 'env1')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.Save = mock.Mock(name = 'Save')
        args.SaveVariables(variables, 'filename1', 'env1')
        try:
            variables.Save.assert_called_once_with('filename1','var_env1_proxy')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_GenerateVariablesHelpText_1(self):
        """_Arguments(decls).GenerateVariablesHelpText(variables, 'env1')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.GenerateHelpText = mock.Mock(name = 'GenerateHelpText')
        args.GenerateVariablesHelpText(variables, 'env1')
        try:
            variables.GenerateHelpText.assert_called_once_with('var_env1_proxy')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_GenerateVariablesHelpText_2(self):
        """_Arguments(decls).GenerateVariablesHelpText(variables, 'env1', 'arg1', 'arg2')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.GenerateHelpText = mock.Mock(name = 'GenerateHelpText')
        args.GenerateVariablesHelpText(variables, 'env1', 'arg1', 'arg2')
        try:
            variables.GenerateHelpText.assert_called_once_with('var_env1_proxy', 'arg1', 'arg2')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_HandleVariablesHelp_1(self):
        """_Arguments(decls).HandleVariablesHelp('var1', 'env1', 'arg1', 'arg2', foo = 'foo1')"""
        with mock.patch('sys.stdout') as mock_stdout, \
             mock.patch('SCons.Script.Main.AddOption') as mock_AddOption, \
             mock.patch('SCons.Script.Main.GetOption', return_value = True) as mock_GetOption:
            args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
            args.GenerateVariablesHelpText = mock.Mock(return_value = 'All the help')
            args.HandleVariablesHelp('var1', 'env1', 'arg1', 'arg2', foo='foo1')
            mock_AddOption.assert_called_once_with('--help-variables',dest='help_variables',action='store_true',help='print help for CLI variables')
            mock_GetOption.assert_called_once_with('help_variables')
            args.GenerateVariablesHelpText.assert_called_once_with('var1', 'env1', 'arg1', 'arg2', foo='foo1')
            mock_stdout.write.assert_called_once_with('All the help')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_HandleVariablesHelp_2(self):
        """_Arguments(decls).HandleVariablesHelp('var1', 'env1', option_name='--my-help', option_dest='my_help', option_help='Print My Help')"""
        with mock.patch('sys.stdout') as mock_stdout, \
             mock.patch('SCons.Script.Main.AddOption') as mock_AddOption, \
             mock.patch('SCons.Script.Main.GetOption', return_value = True) as mock_GetOption:
            args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
            args.GenerateVariablesHelpText = mock.Mock(return_value = 'All the help')
            result = args.HandleVariablesHelp('var1', 'env1', option_name='--my-help', option_dest='my_help', option_help='Print My Help')
            self.assertEqual(result, 'All the help')
            mock_AddOption.assert_called_once_with('--my-help',dest='my_help',action='store_true',help='Print My Help')
            mock_GetOption.assert_called_once_with('my_help')
            args.GenerateVariablesHelpText.assert_called_once_with('var1','env1')
            mock_stdout.write.assert_called_once_with('All the help')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_HandleVariablesHelp_3(self):
        """_Arguments(decls).HandleVariablesHelp('var1', 'env1', option_create=False)"""
        with mock.patch('sys.stdout') as mock_stdout, \
             mock.patch('SCons.Script.Main.AddOption') as mock_AddOption, \
             mock.patch('SCons.Script.Main.GetOption', return_value = True) as mock_GetOption:
            args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
            args.GenerateVariablesHelpText = mock.Mock(return_value = 'All the help')
            result = args.HandleVariablesHelp('var1', 'env1', option_create=False)
            self.assertEqual(result, 'All the help')
            mock_AddOption.assert_not_called()
            mock_GetOption.assert_called_once_with('help_variables')
            args.GenerateVariablesHelpText.assert_called_once_with('var1', 'env1')
            mock_stdout.write.assert_called_once_with('All the help')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_HandleVariablesHelp_4(self):
        """_Arguments(decls).HandleVariablesHelp('var1', 'env1', print_help=False)"""
        with mock.patch('sys.stdout') as mock_stdout, \
             mock.patch('SCons.Script.Main.AddOption') as mock_AddOption, \
             mock.patch('SCons.Script.Main.GetOption', return_value = True) as mock_GetOption:
            args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
            args.GenerateVariablesHelpText = mock.Mock(return_value = 'All the help')
            result = args.HandleVariablesHelp('var1', 'env1', print_help=False)
            self.assertEqual(result, 'All the help')
            mock_AddOption.assert_called_once_with('--help-variables',dest='help_variables',action='store_true',help='print help for CLI variables')
            mock_GetOption.assert_called_once_with('help_variables')
            args.GenerateVariablesHelpText.assert_called_once_with('var1', 'env1')
            mock_stdout.write.assert_not_called()

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_HandleVariablesHelp_5(self):
        """_Arguments(decls).HandleVariablesHelp('var1', 'env1')"""
        with mock.patch('sys.stdout') as mock_stdout, \
             mock.patch('SCons.Script.Main.AddOption') as mock_AddOption, \
             mock.patch('SCons.Script.Main.GetOption', return_value = False) as mock_GetOption:
            args = SConsArguments.Arguments._Arguments(self._decls_mock_1())
            args.GenerateVariablesHelpText = mock.Mock(return_value = 'All the help')
            result = args.HandleVariablesHelp('var1', 'env1')
            self.assertIs(result, None)
            mock_AddOption.assert_called_once_with('--help-variables',dest='help_variables',action='store_true',help='print help for CLI variables')
            mock_GetOption.assert_called_once_with('help_variables')
            args.GenerateVariablesHelpText.assert_not_called()
            mock_stdout.write.assert_not_called()



    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_GetCurrentValues_1(self):
        """_Arguments(decls).GetCurrentValues(env) works as expected"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_x' : 'X' }
        current = args.GetCurrentValues(env)
        self.assertIs(current['env_k'], env['env_k'])
        self.assertIs(current['env_e'], env['env_e'])
        self.assertEqual(current, {'env_k' : 'K', 'env_e' : 'E'})

    def test__is_unaltered_1(self):
        """<_Arguments>._is_unaltered({}, {}, 'a') should be True"""
        self.assertTrue(SConsArguments.Arguments._Arguments._is_unaltered({}, {}, 'a'))

    def test__is_unaltered_2(self):
        """<_Arguments>._is_unaltered({'a' : 'foo' }, {'a' : 'foo'}, 'a') should be True"""
        self.assertTrue(SConsArguments.Arguments._Arguments._is_unaltered({'a' : 'foo'}, { 'a' : 'foo' }, 'a'))

    def test__is_unaltered_3(self):
        """<_Arguments>._is_unaltered({'a' : 'foo'}, {}, 'a') should be False"""
        self.assertFalse(SConsArguments.Arguments._Arguments._is_unaltered({'a' : 'foo'}, {}, 'a'))

    def test__is_unaltered_4(self):
        """<_Arguments>._is_unaltered({}, {'a' : 'foo'}, 'a') should be False"""
        self.assertFalse(SConsArguments.Arguments._Arguments._is_unaltered({'a' : 'foo'}, {}, 'a'))

    def test__is_unaltered_5(self):
        """<_Arguments>._is_unaltered({'a' : 'foo' }, {'a' : 'bar'}, 'a') should be False"""
        self.assertFalse(SConsArguments.Arguments._Arguments._is_unaltered({'a' : 'foo'}, { 'a' : 'bar' }, 'a'))

    def test__is_unaltered_6(self):
        """<_Arguments>._is_unaltered({}, {'a' : None}, 'a') should be False"""
        self.assertFalse(SConsArguments.Arguments._Arguments._is_unaltered({}, { 'a' : None }, 'a'))

    def test__is_unaltered_7(self):
        """<_Arguments>._is_unaltered({'a' : None}, {}, 'a') should be False"""
        self.assertFalse(SConsArguments.Arguments._Arguments._is_unaltered({ 'a' : None }, {}, 'a'))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_GetAltered_1(self):
        """Test <_Arguments>.GetAltered()"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_s' : None, 'env_x' : 'X' }
        org = { 'env_k' : 'k', 'env_e' : 'E' }
        altered = args.GetAltered(env, org)
        self.assertEqual(altered, {'env_k' : 'K', 'env_s' : None})

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_OverwriteUnaltered_1(self):
        """Test <_Arguments>.OverwriteUnaltered()"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_s' : None, 'env_x' : 'X' }
        org = { 'env_k' : 'k', 'env_e' : 'E' }
        new = { 'k' : 'new K', 'e' : 'new E', 's' : 'new S', 'x' : 'new X'}
        chg = args.OverwriteUnaltered(env, org, new)
        self.assertEqual(env, { 'env_k' : 'K', 'env_e' : 'new E', 'env_s' : None, 'env_x' : 'X' })
        self.assertEqual(chg, { 'env_e' : 'new E' })

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_ReplaceUnaltered_1(self):
        """Test <_Arguments>.OverwriteUnaltered()"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K',      'env_e' : 'E',                      'env_x' : 'X'       }
        org = { 'env_k' : 'org K',  'env_e' : 'E',      'env_y' : 'y',                      }
        new = { 'k'     : 'new K',  'e'     : 'new E',                  'x'     : 'new X'   }
        ret = args.ReplaceUnaltered(env, org, new)
        self.assertEqual(ret, { 'env_k' : 'K', 'env_e' : 'new E'              })
        self.assertEqual(env, { 'env_k' : 'K', 'env_e' : 'E',   'env_x' : 'X' })

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_Postprocess_1(self):
        """Test <_Arguments>.Postorpcess()"""
        class _test_alt(object): pass
        _test_alt.update = mock.Mock(name = 'update')

        args = SConsArguments.Arguments._Arguments(self._decls_mock_5())
        args.GetCurrentValues = mock.Mock(name = 'GetCurrentValues', return_value  = 'org')
        args.UpdateEnvironment = mock.Mock(name = 'UpdateEnvironment')
        args.GetAltered = mock.Mock(name = 'GetAltered', return_value = _test_alt)
        args.SaveVariables = mock.Mock(name = 'SaveVariables')
        args.OverwriteUnaltered = mock.Mock(name = 'OverwriteUnaltered', return_value = 'chg')

        args.Postprocess('env', 'variables', 'options', 'ose', 'args', 'filename')

        args.GetCurrentValues.assert_called_once_with('env')
        args.UpdateEnvironment.assert_called_once_with('env', 'variables', 'options', 'args')
        args.GetAltered.assert_called_once_with('env', 'org')
        args.SaveVariables.assert_called_once_with('variables', 'filename', 'env')
        args.OverwriteUnaltered.assert_called_once_with('env', 'org', 'ose')
        _test_alt.update.assert_called_once_with('chg')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_Demangle_1(self):
        """Test <_Arguments>.Demangle()"""
        args = SConsArguments.Arguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_s' : None, 'env_x' : 'X' }
        res = args.Demangle(env)
        self.assertEqual(res, { 'k' : 'K', 'e' : 'E', 's' : None })

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test__Arguments ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
