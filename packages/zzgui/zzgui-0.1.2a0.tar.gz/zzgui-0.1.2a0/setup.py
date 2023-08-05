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
    'version': '0.1.2a0',
    'description': 'Python GUI toolkit',
    'long_description': '# The light Python GUI builder (currently based on PyQt5)\n\n# How start with pypi packege:\n```bash\npoetry new project_01 && cd project_01 && poetry shell\npoetry add zzgui\n```\n# How to run:\n```bash\ngit clone https://github.com/AndreiPuchko/zzgui.git\ncd zzgui\npip3 install poetry\npoetry shell\npoetry install\npython3 demo/demo.py\npython3 demo/demo_01.py\npython3 demo/demo_02.py\npython3 demo/demo_03.py\npython3 demo/demo_04.py\n```\n\n# demo/demo_03.py screenshot\n![Alt text](https://andreipuchko.github.io/zzgui/screenshot.png)\n# Build standalone executable \n(The resulting executable file will appear in the folder  dist/)\n## One file\n```bash\npyinstaller -F demo/demo.py\n```\n\n## One directory\n```bash\npyinstaller -D demo/demo.py\n```\n',
    'author': 'Andrei Puchko',
    'author_email': 'andrei.puchko@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
