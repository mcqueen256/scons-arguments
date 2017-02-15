"""`SConsArguments.docbook`

Defines arguments related to Docbook tool 

**Arguments**

Programs:
    DOCBOOK_FOP
        The path to the PDF renderer fop or xep, if one of them is installed

    DOCBOOK_XMLLINT
        The path to the external executable xmllint

    DOCBOOK_XSLTPROC
        The path to the external executable xsltproc (or saxon, xalan)

Flags for programs:
    DOCBOOK_DEFAULT_XSL_EPUB
        The default XSLT file for the DocbookEpub builder

    DOCBOOK_DEFAULT_XSL_HTML
        The default XSLT file for the DocbookHtml builder

    DOCBOOK_DEFAULT_XSL_HTMLCHUNKED
        The default XSLT file for the DocbookHtmlChunked builder

    DOCBOOK_DEFAULT_XSL_HTMLHELP
        The default XSLT file for the DocbookHtmlhelp builder

    DOCBOOK_DEFAULT_XSL_MAN
        The default XSLT file for the DocbookMan builder

    DOCBOOK_DEFAULT_XSL_PDF
        The default XSLT file for the DocbookPdf builder

    DOCBOOK_DEFAULT_XSL_SLIDESHTML
        The default XSLT file for the DocbookSlidesHtml builder

    DOCBOOK_DEFAULT_XSL_SLIDESPDF
        The default XSLT file for the DocbookSlidesPdf builder

    DOCBOOK_FOPFLAGS
        Additonal command-line flags for the PDF renderer fop or xep

    DOCBOOK_XMLLINTFLAGS
        Additonal command-line flags for the external executable xmllint

    DOCBOOK_XSLTPROCFLAGS
        Additonal command-line flags for the external executable xsltproc (or saxon, xalan)

    DOCBOOK_XSLTPROCPARAMS
        Additonal parameters that are not intended for the XSLT processor executable, but the XSL processing itself
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

from SConsArguments.Util import flags2list
from SConsArguments.Importer import export_arguments

_all_arguments = {
  'DOCBOOK_DEFAULT_XSL_EPUB' : {
      'help'        : 'The default XSLT file for the DocbookEpub builder',
      'metavar'     : 'FILE',
  },
  'DOCBOOK_DEFAULT_XSL_HTML' : {
      'help'        : 'The default XSLT file for the DocbookHtml builder',
      'metavar'     : 'FILE',
  },
  'DOCBOOK_DEFAULT_XSL_HTMLCHUNKED' : {
      'help'        : 'The default XSLT file for the DocbookHtmlChunked builder',
      'metavar'     : 'FILE',
  },
  'DOCBOOK_DEFAULT_XSL_HTMLHELP' : {
      'help'        : 'The default XSLT file for the DocbookHtmlhelp builder',
      'metavar'     : 'FILE',
  },
  'DOCBOOK_DEFAULT_XSL_MAN' : {
      'help'        : 'The default XSLT file for the DocbookMan builder',
      'metavar'     : 'FILE',
  },
  'DOCBOOK_DEFAULT_XSL_PDF' : {
      'help'        : 'The default XSLT file for the DocbookPdf builder',
      'metavar'     : 'FILE',
  },
  'DOCBOOK_DEFAULT_XSL_SLIDESHTML' : {
      'help'        : 'The default XSLT file for the DocbookSlidesHtml builder',
      'metavar'     : 'FILE',
  },
  'DOCBOOK_DEFAULT_XSL_SLIDESPDF' : {
      'help'        : 'The default XSLT file for the DocbookSlidesPdf builder',
      'metavar'     : 'FILE',
  },
  'DOCBOOK_FOP' : {
      'help'        : 'The path to the PDF renderer fop or xep, if one of them is installed',
      'metavar'     : 'PROG'
  },
  'DOCBOOK_FOPFLAGS' : {
      'help'        : 'Additonal command-line flags for the PDF renderer fop or xep',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'DOCBOOK_XMLLINT' : {
      'help'        : 'The path to the external executable xmllint',
      'metavar'     : 'PROG'
  },
  'DOCBOOK_XMLLINTFLAGS' : {
      'help'        : 'Additonal command-line flags for the external executable xmllint',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'DOCBOOK_XSLTPROC' : {
      'help'        : 'The path to the external executable xsltproc (or saxon, xalan)',
      'metavar'     : 'PROG'
  },
  'DOCBOOK_XSLTPROCFLAGS' : {
      'help'        : 'Additonal command-line flags for the external executable xsltproc (or saxon, xalan)',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'DOCBOOK_XSLTPROCPARAMS' : {
      'help'        : 'Additonal parameters that are not intended for the XSLT processor executable, but the XSL processing itself',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'DOCBOOK_FOP', 'DOCBOOK_XMLLINT', 'DOCBOOK_XSLTPROC' ],
    'flags' : [ 'DOCBOOK_DEFAULT_XSL_EPUB', 'DOCBOOK_DEFAULT_XSL_HTML',
                'DOCBOOK_DEFAULT_XSL_HTMLCHUNKED',
                'DOCBOOK_DEFAULT_XSL_HTMLHELP', 'DOCBOOK_DEFAULT_XSL_MAN',
                'DOCBOOK_DEFAULT_XSL_PDF', 'DOCBOOK_DEFAULT_XSL_SLIDESHTML',
                'DOCBOOK_DEFAULT_XSL_SLIDESPDF', 'DOCBOOK_FOPFLAGS',
                'DOCBOOK_XMLLINTFLAGS', 'DOCBOOK_XSLTPROCFLAGS',
                'DOCBOOK_XSLTPROCPARAMS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'docbook' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            docbook_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            docbook_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('docbook', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
