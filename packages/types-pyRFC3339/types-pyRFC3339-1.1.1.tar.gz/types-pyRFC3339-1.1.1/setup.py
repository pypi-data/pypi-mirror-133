from setuptools import setup

name = "types-pyRFC3339"
description = "Typing stubs for pyRFC3339"
long_description = '''
## Typing stubs for pyRFC3339

This is a PEP 561 type stub package for the `pyRFC3339` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pyRFC3339`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pyRFC3339. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="1.1.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['pyrfc3339-stubs'],
      package_data={'pyrfc3339-stubs': ['__init__.pyi', 'generator.pyi', 'parser.pyi', 'utils.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
