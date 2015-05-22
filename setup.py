#!/usr/bin/env python
import typedattr
from distutils.core import setup

setup(name='typedattr',
    version=typedattr.__version__,
    description=typedattr.__description__,
    author=typedattr.__author__,
    author_email=typedattr.__author_email__,
    url=typedattr.__url__,
    packages=['typedattr', 'typedattr.view', 'typedattr.concurrent'])
