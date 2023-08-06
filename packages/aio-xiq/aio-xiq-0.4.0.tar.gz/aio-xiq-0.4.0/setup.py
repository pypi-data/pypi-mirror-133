# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioxiq', 'aioxiq.v2']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.1,<0.19.0', 'tenacity>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'aio-xiq',
    'version': '0.4.0',
    'description': 'AsyncIO client for Extreme Cloud IQ',
    'long_description': '# Extreme Cloud IQ - Python3 AsyncIO Client\n\nThis repository contains a Python3 asyncio based client library for interacting\nwith the Extreme Cloud IQ system (XIQ).\n\nNote that Extreme does provide their own Python SDK client, which can be found\nin the reference section below.\n\n# Installation\n\n```shell\npip install aio-xiq\n```\n\nThis XIQ asyncio python client is a subclass from httpx.AsyncClient.\n\n# QuickStart\n\nBefore using the API you must either have an existing token or login with your user-name + password\ncredentials.  You can either pass these values into the client constructor, or use these environment variables:\n\n* XIQ_USER - the login user-name\n* XIQ_PASSWORD = the login password\n<br/>\n-- or --\n* XIQ_TOKEN - an existing API token\n\n**Username + Password**\n\nIf you are using your login credentials you must execute the `login()` method to obtain an access\ntoken.\n\n```python\nfrom aioxiq import XiqClient\n\nasync with XiqClient(xiq_user=\'bob@corp.com\', xiq_password=\'notarealpassword\') as api:\n    await api.login()\n    devices = await api.fetch_devices()\n```\n\n**API Token**\n\nYou can create an API token via the XIQ portal by nagivating to the Global\nSettings page (found under your User profile near the top-right), and then\nselecting the "API Token Management" option on the left sidebar.\n\nWhen using the API Token approach, you can use the client diretly without having\nto perform the login function.\n\n```python\nfrom aioxiq import XiqClient\n\n# presume that XIQ_TOKEN environment variable is set with an existing token.\n# you can immediately use the API without login.\n\nasync with XiqClient() as api:\n    devices = api.fetch_devices()\n```\n\n### References\n * [Extreme Developer Portal](https://developer.extremecloudiq.com/)\n * [Extreme XIQ API Online Docts, Swagger](https://api.extremecloudiq.com/swagger-ui/index.html?configUrl=/openapi/swagger-config)\n * [Extreme XIQ APIs Github repo](https://github.com/extremenetworks/ExtremeCloudIQ-APIs)\n * [Extreme XIQ Python SDK Github repo](https://github.com/extremenetworks/ExtremeCloudIQ-SDK-Python)\n',
    'author': 'Jeremy Schulman',
    'author_email': 'jeremy.schulman@mlb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeremyschulman/aio-xiq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
