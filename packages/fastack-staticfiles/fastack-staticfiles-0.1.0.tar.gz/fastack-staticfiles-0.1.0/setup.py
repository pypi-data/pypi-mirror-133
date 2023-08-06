# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack_staticfiles']

package_data = \
{'': ['*']}

install_requires = \
['fastack>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'fastack-staticfiles',
    'version': '0.1.0',
    'description': 'Easy to add static files',
    'long_description': '# fastack-staticfiles\n\nEasy to add static files\n\n# Usage\n\n```\npip install fastack-staticfiles\n```\n\nAdd the plugin to your project configuration\n\n```py\nPLUGINS = [\n    "fastack_staticfiles",\n    ...\n]\n```\n\nPlugin configuration example\n\n```py\nSTATICFILES = [\n    (\n        "/static",\n        "static",\n        {"directory": "assets", "packages": [], "html": False, "check_dir": True},\n    )\n]\n```\n\nConfiguration format like this `(path: str, name: str, options: dict)`\nThe `options` here will be passed to `starlette.staticfiles.StaticFiles`.\n',
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': 'aprilahijriyan',
    'maintainer_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'url': 'https://github.com/fastack-dev/fastack-staticfiles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
