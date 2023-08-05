# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zzgui', 'zzgui.qt5', 'zzgui.qt5.widgets']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0', 'QScintilla>=2.13.1,<3.0.0', 'zzdb>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'zzgui',
    'version': '0.1.0',
    'description': 'Python GUI toolkit',
    'long_description': None,
    'author': 'Andrei Puchko',
    'author_email': 'andrei.puchko@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
