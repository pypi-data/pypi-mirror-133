# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mandown', 'mandown.sources']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'feedparser>=6.0.8,<7.0.0',
 'requests>=2.27.0,<3.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['mandown = mandown:cli']}

setup_kwargs = {
    'name': 'mandown',
    'version': '0.1.0',
    'description': 'Command line application and library to download manga from various sources',
    'long_description': None,
    'author': 'Daniel Chen',
    'author_email': 'danielchen04@hotmail.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
