# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gharbala']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'Pillow>=8.4.0,<9.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'bs4>=0.0.1,<0.0.2',
 'google-cloud-translate>=3.6.1,<4.0.0',
 'htmlmin>=0.1.12,<0.2.0',
 'internetarchive>=2.2.0,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'requests>=2.26.0,<3.0.0',
 'sentry-sdk>=1.5.1,<2.0.0',
 'spleeter>=2.3.0,<3.0.0',
 'tornado>=6.1,<7.0',
 'youtube_dl>=2021.12.17,<2022.0.0',
 'yt-dlp>=2021.12.27,<2022.0.0']

entry_points = \
{'console_scripts': ['gharbala = gharbala.main:main']}

setup_kwargs = {
    'name': 'gharbala',
    'version': '0.1.6',
    'description': 'Remove music from videos and publish it to wordpress as posts',
    'long_description': None,
    'author': 'Ahmed Kamel',
    'author_email': 'k.tricky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
