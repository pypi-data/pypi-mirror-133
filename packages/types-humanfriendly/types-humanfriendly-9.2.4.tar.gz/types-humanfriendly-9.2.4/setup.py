from setuptools import setup

name = "types-humanfriendly"
description = "Typing stubs for humanfriendly"
long_description = '''
## Typing stubs for humanfriendly

This is a PEP 561 type stub package for the `humanfriendly` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `humanfriendly`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/humanfriendly. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="9.2.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['humanfriendly-stubs'],
      package_data={'humanfriendly-stubs': ['__init__.pyi', 'case.pyi', 'cli.pyi', 'compat.pyi', 'decorators.pyi', 'deprecation.pyi', 'prompts.pyi', 'sphinx.pyi', 'tables.pyi', 'terminal/__init__.pyi', 'terminal/html.pyi', 'terminal/spinners.pyi', 'testing.pyi', 'text.pyi', 'usage.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
