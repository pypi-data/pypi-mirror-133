from setuptools import setup

name = "types-DateTimeRange"
description = "Typing stubs for DateTimeRange"
long_description = '''
## Typing stubs for DateTimeRange

This is a PEP 561 type stub package for the `DateTimeRange` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `DateTimeRange`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/DateTimeRange. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `505ea726415016e53638c8b584b8fdc9c722cac1`.
'''.lstrip()

setup(name=name,
      version="1.2.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-python-dateutil'],
      packages=['datetimerange-stubs'],
      package_data={'datetimerange-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
