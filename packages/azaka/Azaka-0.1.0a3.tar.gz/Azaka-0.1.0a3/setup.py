# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azaka', 'azaka.commands', 'azaka.connection', 'azaka.objects', 'azaka.tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'azaka',
    'version': '0.1.0a3',
    'description': 'A work in progress API Wrapper around The Visual Novel Database (VNDB) written in Python.',
    'long_description': '<p align="center"> <img src="https://cdn-icons-png.flaticon.com/512/2322/2322246.png" height=200> </p>\n\n# WELCOME!\n\nWelcome to Azaka, a work-in-progress asynchronous API wrapper around the [visual novel database](https://vndb.org/) written in python.\n\nThis wrapper is aimed to provide 100% API coverage being extremely simple to use and powerful. Now let\'s discuss why you should use it in next section.\n\n# LINKS -\n\n- [Advantages](https://github.com/mooncell07/Azaka#advantages--)\n- [Disadvantages](https://github.com/mooncell07/Azaka#disadvantages--)\n- [Installation](https://github.com/mooncell07/Azaka#installation--)\n- [Usage](https://github.com/mooncell07/Azaka#usage--)\n- [Docs. & Tuts.](https://github.com/mooncell07/Azaka#documentation--tutorial--)\n- [Thanks](https://github.com/mooncell07/Azaka#thanks)\n\n## ADVANTAGES -\n\n- **Fully Asynchronous** - Everything which poses a threat of blocking the I/O for a significant amount of time is async.\n- **Caching** - Azaka supports caching reponses, which saves us from getting throttled quickly!\n- **Easy to Use** - Azaka provides a really easy to use interface for creating complex commands and a bunch of ready-made presets for those in hurry.\n- **Global Exception handling** - Azaka provides utility for handling command errors globally to save you from try-except hell! Also it does alot behind the screen to save you from sending and receiving bad stuff anyways!\n- **No Dependency requirement** - No third party dependency is required to do anything in entire library.\n\n\n## DISADVANTAGES -\n\n*(yes, i am a gud person)*\n\n- **Bloat** - A few decisions have been taken which have caused the lib. to weigh too much but trust me, it\'s not dead weight, they help with UX.\n- **Syntax Requirement** - I know, a lot of things are needed to be done even by the user to make it operational. I am working on fixing it.\n- **Slow Development & bug hunting** - I am the only person working on entire lib and i have a lot of work irl too so sorrryyy.\n- **Models are not well optimized** - All the models are fully constructed even if there is no need of some members. Working on it.\n- **Support** - Well.. i can only help with it so yea you can contact me on discord `Nova#3379`.\n\n\n## INSTALLATION -\n\nYou can install Azaka using pip.\n\n`pip install -U azaka`\n\nThat\'s it! There is no other required or optional requirement.\n\n## USAGE -\n\n*Example of getting basic VN data.*\n\n```py\nimport azaka\nfrom azaka import VNCondition as VN\n\nclient = azaka.Client()\n\n@client.register\nasync def main(ctx) -> None:\n    vn = await client.get_basic_vn_info(VN.ID == 60)\n    print(vn[0])\n\nclient.start()\n```\n\nAbove example used a preset (`client.get_basic_vn_info`), you can use azaka\'s Interface to build a command yourself!\n\n```py\nimport azaka\nfrom azaka import Type, Flags\n\nclient = azaka.Client()\n\n@client.register\nasync def main(ctx) -> None:\n    with azaka.Interface(type=Type.VN, flags=(Flags.BASIC,)) as interface:\n        VN = interface.condition()\n        interface.set_condition((VN.SEARCH % "fate") & (VN.ID == 50))\n\n    vn = await client.get(interface)\n    print(vn[0])\n\nclient.start()\n```\n\n## DOCUMENTATION & TUTORIAL -\n\nDocumentation is still in development and will be available soon!\n\n\n## THANKS\n\nThank you for your visit :)\n',
    'author': 'mooncell07',
    'author_email': 'mooncell07@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
