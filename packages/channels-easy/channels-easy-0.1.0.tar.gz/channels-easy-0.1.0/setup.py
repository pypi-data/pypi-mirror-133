# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['channels_easy']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0', 'channels>=3.0']

setup_kwargs = {
    'name': 'channels-easy',
    'version': '0.1.0',
    'description': 'A thin wrapper around channels consumer to make things EASY',
    'long_description': "channels-easy\n============\n\nA thin wrapper around channel consumers to make things **EASY**.\n\nInstallation\n------------\n\nTo get the latest stable release from PyPi\n\n```bash\npip install channels-easy\n```\nTo get the latest commit from GitHub\n\n```bash\npip install -e git+git://github.com/namantam1/channels-easy.git#egg=channels-easy\n```\n<!-- TODO: Describe further installation steps (edit / remove the examples below): -->\n\nAdd ``channels-easy`` to your ``INSTALLED_APPS``\n\n```bash\nINSTALLED_APPS = (\n    ...,\n    'channels-easy',\n)\n```\n<!-- Add the ``channels-easy`` URLs to your ``urls.py``\n\n```bash\nurlpatterns = [\n    url(r'^VAR_URL_HOOK/', include('channels-easy.urls')),\n]\n``` -->\n\nUsage\n-----\n\nTODO: Describe usage or point to docs. Also describe available settings.\n\n\nContribute\n----------\n\nIf you want to contribute to this project, please perform the following steps\n\n````bash\n# Fork this repository\n# Clone your fork\npoetry install\n\ngit checkout -b feature_branch master\n# Implement your feature and tests\ngit add . && git commit\ngit push -u origin feature_branch\n# Send us a pull request for your feature branch\n````\n<!-- In order to run the tests, simply execute ``tox``. This will install two new\nenvironments (for Django 1.8 and Django 1.9) and run the tests against both\nenvironments. -->\n",
    'author': 'Naman Tamrakar',
    'author_email': 'namantam1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/namantam1/channels-easy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
