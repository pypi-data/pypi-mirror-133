from setuptools import setup

name = "types-beautifulsoup4"
description = "Typing stubs for beautifulsoup4"
long_description = '''
## Typing stubs for beautifulsoup4

This is a PEP 561 type stub package for the `beautifulsoup4` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `beautifulsoup4`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/beautifulsoup4. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a40d79a4e63c4e750a8d3a8012305da942251eb4`.
'''.lstrip()

setup(name=name,
      version="4.10.10",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['bs4-stubs'],
      package_data={'bs4-stubs': ['__init__.pyi', 'builder/__init__.pyi', 'builder/_html5lib.pyi', 'builder/_htmlparser.pyi', 'builder/_lxml.pyi', 'dammit.pyi', 'diagnose.pyi', 'element.pyi', 'formatter.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
