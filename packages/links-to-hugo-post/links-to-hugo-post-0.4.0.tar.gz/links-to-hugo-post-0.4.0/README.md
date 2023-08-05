# Links to Hugo Post

[![PyPI](https://img.shields.io/pypi/v/links-to-hugo-post?style=flat-square)](https://pypi.python.org/pypi/links-to-hugo-post/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/links-to-hugo-post?style=flat-square)](https://pypi.python.org/pypi/links-to-hugo-post/)
[![PyPI - License](https://img.shields.io/pypi/l/links-to-hugo-post?style=flat-square)](https://pypi.python.org/pypi/links-to-hugo-post/)


---

**Documentation**: [https://namuan.github.io/links-to-hugo-post](https://namuan.github.io/links-to-hugo-post)

**Source Code**: [https://github.com/namuan/links-to-hugo-post](https://github.com/namuan/links-to-hugo-post)

**PyPI**: [https://pypi.org/project/links-to-hugo-post/](https://pypi.org/project/links-to-hugo-post/)

---

Convert a list of links to a Hugo blog post.

## Installation

```sh
pip install links-to-hugo-post
```

## Example Usage

```shell

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
