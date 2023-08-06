# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vurf', 'vurf.parser']

package_data = \
{'': ['*'], 'vurf': ['defaults/*']}

install_requires = \
['click>=8.0.0,<9.0.0', 'tomli<3.0.0']

entry_points = \
{'console_scripts': ['vurf = vurf.cli:main']}

setup_kwargs = {
    'name': 'vurf',
    'version': '2.0.0',
    'description': "Viliam's Universal Requirements Format",
    'long_description': '# VURF\n![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)\n\n![forthebadge](https://forthebadge.com/images/badges/pretty-risque.svg)\n\n![forthebadge](https://forthebadge.com/images/badges/works-on-my-machine.svg)\n\n[![PyPI version](https://badge.fury.io/py/vurf.svg)](https://badge.fury.io/py/vurf)\n\n> Viliam\'s Universal Requirements Format\n\n## What it is\n*VURF* is a format, parser, CLI, and python module for saving packages into Python-ish looking file.\nIt supports different *sections*, *conditionals* and deep nesting and envaluation thanks to AST parser.\n\n### Example packages.vurf\n```python\nwith pip:\n  vurf\n  black\n  click==8.0.0\n  if at_work:\n    ql-cq\n    ql-orange\nwith brew:\n  nnn  # terminal file manager\n```\n\n## Installation\n```sh\npip install vurf\n```\n\n## Usage\n```sh\n# Do something to initialize config and packages files\n$ vurf default\n\n# Basic operations\n$ vurf add some-package\n$ vurf remove package\n\n# Print packages\n$ vurf packages\n\n# Install them\n$ vurf install\n```\n\nFor all options look at [CLI](#CLI) section and for integration with other tools look at [Automation](./automation/).\n\n## CLI\n```\n$ vurf\nUsage: vurf [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -q, --quiet  Don\'t produce unnecessary output.\n  --version    Show the version and exit.\n  --help       Show this message and exit.\n\nCommands:\n  add              Add package(s).\n  config           Edit config file.\n  default          Print default section.\n  edit             Edit packages file.\n  format           Format packages file.\n  has              Exit with indication if package is in packages.\n  has-section      Exit with indication if section is in sections.\n  install          Install packages.\n  package-section  Print the first section that contains the package.\n  packages         Print list of packages.\n  print            Print contents of packages file.\n  remove           Remove package(s).\n  sections         Print list of sections.\n  uninstall        Uninstall packages.\n```\n\n### Completions\nShell completions are installed into `vurf_completions` in your `side-packages`.\nThe easiest way to find the location is to run `pip show -f vurf | grep Location`.\n\nThen you can source them for example like this\n```bash\n# .bashrc\nsource "/Users/viliam/Library/Python/3.10/lib/python/site-packages/vurf_completions/completions.bash"\n```\n\n## Config\n\nNote: *VURF* will automatically create config file on the first run.\n\n### Config file format\n```toml\n# Where packages file is saved\npackages_location = "/Users/viliam/packages.vurf"\n# Name of the default section\ndefault_section = "brew"\n\n# Sections can be though of as installers for different packages\n# `install` and `uninstall` attributes are optional and default to `echo`\n# `sequential` attribute is optional and defaults to `false`\n# Use `sequential = true` if you want to install/uninstall packages one by one\n[[sections]]\nname = "brew"\ninstall = "brew install"\nuninstall = "brew uninstall"\nsequential = false\n\n[[sections]]\nname = "cask"\ninstall = "brew install --cask"\n\n[[sections]]\nname = "python"\ninstall = "pip install --quiet --user"\nuninstall = "pip uninstall"\n\n# Parameters are constants that can be accessed from conditionals\n[parameters]\nhostname = "mac"\nprimary_computer = true\nfs = "apfs"\n```\n\n## Grammar\n*VURF* has [grammar](./vurf/parser/grammar.lark) and LALR(1) parser implemented in [Lark](https://github.com/lark-parser/lark).\nThe "source code" aims to look like Python code as much as possible.\n\n### Keywords\n* `with [section]` - specifies "section" of requirements file. Different sections usually have different installers.\n* `if [condition]:` - conditions for including packages. See [Conditionals](##Conditionals) sections.\n* `elif [condition]:`\n* `else:`\n* `...` - ellipsis - placeholder for empty section.\n\n### Packages\n* are saved as `[name]  # [comment]`\n* `name` can be almost any valid package name (cannot start with "." or contain tabs or newline characters)\n* names containing spaces must be quoted. E.g. `\'multi word package name\'`\n* comments are optional\n\n## Conditionals\nConditionals are evaluated using Python\'s `eval` function.\nThey can be as simple as \n\n```python\nif var:\n  ...\n```\n\nor as complex as\n\n```python\nif pathlib.Path(\'some-file\').exists() and os.lstat(\'some-file\').st_mode == 33188:\n  ...\n```\n\nEvaluation has access to standard library modules:\n* [os](https://docs.python.org/3/library/os.html)\n* [pathlib](https://docs.python.org/3/library/pathlib.html)\n* [subprocess](https://docs.python.org/3/library/subprocess.html)\n\nand also to configuration variables defined in `config.toml`.\n\n## Module\n*VURF* provides python module that exposes approximately the same API as the CLI.\n\n### Example\n```python\nfrom vurf import Vurf\n\nwith Vurf.context() as packages:\n    sections = packages.sections()\n    packages.add(\'some-package\', section = sections[1])\n    assert packages.has(\'some-package\')\n    packages.remove([\'other-package\', \'third-package\'])\n```\n',
    'author': 'Viliam Valent',
    'author_email': 'vurf@valent.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ViliamV/vurf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
