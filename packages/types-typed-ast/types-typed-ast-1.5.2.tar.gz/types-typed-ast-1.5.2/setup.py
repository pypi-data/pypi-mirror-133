from setuptools import setup

name = "types-typed-ast"
description = "Typing stubs for typed-ast"
long_description = '''
## Typing stubs for typed-ast

This is a PEP 561 type stub package for the `typed-ast` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `typed-ast`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/typed-ast. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="1.5.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['typed_ast-stubs'],
      package_data={'typed_ast-stubs': ['__init__.pyi', 'ast27.pyi', 'ast3.pyi', 'conversions.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
