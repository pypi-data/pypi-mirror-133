from setuptools import setup

name = "types-tabulate"
description = "Typing stubs for tabulate"
long_description = '''
## Typing stubs for tabulate

This is a PEP 561 type stub package for the `tabulate` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `tabulate`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/tabulate. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="0.8.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['tabulate-stubs'],
      package_data={'tabulate-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
