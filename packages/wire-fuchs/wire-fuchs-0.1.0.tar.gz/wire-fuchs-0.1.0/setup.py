# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuchs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wire-fuchs',
    'version': '0.1.0',
    'description': 'Template engine for smart foxes, in python',
    'long_description': '# Fuchs Templates\n\n<img  src="https://images.unsplash.com/photo-1605101479435-005f9c563944?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8Zm94fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60" style="border-radius: 7px;width: 300px; margin-top: -50px;" align="right">\n\n> Fuchs Templates is a simple template engine for HTML/XML written in Python.\n\nFuchs is the successor of [TEX](https://pypi.org/project/tex-engine) (Template Engine X)\n\n## Inspiration\n\nFuchs was clearly influenced by template engines like Handlebars, Jinja and Genshi. And deliberately combines everything to ensure the best comfort with the highest quality.\n\n## Functional references\n\nFuchs takes its cue from PHP, it has a syntax that allows to execute Python code.\n\n```html\n<!DOCTYPE html>\n<html>\n    <?fuchs \n        # valid python code inside here\n        abc = "abc"\n    ?>\n    <p>{{abc}}</p>\n</html>\n```\n\n```html\n<!DOCTYPE html>\n<html>\n    <?fuchs \n        # valid python code inside here\n        import random\n        abc = random.randint(1,10)\n    ?>\n    <p>{{abc}}</p>\n</html>\n``` \n\n## Why not Jinja?\n\nFor my web framework Wire, I really wanted something that came from myself.  I mean, it\'s easy to add any dependency and be satisfied. But, I don\'t want that. \n\n\n# Note\nSince Fuchs works exclusively on the server side, any security measures were removed when evaluating the code. Keywords like `quit()`, `exit()` etc. are therefore usable. \nPlease avoid using them.',
    'author': 'cheetahbyte',
    'author_email': 'bernerdoodle@outlook.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cheetahbyte/fuchs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
