from setuptools import setup

name = "types-Send2Trash"
description = "Typing stubs for Send2Trash"
long_description = '''
## Typing stubs for Send2Trash

This is a PEP 561 type stub package for the `Send2Trash` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Send2Trash`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Send2Trash. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="1.8.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['send2trash-stubs'],
      package_data={'send2trash-stubs': ['__init__.pyi', 'compat.pyi', 'exceptions.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
