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
    'version': '0.1.1',
    'description': 'Command line application and library to download manga from various sources',
    'long_description': '# mandown\n\nPython library and command line application to download books from various sources including manga\n\nCurrently only supports MangaSee.\n\n## Dependencies\n\n- python = "^3.8"\n- typer = "^0.4.0"\n- feedparser = "^6.0.8"\n- beautifulsoup4 = "^4.10.0"\n- requests = "^2.27.0"\n\n## Usage\n\n```\nmandown URL DESTINATION_FOLDER\n```\n\nRun `python cli.py --help` for more info.\n\n## Library usage\n\n```python\nfrom mandown import mandown\n\nmd.download(url_to_manga, destination_folder, start_chapter=None, end_chapter=None, maxthreads=4)\n\nmanga = md.query(url_to_manga)\nprint(manga.metadata, manga.chapters)\n```\n',
    'author': 'Daniel Chen',
    'author_email': 'danielchen04@hotmail.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/potatoeggy/mandown',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
