# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.11.0']

setup_kwargs = {
    'name': 'xontrib-iterm2',
    'version': '0.0.2',
    'description': 'iTerm2 shell integration for Xonsh shell.',
    'long_description': '# iTerm2 Shell Integration\n[iTerm2](https://iterm2.com/index.html) \n[Shell integration](https://iterm2.com/documentation-escape-codes.html) for Xonsh shell. \n\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-iterm2\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-iterm2\n```\n\n## Usage\n\n``` bash\n# this modifies the $PROMPT function. So load it after setting $PROMPT if you have a custom value\nxontrib load iterm2\n```\n',
    'author': 'Noortheen Raja NJ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-iterm2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
