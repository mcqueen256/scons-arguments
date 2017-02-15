"""`SConsArguments.tex`

Defines arguments related to tex

**Arguments**

Programs:
    BIBTEX
        The bibliography generator for TeX and LaTeX

    LATEX
        The LaTeX structured formatter and typesetter

    MAKEINDEX
        The makeindex generator for the TeX

    PDFLATEX
        The pdflatex utility

    PDFTEX
        The pdftex utility

    TEX
        The TeX formatter and typesetter

Flags for programs:
    BIBTEXFLAGS
        General options passed to BibTeX

    LATEXFLAGS
        General options passed to the LaTeX structured formatter and typesetter

    LATEXRETRIES
        The maximum number of times that LaTeX will be re-run

    MAKEINDEXFLAGS
        General options passed to the makeindex

    PDFLATEXFLAGS
        General options passed to the pdflatex utility

    PDFTEXFLAGS
        General options passed to the pdftex utility

    TEXFLAGS
        General options passed to the TeX formatter and typesetter

    TEXINPUTS
        List of directories that the LaTeX program will search for include directories
"""

#
# Copyright (c) 2017 by Pawel Tomulik
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

from SConsArguments.Util import flags2list, paths2list
from SConsArguments.Importer import export_arguments

_all_arguments = {
    'BIBTEX' : {
        'help' : 'The bibliography generator for TeX and LaTeX',
        'metavar' : 'PROG',
    },
    'BIBTEXFLAGS' : {
        'help' : 'General options passed to BibTeX',
        'metavar' : 'FLAGS',
        'converter' : flags2list
    },
    'LATEX' : {
        'help' : 'The LaTeX structured formatter and typesetter',
        'metavar' : 'PROG',
    },
    'LATEXFLAGS' : {
        'help' : 'General options passed to the LaTeX structured formatter and typesetter',
        'metavar' : 'FLAGS',
        'converter' : flags2list
    },
    'LATEXRETRIES' : {
        'help' : 'The maximum number of times that LaTeX will be re-run',
        'metavar' : 'NUM',
        'converter' : int
    },
    'MAKEINDEX' : {
        'help' : 'The makeindex generator for the TeX',
        'metavar' : 'PROG',
    },
    'MAKEINDEXFLAGS' : {
        'help' : 'General options passed to the makeindex',
        'metavar' : 'FLAGS',
        'converter' : flags2list
    },
    'PDFLATEX' : {
        'help' : 'The pdflatex utility',
        'metavar' : 'PROG',
    },
    'PDFLATEXFLAGS' : {
        'help' : 'General options passed to the pdflatex utility',
        'metavar' : 'FLAGS',
        'converter' : flags2list
    },
    'PDFTEX' : {
        'help' : 'The pdftex utility',
        'metavar' : 'PROG',
    },
    'PDFTEXFLAGS' : {
        'help' : 'General options passed to the pdftex utility',
        'metavar' : 'FLAGS',
        'converter' : flags2list
    },
    'TEX' : {
        'help' : 'The TeX formatter and typesetter',
        'metavar' : 'PROG',
    },
    'TEXFLAGS' : {
        'help' : 'General options passed to the TeX formatter and typesetter',
        'metavar' : 'FLAGS',
        'converter' : flags2list
    },
    'TEXINPUTS' : {
        'help' : 'List of directories that the LaTeX program will search for include directories',
        'metavar' : 'PATHS',
        'converter' : paths2list
    },
}

_groups = {
    'progs' : [ 'BIBTEX', 'LATEX', 'MAKEINDEX', 'PDFLATEX', 'PDFTEX', 'TEX' ],
    'flags' : [ 'BIBTEXFLAGS', 'LATEXFLAGS', 'LATEXRETRIES', 'MAKEINDEXFLAGS',
                'PDFLATEXFLAGS', 'PDFTEXFLAGS', 'TEXFLAGS', 'TEXINPUTS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'tex' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            tex_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            tex_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('tex', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
