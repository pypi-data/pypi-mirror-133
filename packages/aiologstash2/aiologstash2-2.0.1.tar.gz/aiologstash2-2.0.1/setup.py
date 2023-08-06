# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiologstash2']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=4.0.2,<5.0.0', 'python-logstash>=0.4.6,<0.5.0']

setup_kwargs = {
    'name': 'aiologstash2',
    'version': '2.0.1',
    'description': '',
    'long_description': "# aiologstash2\n\n[![image](https://travis-ci.org/aio-libs/aiologstash.svg?branch=master)](https://travis-ci.org/aio-libs/aiologstash)\n\n[![image](https://codecov.io/gh/aio-libs/aiologstash/branch/master/graph/badge.svg)](https://codecov.io/gh/aio-libs/aiologstash)\n\n[![image](https://badge.fury.io/py/aiologstash.svg)](https://badge.fury.io/py/aiologstash)\n\nasyncio logging handler for logstash.\n\n# Installation\n\n``` shell\npip install aiologstash2\n```\n\n# Usage\n\n``` python\nimport logging\nfrom aiologstash2 import create_tcp_handler\n\nasync def init_logger():\n     handler = await create_tcp_handler('127.0.0.1', 5000)\n     root = logging.getLogger()\n     root.setLevel(logging.DEBUG)\n     root.addHandler(handler)\n```\n\n# Thanks\n\nThis is an actively maintained fork of [aio-libs'\naiologstash](https://github.com/aio-libs/aiologstash)\n\nThe library was donated by [Ocean S.A.](https://ocean.io/)\n\nThanks to the company for contribution.\n",
    'author': 'Aviram Hassan',
    'author_email': 'aviramyhassan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aviramha/aiologstash2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
