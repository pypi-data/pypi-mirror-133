# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['prefs', 'prefs.parser']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'click>=8.0.3,<9.0.0', 'lark>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['prefs = prefs.cli:main']}

setup_kwargs = {
    'name': 'prefs',
    'version': '1.0.0',
    'description': 'Store and manage preferences easily.',
    'long_description': '# PREFS\n> **Store and manage preferences easily.**  \n\n[![PREFS logo](https://github.com/Patitotective/PREFS/blob/main/assets/logo.png?raw=true)](https://patitotective.github.io/PREFS)\n\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/prefs)](https://pypi.org/project/prefs/)\n[![PREFS version](https://img.shields.io/pypi/v/prefs)](https://pypi.org/project/prefs/)\n[![Downloads](https://pepy.tech/badge/prefs)](https://pepy.tech/project/prefs)\n[![Stars](https://img.shields.io/github/stars/patitotective/prefs)](https://github.com/Patitotective/PREFS/stargazers)\n[![Watchers](https://img.shields.io/github/watchers/Patitotective/PREFS)](https://github.com/Patitotective/PREFS/watchers)\n\n[![Build](https://img.shields.io/appveyor/build/Patitotective/PREFS)](https://ci.appveyor.com/project/Patitotective/prefs)\n[![Last commit](https://img.shields.io/github/last-commit/Patitotective/PREFS)](https://github.com/Patitotective/PREFS/commits/main)\n![Size](https://img.shields.io/github/repo-size/Patitotective/PREFS)\n[![License MIT](https://img.shields.io/github/license/Patitotective/PREFS)](https://github.com/Patitotective/PREFS/)  \n\n[![Made with Python](https://img.shields.io/badge/made%20with-python-blue)](https://www.python.org/)\n[![Discord server](https://img.shields.io/discord/891409914533118012?logo=discord)](https://discord.gg/as85Q4GnR6)\n\n**PREFS** is Python library that stores preferences in a text file with a dictionary-like structure.\n\n## Installation\nOn _Windows_:  \n`pip install PREFS`\n\nOn _MacOS_ and _Linux_:  \n`pip3 install PREFS`\n\n### Getting started\nTo initialize your preferences you will need to instance the `Prefs` class with the first argument as the default preferences (the ones used the first time the program runs or whenever the file gets deleted).\n\n```py\nimport prefs\n\ndefault_prefs = {\n  "lang": "en", \n  "theme": {\n    "background": "#ffffff", \n    "font": "UbuntuMono", \n  }, \n}\n\nmy_prefs = prefs.Prefs(default_prefs)\n```\n\nThe above code will create a file called `prefs.prefs` that looks like:\n```py\n#PREFS\nlang=\'en\'\ntheme=>\n  background=\'#ffffff\' \n  font=\'UbuntuMono\'\n```\nThen you can change values as if it were a dictionary.\n```py\nmy_prefs["lang"] = "es"\n```\nAnd now `prefs.prefs` will look like:\n```py\n#PREFS\nlang=\'es\'\ntheme=>\n  background=\'#ffffff\'\n  font=\'UbuntuMono\'\n```\n\nYou can write your own _PREFS_ files manually as well, to manage your application\'s color scheme or the translations.\n\n***\n\n## About\n- Docs: https://patitotective.github.io/PREFS/docs/start.\n- GitHub: https://github.com/Patitotective/PREFS.\n- Pypi: https://pypi.org/project/PREFS/.\n- Discord: https://discord.gg/as85Q4GnR6.\n\nContact me:\n- Discord: **Patitotective#0127**.\n- Tiwtter: [@patitotective](https://twitter.com/patitotective).\n- Email: **cristobalriaga@gmail.com**.\n\n***v1.0.0***\n',
    'author': 'Patitotective',
    'author_email': 'cristobalriaga@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Patitotective/PREFS',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
