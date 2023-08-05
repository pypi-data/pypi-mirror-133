# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_priv', 'django_priv.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0']

setup_kwargs = {
    'name': 'django-priv',
    'version': '0.2.0',
    'description': 'yow',
    'long_description': None,
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
