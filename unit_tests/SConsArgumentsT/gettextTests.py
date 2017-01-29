""" `SConsArgumentsT.gettextTests`

Unit tests for `SConsArguments.gettext`
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

import SConsArguments.gettext as gettext
import unittest
from . import TestCase

#############################################################################
class Test_gettext(TestCase):
    """Test SConsArguments.gettext"""
    def test_arguments1(self):
        "Test SConsArguments.gettext.arguments()"
        decl = gettext.arguments()
        self.assertEqual(decl['MSGFMT']['help'], 'The msgfmt executable')
        self.assertEqual(decl['MSGFMT']['metavar'], 'PROG')

        self.assertEqual(decl['MSGFMTFLAGS']['help'], 'General user options passed to msgfmt')
        self.assertEqual(decl['MSGFMTFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['MSGFMTFLAGS']['converter'], gettext.flags2list)

        decl = gettext.arguments()
        self.assertEqual(decl['MSGINIT']['help'], 'The msginit executable')
        self.assertEqual(decl['MSGINIT']['metavar'], 'PROG')

        self.assertEqual(decl['MSGINITFLAGS']['help'], 'General user options passed to msginit')
        self.assertEqual(decl['MSGINITFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['MSGINITFLAGS']['converter'], gettext.flags2list)

        decl = gettext.arguments()
        self.assertEqual(decl['MSGMERGE']['help'], 'The msgmerge executable')
        self.assertEqual(decl['MSGMERGE']['metavar'], 'PROG')

        self.assertEqual(decl['MSGMERGEFLAGS']['help'], 'General user options passed to msgmerge')
        self.assertEqual(decl['MSGMERGEFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['MSGMERGEFLAGS']['converter'], gettext.flags2list)

        decl = gettext.arguments()
        self.assertEqual(decl['XGETTEXT']['help'], 'The xgettext executable')
        self.assertEqual(decl['XGETTEXT']['metavar'], 'PROG')

        self.assertEqual(decl['XGETTEXTFLAGS']['help'], 'General user flags passed to xgettext.')
        self.assertEqual(decl['XGETTEXTFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['XGETTEXTFLAGS']['converter'], gettext.flags2list)

        self.assertEqual(decl['XGETTEXTPATH']['help'], 'List of directories, where xgettext will look for source files')
        self.assertEqual(decl['XGETTEXTPATH']['metavar'], 'PATHS')
        self.assertEqual(decl['XGETTEXTPATH']['converter'], gettext.paths2list)


    def test_arguments__groups_1(self):
        "Test SConsArguments.gettext.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'gettext_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'gettext_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = gettext.arguments(**kw)
            self.assertAllMissing(decl, ['MSGFMT', 'MSGINIT', 'MSGMERGE', 'XGETTEXT'])
            self.assertAllPresent(decl, ['MSGFMTFLAGS', 'MSGINITFLAGS', 'MSGMERGEFLAGS', 'XGETTEXTFLAGS', 'XGETTEXTPATH' ])

    def test_arguments__groups_2(self):
        "Test SConsArguments.gettext.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'gettext_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'gettext_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = gettext.arguments(**kw)
            self.assertAllPresent(decl, ['MSGFMT', 'MSGINIT', 'MSGMERGE', 'XGETTEXT'])
            self.assertAllMissing(decl, ['MSGFMTFLAGS', 'MSGINITFLAGS', 'MSGMERGEFLAGS', 'XGETTEXTFLAGS', 'XGETTEXTPATH' ])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_gettext ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
