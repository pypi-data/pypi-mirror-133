from setuptools import setup

name = "types-pyvmomi"
description = "Typing stubs for pyvmomi"
long_description = '''
## Typing stubs for pyvmomi

This is a PEP 561 type stub package for the `pyvmomi` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pyvmomi`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pyvmomi. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="7.0.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-enum34'],
      packages=['pyVmomi-stubs'],
      package_data={'pyVmomi-stubs': ['__init__.pyi', 'vim/__init__.pyi', 'vim/event.pyi', 'vim/fault.pyi', 'vim/option.pyi', 'vim/view.pyi', 'vmodl/__init__.pyi', 'vmodl/fault.pyi', 'vmodl/query.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
