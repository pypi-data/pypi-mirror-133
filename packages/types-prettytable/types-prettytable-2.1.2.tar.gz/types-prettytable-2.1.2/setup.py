from setuptools import setup

name = "types-prettytable"
description = "Typing stubs for prettytable"
long_description = '''
## Typing stubs for prettytable

This is a PEP 561 type stub package for the `prettytable` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `prettytable`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/prettytable. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="2.1.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['prettytable-stubs'],
      package_data={'prettytable-stubs': ['__init__.pyi', 'prettytable.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
