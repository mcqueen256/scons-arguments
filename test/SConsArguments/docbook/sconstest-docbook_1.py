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
Tests 'docbook' module
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
args = ImportArguments('docbook').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('DOCBOOK_DEFAULT_XSL_EPUB: $DOCBOOK_DEFAULT_XSL_EPUB'))
    print(env.subst('DOCBOOK_DEFAULT_XSL_HTML: $DOCBOOK_DEFAULT_XSL_HTML'))
    print(env.subst('DOCBOOK_DEFAULT_XSL_HTMLCHUNKED: $DOCBOOK_DEFAULT_XSL_HTMLCHUNKED'))
    print(env.subst('DOCBOOK_DEFAULT_XSL_HTMLHELP: $DOCBOOK_DEFAULT_XSL_HTMLHELP'))
    print(env.subst('DOCBOOK_DEFAULT_XSL_MAN: $DOCBOOK_DEFAULT_XSL_MAN'))
    print(env.subst('DOCBOOK_DEFAULT_XSL_PDF: $DOCBOOK_DEFAULT_XSL_PDF'))
    print(env.subst('DOCBOOK_DEFAULT_XSL_SLIDESHTML: $DOCBOOK_DEFAULT_XSL_SLIDESHTML'))
    print(env.subst('DOCBOOK_DEFAULT_XSL_SLIDESPDF: $DOCBOOK_DEFAULT_XSL_SLIDESPDF'))
    print(env.subst('DOCBOOK_FOP: $DOCBOOK_FOP'))
    print(env.subst('DOCBOOK_FOPFLAGS: $DOCBOOK_FOPFLAGS'))
    print(env.subst('DOCBOOK_XMLLINT: $DOCBOOK_XMLLINT'))
    print(env.subst('DOCBOOK_XMLLINTFLAGS: $DOCBOOK_XMLLINTFLAGS'))
    print(env.subst('DOCBOOK_XSLTPROC: $DOCBOOK_XSLTPROC'))
    print(env.subst('DOCBOOK_XSLTPROCFLAGS: $DOCBOOK_XSLTPROCFLAGS'))
    print(env.subst('DOCBOOK_XSLTPROCPARAMS: $DOCBOOK_XSLTPROCPARAMS'))
""")

test.run(['--help'])
lines = [
    'DOCBOOK_DEFAULT_XSL_EPUB: The default XSLT file for the DocbookEpub builder',
    'DOCBOOK_DEFAULT_XSL_HTML: The default XSLT file for the DocbookHtml builder',
    'DOCBOOK_DEFAULT_XSL_HTMLCHUNKED: The default XSLT file for the DocbookHtmlChunked builder',
    'DOCBOOK_DEFAULT_XSL_HTMLHELP: The default XSLT file for the DocbookHtmlhelp builder',
    'DOCBOOK_DEFAULT_XSL_MAN: The default XSLT file for the DocbookMan builder',
    'DOCBOOK_DEFAULT_XSL_PDF: The default XSLT file for the DocbookPdf builder',
    'DOCBOOK_DEFAULT_XSL_SLIDESHTML: The default XSLT file for the DocbookSlidesHtml builder',
    'DOCBOOK_DEFAULT_XSL_SLIDESPDF: The default XSLT file for the DocbookSlidesPdf builder',
    'DOCBOOK_FOP: The path to the PDF renderer fop or xep, if one of them is installed',
    'DOCBOOK_FOPFLAGS: Additonal command-line flags for the PDF renderer fop or xep',
    'DOCBOOK_XMLLINT: The path to the external executable xmllint',
    'DOCBOOK_XMLLINTFLAGS: Additonal command-line flags for the external executable xmllint',
    'DOCBOOK_XSLTPROC: The path to the external executable xsltproc (or saxon, xalan)',
    'DOCBOOK_XSLTPROCFLAGS: Additonal command-line flags for the external executable xsltproc (or saxon, xalan)',
    'DOCBOOK_XSLTPROCPARAMS: Additonal parameters that are not intended for the XSLT processor executable, but the XSL processing itself',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run(['DOCBOOK_DEFAULT_XSL_EPUB=somefile'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_DEFAULT_XSL_EPUB: somefile'])
test.run(['DOCBOOK_DEFAULT_XSL_HTML=somefile'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_DEFAULT_XSL_HTML: somefile'])
test.run(['DOCBOOK_DEFAULT_XSL_HTMLCHUNKED=somefile'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_DEFAULT_XSL_HTMLCHUNKED: somefile'])
test.run(['DOCBOOK_DEFAULT_XSL_HTMLHELP=somefile'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_DEFAULT_XSL_HTMLHELP: somefile'])
test.run(['DOCBOOK_DEFAULT_XSL_MAN=somefile'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_DEFAULT_XSL_MAN: somefile'])
test.run(['DOCBOOK_DEFAULT_XSL_PDF=somefile'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_DEFAULT_XSL_PDF: somefile'])
test.run(['DOCBOOK_DEFAULT_XSL_SLIDESHTML=somefile'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_DEFAULT_XSL_SLIDESHTML: somefile'])
test.run(['DOCBOOK_DEFAULT_XSL_SLIDESPDF=somefile'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_DEFAULT_XSL_SLIDESPDF: somefile'])
test.run(['DOCBOOK_FOP=myfop'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_FOP: myfop'])
test.run(['DOCBOOK_FOPFLAGS=one two'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_FOPFLAGS: one two'])
test.run(['DOCBOOK_XMLLINT=xmllint'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_XMLLINT: xmllint'])
test.run(['DOCBOOK_XMLLINTFLAGS=one two'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_XMLLINTFLAGS: one two'])
test.run(['DOCBOOK_XSLTPROC=xsltproc'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_XSLTPROC: xsltproc'])
test.run(['DOCBOOK_XSLTPROCFLAGS=one two'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_XSLTPROCFLAGS: one two'])
test.run(['DOCBOOK_XSLTPROCPARAMS=one two'])
test.must_contain_all_lines(test.stdout(), ['DOCBOOK_XSLTPROCPARAMS: one two'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
