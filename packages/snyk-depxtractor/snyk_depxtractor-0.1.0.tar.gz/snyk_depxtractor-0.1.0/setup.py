# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snyk_depxtractor']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pyarrow>=6.0.1,<7.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['sde = snyk_depxtractor.cli:cli']}

setup_kwargs = {
    'name': 'snyk-depxtractor',
    'version': '0.1.0',
    'description': 'Snyk Dependency Extractor',
    'long_description': '# snyk-dependency-extractor\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)\n---\nTool to extract dependencies from a Snyk group. Initial version, updates may come.\n\nThe tool uses 5 threads to process the organizations inside the group, and 4 threads for each org to process the deps. This way we can avoid slowing ourselves (mostly) by throttling on huge orgs.\n\n-   Free software: [GNU General Public License\n    v3.0](https://github.com/zsolt-halo/snyk-depxtractor/blob/master/LICENSE)\n<!-- -   Documentation: <https://snyk-dependency-extractor.readthedocs.io>. -->\n\n## Features\n\n- Extract all dependencies from a Snyk group into a csv in the local folder\n\n## Todo\n- [ ] Configure output folder/file\n- [x] Enable multiple output formats, json/parquet\n- [ ] Pypi package\n- [ ] CLI command\n- [ ] Proper docs/testing\n- [ ] Pipeline\n\n## Install\n\nUse `pip` for install:\n\n``` console\n# clone the repo and install the deps/enter venv\n$ poetry install\n$ poetry shell\n# export your Snyk token with group admin privs\n$ export SNYK_TOKEN=xxxxxxxx\n$ cd snyk_depxtractor\n$ python cli.py dump-group-deps\n```\n\nIf you want to setup for development:\n\n``` console\n$ # Install poetry using pipx\n$ python -m pip install pipx\n$ python -m pipx ensurepath\n$ pipx install poetry\n\n$ # Clone repository\n$ git clone https://github.com/zsolt-halo/snyk-depxtractor.git\n$ cd snyk-dependency-extractor/\n\n$ # Install dependencies and hooks\n$ poetry install\n$ poetry run pre-commit install\n```\n\n## Known Issues\n`poetry build` produces a wheel which when installed, has some path issues and throws an error `from core import core`\n\nWill fix it eventually :)\n',
    'author': 'Zsolt Halo',
    'author_email': 'net.zsolt.net@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zsolt-halo/snyk-depxtractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
