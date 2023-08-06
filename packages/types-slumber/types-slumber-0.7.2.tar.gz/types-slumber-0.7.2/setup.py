from setuptools import setup

name = "types-slumber"
description = "Typing stubs for slumber"
long_description = '''
## Typing stubs for slumber

This is a PEP 561 type stub package for the `slumber` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `slumber`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/slumber. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="0.7.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['slumber-stubs'],
      package_data={'slumber-stubs': ['__init__.pyi', 'exceptions.pyi', 'serialize.pyi', 'utils.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
