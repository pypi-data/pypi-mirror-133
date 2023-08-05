# Twitter tools

[![PyPI](https://img.shields.io/pypi/v/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)
[![PyPI - License](https://img.shields.io/pypi/l/twitter-utils?style=flat-square)](https://pypi.python.org/pypi/twitter-utils/)


---

**Documentation**: [https://namuan.github.io/twitter-utils](https://namuan.github.io/twitter-utils)

**Source Code**: [https://github.com/namuan/twitter-utils](https://github.com/namuan/twitter-utils)

**PyPI**: [https://pypi.org/project/twitter-utils/](https://pypi.org/project/twitter-utils/)

---

Collection of twitter utilities.

## Installation

```sh
pip install twitter-utils
```

## Example Usage

This works better with a logged in user otherwise Twitter bombards you with popups and other crap.
The following command is tested on MacOS and will create a symlink to your Firefox profile.
Please replace the source path with your own.

```shell
ln -s "~/Library/Application\ Support/Firefox/Profiles/.." $(pwd)/fireprofile
```

All commands take an argument to specify the output directory.
Each tweet captured will be saved in the output directory to a file with the file name as the tweet id.

### Grab tweets of an account between two dates

```shell
tweets-between --account <<account>> --since 2020-04-10 --until 2020-04-25 -o temp-dir
```

### Grab tweets on a page

```shell
tweets-thread -a <<account>> -t <<tweet-id>> -o temp-dir
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Validating build

```sh
make build
```

### Release process

A release is automatically published when a new version is bumped using `make bump`.
See `.github/workflows/build.yml` for more details.
Once the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.
