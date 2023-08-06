# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coltrane', 'coltrane.management', 'coltrane.management.commands']

package_data = \
{'': ['*'], 'coltrane': ['templates/coltrane/*']}

install_requires = \
['Django>3.0',
 'click>=8.0.0,<9.0.0',
 'markdown2>=2.4.2,<3.0.0',
 'python-dotenv>0.17']

extras_require = \
{'gunicorn': ['gunicorn>=20.1.0,<21.0.0']}

entry_points = \
{'console_scripts': ['coltrane = coltrane.console:cli']}

setup_kwargs = {
    'name': 'coltrane-web',
    'version': '0.5.0',
    'description': 'Use Django as a static site',
    'long_description': '# coltrane\n\nA simple content site framework that harnesses the power of Django without the hassle.\n\n## Features\n\n- Can be a standalone static site or added to `INSTALLED_APPS` to integrate into an existing Django site\n- Renders markdown files automatically\n- Can use data from JSON files in templates and content\n- All the power of Django templates, template tags, and filters\n- Can include other Django apps\n- Build HTML output for a true static site (coming soon)\n\nStill a little experimental. ;)\n\n## Install\n\n### Create a standalone site\n\n1. Make a new directory for your site and traverse into it: `mkdir new-site && cd new-site`\n1. Install `poetry` (if not already installed) to handle Python packages: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`\n1. Create `poetry` project, add `coltrane` dependency, and install Python packages: `poetry init --no-interaction --dependency coltrane-web:latest && poetry install`\n1. Start a new `coltrane` site: `poetry run coltrane create`\n1. Start local development server: `poetry run coltrane play`\n1. Go to localhost:8000 in web browser\n\n### Add to an existing Django site\n\nComing soon.\n\n## Render markdown files\n\n`coltrane` takes the URL slug and looks up a corresponding markdown file in the `content` directory.\n\nFor example: http://localhost:8000/this-is-a-good-example/ will render the markdown in `content/this-is-a-good-example.md`. The root (i.e. http://localhost:8000/) will look for `content/index.md`.\n\nIf a markdown file cannot be found, the response will be a 404.\n\n## Use JSON data\n\n`coltrane` is designed to be used without a database, however, sometimes it\'s useful to have access to data inside your templates.\n\n### JSON data file\n\nCreate a file named `data.json` in your project folder: `touch data.json`. Add whatever data you want to that file and it will be included in the template context.\n\n#### `data.json`\n\n```JSON\n{\n    {"answer": 42}\n}\n```\n\n#### `index.md` file\n\n```markdown\n# index\n\nThe answer to everything is {{ data.answer }}\n```\n\n#### Generated `index.html`\n\n```html\n<h1>index</h1>\n\n<p>The answer to everything is 42</p>\n```\n\n### JSON data directory\n\nCreate a directory named `data` in your project folder: `mkdir data`. Create as many JSON files as you want. The name of the file (without the `json` extension) will be used as the key in the context data.\n\n#### `data/author.json`\n\n```JSON\n{\n    {"name": "Douglas Adams"}\n}\n```\n\n#### `index.md` file\n\n```markdown\n# index\n\n{{ data.author.name }} is the author\n```\n\n#### Generated `index.html`\n\n```html\n<h1>index.md</h1>\n\n<p>Douglas Adams is the author</p>\n```\n\n## Override templates\n\nOverriding templates work just like in Django. `coltrane` comes with two minimal templates: `base.html` and `content.html`.\n\n### Override base template\n\nCreate a file named `templates/coltrane/base.html` in your app to override the base template. By default, it needs to include a `content` block.\n\n```html\n{% block content %}{% endblock content %}\n```\n\n### Override content template\n\nCreate a file named `templates/coltrane/content.html` in your app to override the content template. By default, it needs to include a `content` block for the base template and `{{ content }}` to render the markdown.\n\nNote: `content` is already marked safe so the rendered HTML will be output correctly and you do not need to use a `safe` filter for the content template variable.\n\n```html\n{% block content %}{{ content }}{% endblock content %}\n```\n\n## Build static HTML\n\n`coltrane record` will build the static HTML. Coming soon.\n\n## What\'s with the name?\n\n`coltrane` is built on top of the Django web framework, which is named after [Django Reinhardt](https://en.wikipedia.org/wiki/Django_Reinhardt). Following in that tradition, I named this static site framework after [John Coltrane](https://en.wikipedia.org/wiki/John_Coltrane), another jazz musician.\n\n## Other Python static site builder alternatives\n\n- [Combine](https://combine.dropseed.dev/) which uses Jinja templates under the hood\n- [Pelican](https://blog.getpelican.com/)\n- [Nikola](https://getnikola.com/)\n\n## Thanks\n\n- https://twitter.com/willmcgugan/status/1477283879841157123 for the initial inspiration\n- https://github.com/wsvincent/django-microframework for the `app.py` idea\n- https://olifante.blogs.com/covil/2010/04/minimal-django.html\n- https://simonwillison.net/2009/May/19/djng/\n- https://stackoverflow.com/questions/1297873/how-do-i-write-a-single-file-django-application\n- https://github.com/trentm/python-markdown2\n',
    'author': 'adamghill',
    'author_email': 'adam@adamghill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adamghill/coltrane/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
