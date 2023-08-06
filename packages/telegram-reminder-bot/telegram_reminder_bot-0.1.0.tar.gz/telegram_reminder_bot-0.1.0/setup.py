# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_reminder_bot']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.11,<2.0.0',
 'croniter>=1.1.0,<2.0.0',
 'daemons[daemon]>=1.3.2,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-telegram-bot>=13.4.1,<14.0.0']

entry_points = \
{'console_scripts': ['telegram-reminder-bot = '
                     'telegram_reminder_bot.entrypoint:main']}

setup_kwargs = {
    'name': 'telegram-reminder-bot',
    'version': '0.1.0',
    'description': 'A telegram bot to remind you important stuff',
    'long_description': None,
    'author': 'Yoann Piétri',
    'author_email': 'me@nanoy.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
