""" `SConsArgumentsT.texTests`

Unit tests for `SConsArguments.tex`
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

import SConsArguments.tex as tex
import unittest
from . import TestCase

#############################################################################
class Test_tex(TestCase):
    """Test SConsArguments.tex"""
    def test_arguments1(self):
        "Test SConsArguments.tex.arguments()"
        decl = tex.arguments()

        self.assertEqual(decl['BIBTEX']['help'], 'The bibliography generator for TeX and LaTeX')
        self.assertEqual(decl['BIBTEX']['metavar'], 'PROG')

        self.assertEqual(decl['BIBTEXFLAGS']['help'], 'General options passed to BibTeX')
        self.assertEqual(decl['BIBTEXFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['BIBTEXFLAGS']['converter'], tex.flags2list)

        self.assertEqual(decl['LATEX']['help'], 'The LaTeX structured formatter and typesetter')
        self.assertEqual(decl['LATEX']['metavar'], 'PROG')

        self.assertEqual(decl['LATEXFLAGS']['help'], 'General options passed to the LaTeX structured formatter and typesetter')
        self.assertEqual(decl['LATEXFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['LATEXFLAGS']['converter'], tex.flags2list)

        self.assertEqual(decl['LATEXRETRIES']['help'], 'The maximum number of times that LaTeX will be re-run')
        self.assertEqual(decl['LATEXRETRIES']['metavar'], 'NUM')
        self.assertEqual(decl['LATEXRETRIES']['converter'], int)

        self.assertEqual(decl['MAKEINDEX']['help'], 'The makeindex generator for the TeX')
        self.assertEqual(decl['MAKEINDEX']['metavar'], 'PROG')

        self.assertEqual(decl['MAKEINDEXFLAGS']['help'], 'General options passed to the makeindex')
        self.assertEqual(decl['MAKEINDEXFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['MAKEINDEXFLAGS']['converter'], tex.flags2list)

        self.assertEqual(decl['PDFLATEX']['help'], 'The pdflatex utility')
        self.assertEqual(decl['PDFLATEX']['metavar'], 'PROG')

        self.assertEqual(decl['PDFLATEXFLAGS']['help'], 'General options passed to the pdflatex utility')
        self.assertEqual(decl['PDFLATEXFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['PDFLATEXFLAGS']['converter'], tex.flags2list)

        self.assertEqual(decl['PDFTEX']['help'], 'The pdftex utility')
        self.assertEqual(decl['PDFTEX']['metavar'], 'PROG')

        self.assertEqual(decl['PDFTEXFLAGS']['help'], 'General options passed to the pdftex utility')
        self.assertEqual(decl['PDFTEXFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['PDFTEXFLAGS']['converter'], tex.flags2list)

        self.assertEqual(decl['TEX']['help'], 'The TeX formatter and typesetter')
        self.assertEqual(decl['TEX']['metavar'], 'PROG')

        self.assertEqual(decl['TEXFLAGS']['help'], 'General options passed to the TeX formatter and typesetter')
        self.assertEqual(decl['TEXFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['TEXFLAGS']['converter'], tex.flags2list)

        self.assertEqual(decl['TEXINPUTS']['help'], 'List of directories that the LaTeX program will search for include directories')
        self.assertEqual(decl['TEXINPUTS']['metavar'], 'PATHS')
        self.assertEqual(decl['TEXINPUTS']['converter'], tex.paths2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.tex.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'tex_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'tex_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = tex.arguments(**kw)
            self.assertAllMissing(decl, [ 'BIBTEX', 'LATEX', 'MAKEINDEX', 'PDFLATEX', 'PDFTEX', 'TEX' ])
            self.assertAllPresent(decl, [ 'BIBTEXFLAGS', 'LATEXFLAGS', 'LATEXRETRIES', 'MAKEINDEXFLAGS', 'PDFLATEXFLAGS', 'PDFTEXFLAGS', 'TEXFLAGS', 'TEXINPUTS' ])

    def test_arguments__groups_2(self):
        "Test SConsArguments.tex.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'tex_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'tex_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = tex.arguments(**kw)
            self.assertAllPresent(decl, [ 'BIBTEX', 'LATEX', 'MAKEINDEX', 'PDFLATEX', 'PDFTEX', 'TEX' ])
            self.assertAllMissing(decl, [ 'BIBTEXFLAGS', 'LATEXFLAGS', 'LATEXRETRIES', 'MAKEINDEXFLAGS', 'PDFLATEXFLAGS', 'PDFTEXFLAGS', 'TEXFLAGS', 'TEXINPUTS' ])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_tex ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
