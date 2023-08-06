from setuptools import setup

name = "types-characteristic"
description = "Typing stubs for characteristic"
long_description = '''
## Typing stubs for characteristic

This is a PEP 561 type stub package for the `characteristic` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `characteristic`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/characteristic. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a40d79a4e63c4e750a8d3a8012305da942251eb4`.
'''.lstrip()

setup(name=name,
      version="14.3.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['characteristic-stubs'],
      package_data={'characteristic-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
