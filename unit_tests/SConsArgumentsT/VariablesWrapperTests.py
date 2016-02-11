""" SConsArguments.VariablesWrapperTests

Unit tests for SConsArguments.VariablesWrapper
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

import SConsArguments.VariablesWrapper
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
class Test__VariablesWrapper(unittest.TestCase):
    class _Option:
        def __init__(self, key, default = None, validator = None, converter = None, aliases = []):
            self.key = key
            self.default = default
            self.validator = validator
            self.converter = converter
            self.aliases = aliases

    class _Variables:
        def __init__(self, files=[], args={}, is_global=1):
            self.files = files
            self.args = args
            self.is_global = is_global
            self.unknown = dict()

    def test___init___1(self):
        """_VariablesWrapper.__init__(variables) should initialize variables"""
        class _test_variables: pass
        wrap = SConsArguments._VariablesWrapper(_test_variables)
        self.assertIs(wrap.variables, _test_variables)

    def test___getattr___1(self):
        """_VariablesWrapper.foo should return _VariablesWrapper.variables.foo"""
        class _test_variables:
            foo = 10
        wrap = SConsArguments._VariablesWrapper(_test_variables)
        self.assertIs(wrap.foo, _test_variables.foo)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_Update_1(self):
        """Test <_VaraiblesWrapper>.Update()"""
        _Variables = Test__VariablesWrapper._Variables
        _Option = Test__VariablesWrapper._Option
        validate_d = mock.Mock(name = 'validate_d')
        variables = _Variables( files = ['existing/file', 'inexistent/file'])
        variables.options = [
            _Option('a', SConsArguments._undef),
            _Option('b'),
            _Option('c', 'C def'),
            _Option('d', validator = validate_d),
            _Option('e', 'E def', converter = lambda x : x + ' converted'),
            _Option('f', 'F def'),
            _Option('g', 'G def', aliases = ['g_alias']),
            _Option('h', 'H def', aliases = ['h_alias'])
        ]
        args = { 'd' : 'D', 'e' : 'E', 'g_alias' : 'G' , 'z' : 'Z'}
        env = dict()
        fd = mock.Mock(name = 'fd')
        fd.read = mock.Mock(name = 'read', return_value = "b='B file'\nf=None\nh_alias='H file'")
        wrapper = SConsArguments._VariablesWrapper(variables)
        with mock.patch('__builtin__.open', spec=open, return_value = fd) as _open, \
             mock.patch('os.path.exists', side_effect = lambda f : f == 'existing/file') as _os_path_exists:
            wrapper.Update(env, args)
        _os_path_exists.assert_has_calls([mock.call('existing/file'), mock.call('inexistent/file')])
        _open.assert_called_once_with('existing/file','rU')
        validate_d.assert_called_once_with('d', 'D', env)
        self.assertEqual(env, {'c' : 'C def', 'b' : 'B file', 'd' :'D', 'e' : 'E converted', 'f' : None, 'g' : 'G', 'h' : 'H def'})
        self.assertEqual(variables.unknown, {'z' : 'Z'})

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test__VariablesWrapper ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
