scons-arguments
===============

| travis-ci | appveyor  | coveralls |
|-----------|-----------|-----------|
|[![Build Status](https://travis-ci.org/ptomulik/scons-arguments.png?branch=master)](https://travis-ci.org/ptomulik/scons-arguments)| [![Build status](https://ci.appveyor.com/api/projects/status/0fvtobp37lh1le0y/branch/master?svg=true)](https://ci.appveyor.com/project/ptomulik/scons-arguments/branch/master) | [![Coverage Status](https://coveralls.io/repos/ptomulik/scons-arguments/badge.svg?branch=master&service=github)](https://coveralls.io/github/ptomulik/scons-arguments?branch=master) |

Welcome to ``scons-arguments``.

This scons extension enables one to easily define scons command-line variables
and options. It provides a concept of *Argument* which correlates three
entities:

- command line option (e.g. ``scons --prefix=/usr/bin`` in command line),
- command line variable (e.g. ``scons PREFIX=/usr/bin`` in command line),
- scons construction variable (e.g. ``env['PREFIX']`` inside of a scons script).

*Arguments* allow to easily define how data should flow from scons command
line and operating system's environment to a scons environment (to scons
construction variables).

The extension also provides a number of modules with predefined command-line
arguments for core SCons tools (``cc``, ``c++``, ``link``, etc.).

INSTALLATION
------------

There are two method for installation:

### Installation by simple copy

Copy recursively ``SConsArguments/`` to your ``site_scons/`` directory

    cp -r scons-arguments/SConsArguments your/projects/site_scons/

### Installation as a submodule in git-based projects

Add the repository as a submodule to your project

```shell
git submodule add git://github.com/ptomulik/scons-arguments.git 3rd/scons-arguments
```

In your `site_scons/site_init.py` add the following lines:

```python
# site_scons/site_init.py
import sys
sys.path.append(Dir('#3rd/scons-arguments').abspath)
```

QUICK EXAMPLE
-------------

A simple C++ project, with a SConstruct file accepting most of the C/C++
compiler- and linker-related command-line arguments.

SConstruct file:

```python
# SConstruct
from SConsArguments import ImportArguments

env = Environment()
var = Variables()

dcl = ImportArguments(['c++', 'cc', 'link'])
arg = dcl.Commit(env, var, True)
arg.Postprocess(env, var, True)
if arg.HandleVariablesHelp(var, env):
  Exit(0)

env.Program('hello.cpp')
```

and the C++ source code (file ``hello.cpp``):

```c++
#include <iostream>

int main()
{
  std::cout << "Hello world" << std::endl;
  return 0;
}
```

Just try to run ``scons``, then ``scons --help``. Use ``scons --help-variables``
to see the full list of new command-line variables. Play with compiler/linker
options, for example run ``scons CCFLAGS='-g -O2'``.

DOCUMENTATION
-------------

### User documentation

Online User Manual may be found at:

  * <http://ptomulik.github.io/scons-arguments/user/manual.html>

User documentation can be generated from the top level directory with the
following command (see also requirements below)

```shell
scons user-doc
```
The generated documentation is located in ``build/doc/user``.

### API documentation

Online API documentation may be found at:

  * <http://ptomulik.github.io/scons-arguments/api/>

API documentation can be generated from the top level directory with the
following command (see also requirements below)

```shell
scons api-doc
```

The generated documentation will be written to ``build/doc/api``.

#### Requirements for user-doc

To generate user's documentation, you'll need following packages on your
system:

  * docbook5-xml <http://www.oasis-open.org/docbook/xml/>
  * xsltproc <ftp://xmlsoft.org/libxslt/>
  * imagemagick <http://www.imagemagick.org/>

You also must install locally the SCons docbook tool by Dirk Baechle:

  * scons docbook tool <https://bitbucket.org/dirkbaechle/scons_docbook/>

this is easily done by running the following bash script

```
python bin/downloads.py scons-docbook
```

or simply (to download all dependencies)

```
python bin/downloads.py
```

from the top level directory.

#### Requirements for api-doc

To generate API documentation, you may need following packages on your system:

  * python-epydoc <http://epydoc.sourceforge.net/>
  * python-docutils <http://pypi.python.org/pypi/docutils>
  * python-pygments <http://pygments.org/>

Note, that epydoc is no longer developed, last activities in the project are
dated to 2008. The pip epydoc package 3.0.1 is not usable with current versions
of python. Fortunately Debian package is patched to work with current python.
Please use the ``python-epydoc`` package installed with apt-get.

```shell
apt-get install python-epydoc python-docutils python-pygments
```

TESTING
-------

We provide unit tests and end-to-end tests.

### Running unit tests

To run unit tests type

```shell
scons unit-test
```

### Requirements for unit tests

  * python-unittest2 <https://pypi.python.org/pypi/unittest2>
  * python-mock <https://pypi.python.org/pypi/mock>

On Debian install them with:

```shell
apt-get install python-unittest2 python-mock
```

### Running end-to-end tests

To run end-to-end tests, type

```shell
scons test
```

End-to-end tests are stored under ``test/`` directory. To run particular test
type (on Linux):

```shell
SCONS_EXTERNAL_TEST=1 python runtest.py test/SConsArguments/ArgumentDeclaration/sconstest-argumentdeclaration_1.py
```


### Requirements for end-to-end tests

  * SCons testing framework

Download the SCons testing framework with:

```shell
python ./bin/downloads.py scons-test
```

or

```shell
python ./bin/downloads.py
```

LICENSE
-------

Copyright (c) 2015-2017 by Pawel Tomulik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
