""" `SConsArgumentsT.docbookTests`

Unit tests for `SConsArguments.docbook`
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

import SConsArguments.docbook as docbook
import unittest
from . import TestCase

#############################################################################
class Test_docbook(TestCase):
    """Test SConsArguments.c++"""
    def test_arguments1(self):
        "Test SConsArguments.c++.arguments()"
        decl = docbook.arguments()

        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_EPUB']['help'], 'The default XSLT file for the DocbookEpub builder')
        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_EPUB']['metavar'], 'FILE')

        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_HTML']['help'], 'The default XSLT file for the DocbookHtml builder')
        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_HTML']['metavar'], 'FILE')

        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_HTMLCHUNKED']['help'], 'The default XSLT file for the DocbookHtmlChunked builder')
        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_HTMLCHUNKED']['metavar'], 'FILE')

        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_HTMLHELP']['help'], 'The default XSLT file for the DocbookHtmlhelp builder')
        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_HTMLHELP']['metavar'], 'FILE')

        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_MAN']['help'], 'The default XSLT file for the DocbookMan builder')
        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_MAN']['metavar'], 'FILE')

        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_PDF']['help'], 'The default XSLT file for the DocbookPdf builder')
        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_PDF']['metavar'], 'FILE')

        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_SLIDESHTML']['help'], 'The default XSLT file for the DocbookSlidesHtml builder')
        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_SLIDESHTML']['metavar'], 'FILE')

        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_SLIDESPDF']['help'], 'The default XSLT file for the DocbookSlidesPdf builder')
        self.assertEqual(decl['DOCBOOK_DEFAULT_XSL_SLIDESPDF']['metavar'], 'FILE')

        self.assertEqual(decl['DOCBOOK_FOP']['help'], 'The path to the PDF renderer fop or xep, if one of them is installed')
        self.assertEqual(decl['DOCBOOK_FOP']['metavar'], 'PROG')

        self.assertEqual(decl['DOCBOOK_FOPFLAGS']['help'], 'Additonal command-line flags for the PDF renderer fop or xep')
        self.assertEqual(decl['DOCBOOK_FOPFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['DOCBOOK_FOPFLAGS']['converter'], docbook.flags2list)

        self.assertEqual(decl['DOCBOOK_XMLLINT']['help'], 'The path to the external executable xmllint')
        self.assertEqual(decl['DOCBOOK_XMLLINT']['metavar'], 'PROG')

        self.assertEqual(decl['DOCBOOK_XMLLINTFLAGS']['help'], 'Additonal command-line flags for the external executable xmllint')
        self.assertEqual(decl['DOCBOOK_XMLLINTFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['DOCBOOK_XMLLINTFLAGS']['converter'], docbook.flags2list)

        self.assertEqual(decl['DOCBOOK_XSLTPROC']['help'], 'The path to the external executable xsltproc (or saxon, xalan)')
        self.assertEqual(decl['DOCBOOK_XSLTPROC']['metavar'], 'PROG')

        self.assertEqual(decl['DOCBOOK_XSLTPROCFLAGS']['help'], 'Additonal command-line flags for the external executable xsltproc (or saxon, xalan)')
        self.assertEqual(decl['DOCBOOK_XSLTPROCFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['DOCBOOK_XSLTPROCFLAGS']['converter'], docbook.flags2list)

        self.assertEqual(decl['DOCBOOK_XSLTPROCPARAMS']['help'], 'Additonal parameters that are not intended for the XSLT processor executable, but the XSL processing itself')
        self.assertEqual(decl['DOCBOOK_XSLTPROCPARAMS']['metavar'], 'FLAGS')
        self.assertEqual(decl['DOCBOOK_XSLTPROCPARAMS']['converter'], docbook.flags2list)


    def test_arguments__groups_1(self):
        "Test SConsArguments.docbook.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'docbook_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'docbook_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = docbook.arguments(**kw)
            self.assertAllMissing(decl, [ 'DOCBOOK_FOP', 'DOCBOOK_XMLLINT', 'DOCBOOK_XSLTPROC' ])
            self.assertAllPresent(decl, [ 'DOCBOOK_DEFAULT_XSL_EPUB', 'DOCBOOK_DEFAULT_XSL_HTML',
                                          'DOCBOOK_DEFAULT_XSL_HTMLCHUNKED',
                                          'DOCBOOK_DEFAULT_XSL_HTMLHELP', 'DOCBOOK_DEFAULT_XSL_MAN',
                                          'DOCBOOK_DEFAULT_XSL_PDF', 'DOCBOOK_DEFAULT_XSL_SLIDESHTML',
                                          'DOCBOOK_DEFAULT_XSL_SLIDESPDF', 'DOCBOOK_FOPFLAGS',
                                          'DOCBOOK_XMLLINTFLAGS', 'DOCBOOK_XSLTPROCFLAGS',
                                          'DOCBOOK_XSLTPROCPARAMS' ])

    def test_arguments__groups_2(self):
        "Test SConsArguments.docbook.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'docbook_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'docbook_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = docbook.arguments(**kw)
            self.assertAllPresent(decl, [ 'DOCBOOK_FOP', 'DOCBOOK_XMLLINT', 'DOCBOOK_XSLTPROC' ])
            self.assertAllMissing(decl, [ 'DOCBOOK_DEFAULT_XSL_EPUB', 'DOCBOOK_DEFAULT_XSL_HTML',
                                          'DOCBOOK_DEFAULT_XSL_HTMLCHUNKED',
                                          'DOCBOOK_DEFAULT_XSL_HTMLHELP', 'DOCBOOK_DEFAULT_XSL_MAN',
                                          'DOCBOOK_DEFAULT_XSL_PDF', 'DOCBOOK_DEFAULT_XSL_SLIDESHTML',
                                          'DOCBOOK_DEFAULT_XSL_SLIDESPDF', 'DOCBOOK_FOPFLAGS',
                                          'DOCBOOK_XMLLINTFLAGS', 'DOCBOOK_XSLTPROCFLAGS',
                                          'DOCBOOK_XSLTPROCPARAMS' ])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_docbook ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
