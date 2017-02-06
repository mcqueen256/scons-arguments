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
Tests 'tex' module
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
args = ImportArguments('tex').Commit(env, var)
args.Postprocess(env, var)

if GetOption('help'):
    print(args.GenerateVariablesHelpText(var, env))
else:
    print(env.subst('BIBTEX: $BIBTEX'))
    print(env.subst('BIBTEXFLAGS: $BIBTEXFLAGS'))
    print(env.subst('LATEX: $LATEX'))
    print(env.subst('LATEXFLAGS: $LATEXFLAGS'))
    print(env.subst('LATEXRETRIES: $LATEXRETRIES'))
    print(env.subst('MAKEINDEX: $MAKEINDEX'))
    print(env.subst('MAKEINDEXFLAGS: $MAKEINDEXFLAGS'))
    print(env.subst('PDFLATEX: $PDFLATEX'))
    print(env.subst('PDFLATEXFLAGS: $PDFLATEXFLAGS'))
    print(env.subst('PDFTEX: $PDFTEX'))
    print(env.subst('PDFTEXFLAGS: $PDFTEXFLAGS'))
    print(env.subst('TEX: $TEX'))
    print(env.subst('TEXFLAGS: $TEXFLAGS'))
    print(env.subst('TEXINPUTS: $TEXINPUTS'))
""")

test.run(['--help'])
lines = [
    'BIBTEX: The bibliography generator for TeX and LaTeX',
    'BIBTEXFLAGS: General options passed to BibTeX',
    'LATEX: The LaTeX structured formatter and typesetter',
    'LATEXFLAGS: General options passed to the LaTeX structured formatter and typesetter',
    'LATEXRETRIES: The maximum number of times that LaTeX will be re-run',
    'MAKEINDEX: The makeindex generator for the TeX',
    'MAKEINDEXFLAGS: General options passed to the makeindex',
    'PDFLATEX: The pdflatex utility',
    'PDFLATEXFLAGS: General options passed to the pdflatex utility',
    'PDFTEX: The pdftex utility',
    'PDFTEXFLAGS: General options passed to the pdftex utility',
    'TEX: The TeX formatter and typesetter',
    'TEXFLAGS: General options passed to the TeX formatter and typesetter',
    'TEXINPUTS: List of directories that the LaTeX program will search for include directories',
]
test.must_contain_all_lines(test.stdout(), lines)

test.run('BIBTEX=myBIBTEX')
test.must_contain_all_lines(test.stdout(), ['BIBTEX: myBIBTEX'])
test.run(['BIBTEXFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['BIBTEXFLAGS: --flag1 --flag2'])

test.run('LATEX=myLATEX')
test.must_contain_all_lines(test.stdout(), ['LATEX: myLATEX'])
test.run(['LATEXFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['LATEXFLAGS: --flag1 --flag2'])
test.run(['LATEXRETRIES=12'])
test.must_contain_all_lines(test.stdout(), ['LATEXRETRIES: 12'])

test.run('MAKEINDEX=myMAKEINDEX')
test.must_contain_all_lines(test.stdout(), ['MAKEINDEX: myMAKEINDEX'])
test.run(['MAKEINDEXFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['MAKEINDEXFLAGS: --flag1 --flag2'])

test.run('PDFLATEX=myPDFLATEX')
test.must_contain_all_lines(test.stdout(), ['PDFLATEX: myPDFLATEX'])
test.run(['PDFLATEXFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['PDFLATEXFLAGS: --flag1 --flag2'])

test.run('PDFTEX=myPDFTEX')
test.must_contain_all_lines(test.stdout(), ['PDFTEX: myPDFTEX'])
test.run(['PDFTEXFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['PDFTEXFLAGS: --flag1 --flag2'])

test.run('TEX=myTEX')
test.must_contain_all_lines(test.stdout(), ['TEX: myTEX'])
test.run(['TEXFLAGS=--flag1 --flag2'])
test.must_contain_all_lines(test.stdout(), ['TEXFLAGS: --flag1 --flag2'])
test.run(['TEXINPUTS=first/path:second/path'])
test.must_contain_all_lines(test.stdout(), ['TEXINPUTS: first/path second/path'])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
