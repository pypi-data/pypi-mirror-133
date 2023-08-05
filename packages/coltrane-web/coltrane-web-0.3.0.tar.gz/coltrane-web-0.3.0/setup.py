# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coltrane', 'coltrane.management', 'coltrane.management.commands']

package_data = \
{'': ['*'], 'coltrane': ['templates/coltrane/*']}

install_requires = \
['Django>=4.0,<5.0',
 'click>=8.0.3,<9.0.0',
 'markdown2>=2.4.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0']

extras_require = \
{'gunicorn': ['gunicorn>=20.1.0,<21.0.0']}

entry_points = \
{'console_scripts': ['coltrane = coltrane.console:cli']}

setup_kwargs = {
    'name': 'coltrane-web',
    'version': '0.3.0',
    'description': 'Use Django as a static site',
    'long_description': '# coltrane\n\nA simple content site framework that harnesses the power of Django without the hassle.\n\n## Features\n\n- Can be a standalone static site or added to `INSTALLED_APPS` to integrate into an existing Django site\n- Renders markdown files automatically\n- Can use data from JSON files in templates and content\n- All the power of Django templates, template tags, and filters\n- Can include other Django apps\n- Build HTML output for a true static site (coming soon)\n\nStill a little experimental. ;)\n\n## Install\n\n### Create a standalone site\n\n1. Make a new directory for your site and traverse into it: `mkdir new-site && cd new-site`\n1. Install `poetry` (if needed): `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`\n1. Add `coltrane` dependency: `poetry init --dependency coltrane-web:latest && poetry install`\n1. Initialize `coltrane`: `poetry run coltrane init`\n1. Create secret key at https://djecrety.ir/ and update SECRET_KEY in .env\n1. Start local development server: `poetry run coltrane play`\n1. Go to localhost:8000 in web browser\n\n### Add to an existing Django site\n\nComing soon.\n\n## Render markdown files\n\n`coltrane` takes the URL slug and looks up a corresponding markdown file in the `content` directory.\n\nFor example: http://localhost:8000/this-is-a-good-example/ will render the markdown in `content/this-is-a-good-example.md`. The root (i.e. http://localhost:8000/) will look for `content/index.md`.\n\nIf a markdown file cannot be found, the response will be a 404.\n\n## Use JSON data\n\n`coltrane` is designed to be used without a database, however, sometimes it\'s useful to have access to data inside your templates.\n\n### data.json\n\nCreate a file named `data.json`: `echo {} >> data.json`. Add whatever data you want to that file and it will be included in the template context.\n\n`data.json`\n\n```JSON\n{\n    {"answer": 42}\n}\n```\n\n```markdown\n# index.md\n\n{{ data.answer }} == 42\n```\n\n```html\n<h1>index.md</h1>\n\n42 == 42\n```\n\n### JSON data directory\n\nCreate a directory named `data`: `mkdir data`. Create as many JSON files as you want. The name of the file (without the `json` extension) will be used as the key in the context data.\n\n`data/author.json`\n\n```JSON\n{\n    {"name": "Douglas Adams"}\n}\n```\n\n```markdown\n# index.md\n\n{{ data.author.name }} == Douglas Adams\n```\n\n```html\n<h1>index.md</h1>\n\nDouglas Adams == Douglas Adams\n```\n\n## Override templates\n\nOverriding templates work just like in Django.\n\n### Override base template\n\nCreate a file named `templates/coltrane/base.html` in your app to override the base template. By default, it needs to include a `content` block.\n\n```html\n{% block content %}{% endblock content %}\n```\n\n### Override content template\n\nCreate a file named `templates/coltrane/content.html` in your app to override the content template. By default, it needs to include a `content` block for the base template and `{{ content }}` to render the markdown.\n\n```html\n{% block content %}{{ content }}{% endblock content %}\n```\n\n## Build static HTML\n\n`coltrane record` will build the static HTML. Not currently implemented.\n\n## What\'s with the name?\n\n`coltrane` is built on top of the Django web framework, which is named after the Jazz musician Django Reinhardt. `coltrane` is named after another Jazz musician, John Coltrane.\n\n## Thanks\n\n- https://twitter.com/willmcgugan/status/1477283879841157123 for the initial inspiration\n- https://github.com/wsvincent/django-microframework for the `app.py` idea\n- https://olifante.blogs.com/covil/2010/04/minimal-django.html\n- https://simonwillison.net/2009/May/19/djng/\n- https://stackoverflow.com/questions/1297873/how-do-i-write-a-single-file-django-application\n- https://github.com/trentm/python-markdown2\n',
    'author': 'adamghill',
    'author_email': 'adam@adamghill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
