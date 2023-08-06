from setuptools import setup

name = "types-toml"
description = "Typing stubs for toml"
long_description = '''
## Typing stubs for toml

This is a PEP 561 type stub package for the `toml` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `toml`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/toml. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="0.10.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['toml-stubs'],
      package_data={'toml-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
