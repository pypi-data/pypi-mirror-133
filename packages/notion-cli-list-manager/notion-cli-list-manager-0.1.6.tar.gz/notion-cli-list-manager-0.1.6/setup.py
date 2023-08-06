# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notion_cli_list_manager']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'prettytable>=2.5.0,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['list = notion_cli_list_manager.main:app']}

setup_kwargs = {
    'name': 'notion-cli-list-manager',
    'version': '0.1.6',
    'description': 'A simple command-line tool for managing Notion databases.',
    'long_description': '\n##### ⚠️ This project is still in work in progress, please forgive any little flaw here and there.\n# Notion CLI List Manager 🗂\nA simple command-line tool for managing [Notion](http://notion.so) ___List___ databases. ✨  \n\n### Increase your productivity with a simple command. 🛋\n\n![](showcase.gif)\n\n## 📺 Features:\n- fast and clear; saving your idea is as simple as type `add "get money"` 💆\u200d♂️\n- tables are pretty-printed with fab ASCII tables 🌈\n- parameters are now supported [^3] 🎻\n\n\n## 👾 Get Started:\n- Create a new internal api integration [here](https://www.notion.so/my-integrations).\n- ❗️ Share the default database you want to use with your integration.  \n  You can copy [my free simple template](https://jacksalici.notion.site/d75c9590dc8b4d62a6c65cbf3fdd1dfb?v=0e3782222f014d7bb3e44a87376e3cfb).\n- Download the tool: [^1]\n```\n    pip install notion-cli-list-manager\n```\n- Set the token and your default database id:\n```\n    list set --token [token] --id [database-id]\n``` \n- You\'re done!\n\n## 🧰 Syntax:\nTL;DR: `list` is the keyword for activating this tool from the terminal. Typing just `list`, the list of your default database\'s items will be shown. Other commands can be used typing `list [command]`\n\n| Commands:|    | Args and options:|\n|---|---|---|\n| `list` | to display all the ___List___ items. | `--db [id] ` to display a specific database. Otherwise the default database will be shown.<br> `--all` to display all the lists.\n| `list add [title]` | to add a new ___List___ item called `title`. |   `[title]` will be the text of the ___List___ item (and the title of the associated Notion database page)  <br> `--db [id] ` to add the entry to a specific database. Otherwise, the default database will be used.| \n| `list rm [index]` | to remove the ___List___ item with the index `index`.  <br> _(Command to call after `list`)_| `[index]` has to be formatted either like a range or a list, or a combination of these. E.g.: 3,4,6:10:2 will remove pages 3, 4, 6, 8.\n| `list db` | to display all the notion display saved in the manager. | `--label [LABEL] --id [ID]` to add a database to the manager. A prompt will then ask you the ordered indexes list.<br> `--rm [LABEL]` to remove a database named [LABEL] from the manager. Note that adding or removing a database to the manager does not cause the actual creation or deletion on Notion. <br> `--prop [LABEL]` to set which and in which order display the properties of an already saved database labeled [LABEL]. A prompt will then ask you the ordered indexes list[^3].\n| `list set --token [token] --id [database_id]` | to set the token and the ID of the Notion Database you want as default. _This must be executed as the first command_. | You can get the `[token]` as internal api integration [here](https://www.notion.so/my-integrations). <br> You can get the database id from the database url: notion.so/[username]/`[database_id]`?v=[view_id]. <br> You can also use separately `--token` and `--id` to set just one parameter. After the `--id` command, a prompt will then ask you the ordered indexes list.   |\n\n## 🛒 Still to do:\nSee the [project tab](https://github.com/jacksalici/notion-cli-list-manager/projects/1) for a complete and real-time-updated list.    \nIssues and PRs are appreciated. 🤝\n\n\n[^3]: At the present, properties are fully supported (except Relations and Rolls up that are __NS__ - Not supported) but read-only. Writeable ones will be supported in the next versions.\n\n[^1]: You can also clone the repo to have always the very last version.  \nHaving installed Python3 and Pip3 on your machine, write on the terminal:  \n`git clone https://github.com/jacksalici/notion-cli-list-manager.git notion-cli-list-manager`  \n`pip3 install notion-cli-list-manager/dist/notion-cli-list-manager-[last-version].tar.gz`\n\n\n\n\n    \n',
    'author': 'Jack Salici',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacksalici/notion-cli-list-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
