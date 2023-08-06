from setuptools import setup

name = "types-retry"
description = "Typing stubs for retry"
long_description = '''
## Typing stubs for retry

This is a PEP 561 type stub package for the `retry` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `retry`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/retry. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a40d79a4e63c4e750a8d3a8012305da942251eb4`.
'''.lstrip()

setup(name=name,
      version="0.9.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['retry-stubs'],
      package_data={'retry-stubs': ['__init__.pyi', 'api.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
