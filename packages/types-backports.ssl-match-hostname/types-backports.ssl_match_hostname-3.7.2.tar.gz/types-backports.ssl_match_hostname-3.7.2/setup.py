from setuptools import setup

name = "types-backports.ssl_match_hostname"
description = "Typing stubs for backports.ssl_match_hostname"
long_description = '''
## Typing stubs for backports.ssl_match_hostname

This is a PEP 561 type stub package for the `backports.ssl_match_hostname` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `backports.ssl_match_hostname`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/backports.ssl_match_hostname. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="3.7.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['backports-stubs'],
      package_data={'backports-stubs': ['__init__.pyi', 'ssl_match_hostname/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
