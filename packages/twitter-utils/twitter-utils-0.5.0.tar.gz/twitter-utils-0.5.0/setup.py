# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['twitter_utils', 'twitter_utils.workflows']

package_data = \
{'': ['*']}

install_requires = \
['py-executable-checklist>=0.10.0,<0.11.0',
 'selenium>=4.1.0,<5.0.0',
 'slug>=2.0,<3.0']

entry_points = \
{'console_scripts': ['tweets-between = twitter_utils.tweets_between:main',
                     'tweets-thread = twitter_utils.tweets_thread:main']}

setup_kwargs = {
    'name': 'twitter-utils',
    'version': '0.5.0',
    'description': 'Collection of twitter utilities.',
    'long_description': '# Twitter tools\n\n[![PyPI](https://img.shields.io/pypi/v/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)\n[![PyPI - License](https://img.shields.io/pypi/l/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)\n\n\n---\n\n**Documentation**: [https://namuan.github.io/twitter-utils](https://namuan.github.io/twitter-utils)\n\n**Source Code**: [https://github.com/namuan/twitter-utils](https://github.com/namuan/twitter-utils)\n\n**PyPI**: [https://pypi.org/project/twitter-utils/](https://pypi.org/project/twitter-utils/)\n\n---\n\nCollection of twitter utilities.\n\n## Installation\n\n```sh\npip install twitter-utils\n```\n\n## Example Usage\n\nAll commands in `twitter-utils` work better with an authenticated user otherwise Twitter bombards you with crap.\nThe following command is tested on MacOS and will create a symlink to your Firefox profile.\nPlease replace the source path with your own.\n\n```shell\nln -s "~/Library/Application\\ Support/Firefox/Profiles/.." $(pwd)/fireprofile\n```\n\nAll commands take an argument to specify the output directory.\nEach tweet captured will be saved in the output directory to a file with the file name as the tweet id.\n\n### Grab tweets of an account between two dates\n\n```shell\ntweets-between --account <<account>> --since 2020-04-10 --until 2020-04-25 -o temp-dir\n```\n\n### Grab tweets on a page\n\n```shell\ntweets-thread -a <<account>> -t <<tweet-id>> -o temp-dir\n```\n\n## Using twarc to capture tweet data using Twitter API\n\nYou can use [twarc](https://twarc-project.readthedocs.io/en/latest/) to get tweets given a list of ids.\nTwarc uses Twitter API so you\'ll need those credentials.\n[Twarc hydrate](https://twarc-project.readthedocs.io/en/latest/twarc1_en_us/#hydrate) command that will grab tweet data given a list of ids.\n```shell\n# Depending on your output directory, here is a command to get the list of file name (tweet ids)\nfind <output-folder>/*.html | while read file; do basename $file ".html"; done > <target-file-with-list-of-tweet-ids>\n\n# These feed this list of ids to twarc\ntwarc hydrate <target-file-with-list-of-tweet-ids> > <file-with-all-tweets-data>.jsonl\n```\n#### Selecting WebDriver\n\nAll commands in `twitter-utils` uses Firefox by default, but it can be overridden by providing an alternate browser.\nSupporting Firefox, Safari and Chrome.\n\nTo use Safari instead of Firefox, pass the `--browser` option before specifying the sub-command.\n\n```\n<cmd> --browser safari ...\n```\nAnd to use Chrome\n```\n<cmd> --browser chrome ...\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Validating build\n\n```sh\nmake build\n```\n\n### Release process\n\nA release is automatically published when a new version is bumped using `make bump`.\nSee `.github/workflows/build.yml` for more details.\nOnce the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.\n',
    'author': 'namuan',
    'author_email': 'github@deskriders.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://namuan.github.io/twitter-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
