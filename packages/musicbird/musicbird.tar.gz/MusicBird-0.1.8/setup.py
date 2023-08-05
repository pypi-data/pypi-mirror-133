# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['musicbird']

package_data = \
{'': ['*'], 'musicbird': ['data/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'ffmpeg-python>=0.2.0,<0.3.0', 'schema>=0.7.5,<0.8.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'docs': ['Sphinx>=4.3.2,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinxcontrib-napoleon>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['musicbird = musicbird.__main__:entrypoint']}

setup_kwargs = {
    'name': 'musicbird',
    'version': '0.1.8',
    'description': 'Convert your music library on-the-fly!',
    'long_description': "MusicBird - Convert your Music library on-the-fly 🐦\n####################################################\n\n.. image:: https://img.shields.io/github/workflow/status/maxhoesel/MusicBird/CI.svg\n   :target: https://img.shields.io/github/workflow/status/maxhoesel/MusicBird/CI.svg\n.. image:: https://img.shields.io/pypi/pyversions/musicbird.svg\n   :target: https://img.shields.io/pypi/pyversions/musicbird.svg\n.. image:: https://img.shields.io/pypi/l/musicbird.svg\n   :target: https://img.shields.io/pypi/l/musicbird.svg\n.. image:: https://img.shields.io/codecov/c/github/maxhoesel/MusicBird.svg\n   :target: https://img.shields.io/codecov/c/github/maxhoesel/MusicBird.svg\n\n----\n\nMusicBird is a python package that creates a mobile-friendly copy of your music library. Its major features include:\n\n* It's *fast*! Not only does it use all your cores when encoding files, it also remembers the state of your library from when you last ran it.\n  This means that MusicBird will only process those files that have actually changed since then.\n* It works with any music library! You don't need to adjust your library structure at all for MusicBird to do its magic - in fact, you could make it read-only\n  and everything would still work just fine!\n* It tracks modified and deleted files! Did you change the tags of a file and want them on your phone as well?\n  Do you no longer like that artist and deleted all their music from your library? Don't worry!\n  MusicBird will pick up those changes and adjust the mirror copy accordingly\n* It's flexible! MusicBird uses the excellent `ffmpeg libraries <https://ffmpeg.org/>`_ under the hood,\n  meaning that most common input and output formats are supported.\n\nDocumentation\n=============\n\nSee the `official docs <https://musicbird.readthedocs.io/en/latest/>`_ for installation and usage instructions\n\nAuthor & License\n================\n\nWritten and maintained by Max Hösel (@maxhoesel)\n\nLicensed under the GNU GPLv3 or later\n",
    'author': 'Max Hösel',
    'author_email': 'musicbird@maxhoesel.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxhoesel/musicbird',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
