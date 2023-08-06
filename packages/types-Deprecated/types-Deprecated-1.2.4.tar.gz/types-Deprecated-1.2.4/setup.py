from setuptools import setup

name = "types-Deprecated"
description = "Typing stubs for Deprecated"
long_description = '''
## Typing stubs for Deprecated

This is a PEP 561 type stub package for the `Deprecated` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Deprecated`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Deprecated. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="1.2.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['deprecated-stubs'],
      package_data={'deprecated-stubs': ['__init__.pyi', 'classic.pyi', 'sphinx.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
