# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfixfmt']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.4', 'black>=20.8b1', 'isort>=4.3.21']

setup_kwargs = {
    'name': 'pyfixfmt',
    'version': '0.9.2',
    'description': 'Run several python fixers over a python file, to provide simple, deterministic code formatting.',
    'long_description': "# PyFixFmt\n\nYour all-in-one python formatter. Able to be called on files or strings to format and standarize a Python file.\n\nRemoves unused imports (with [autoflake](https://github.com/myint/autoflake)), sorts imports (with [isort](https://github.com/PyCQA/isort)), and then formats the code (with [black](https://black.readthedocs.io/en/stable/)). It will respect your project's `pyproject.toml` configuration for those tools.\n\nMeant to make formatting of python code as deterministic as sanely possible.\n\n\n### Instructions\n\nTo install:\n\n`pip install pyfixfmt`\n\nTo run:\n\n```\n# file-glob can be either a single file name or a normal unix glob.\npython -m pyfixfmt --file-glob <your file glob here> --verbose\n```\n\nConfiguration:\n\n```\n# in pyproject.toml\n[tool.formatters.python]\n# Do not change anything about imports in these files\nignore_import_changes = []\n# Do not remove imports that are unused in these files\ndo_not_remove_imports = []\n```\n\n\n### Developing\n\nDevelop with [Poetry](https://python-poetry.org/).\n\nBuild with `poetry build`, and publish with `poetry publish`.",
    'author': 'TJ DeVries',
    'author_email': 'devries.timothyj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/untitled-ai/pyfixfmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
