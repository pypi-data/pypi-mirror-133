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
    'version': '0.6.0',
    'description': 'Use Django as a static site',
    'long_description': '# coltrane\n\nA simple content site framework that harnesses the power of Django without the hassle.\n\n## Features\n\n- Can be a standalone static site or added to `INSTALLED_APPS` to integrate into an existing Django site\n- Renders markdown files automatically\n- Can use data from JSON files in templates and content\n- All the power of Django templates, template tags, and filters\n- Can include other Django apps\n- Build HTML output for a true static site (coming soon)\n\nStill a little experimental. ;)\n\n## Install\n\n### Create a standalone site\n\n1. Make a new directory for your site and traverse into it: `mkdir new-site && cd new-site`\n1. Install `poetry` (if not already installed) to handle Python packages: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`\n1. Create `poetry` project, add `coltrane` dependency, and install Python packages: `poetry init --no-interaction --dependency coltrane-web:latest && poetry install`\n1. Start a new `coltrane` site: `poetry run coltrane create`\n1. Start local development server: `poetry run coltrane play`\n1. Go to localhost:8000 in web browser\n\n### Add to an existing Django site\n\nComing soon.\n\n## Render markdown files\n\n`coltrane` takes the URL slug and looks up a corresponding markdown file in the `content` directory.\n\nFor example: http://localhost:8000/this-is-a-good-example/ will render the markdown in `content/this-is-a-good-example.md`. The root (i.e. http://localhost:8000/) will look for `content/index.md`.\n\nIf a markdown file cannot be found, the response will be a 404.\n\n## Templates\n\n`coltrane` comes with two minimal templates that get used by default: `coltrane/base.html` and `coltrane/content.html`. Overriding those templates work just like in Django.\n\n### Override base template\n\nCreate a file named `templates/coltrane/base.html` in your app to override the base template. By default, it needs to include a `content` block.\n\n```html\n{% block content %}{% endblock content %}\n```\n\n### Override content template\n\nCreate a file named `templates/coltrane/content.html` in your app to override the content template. By default, it needs to include a `content` block for the base template and `{{ content }}` to render the markdown.\n\nNote: `content` is already marked safe so the rendered HTML will be output correctly and you do not need to use a `safe` filter for the content template variable.\n\n```html\n{% block content %}{{ content }}{% endblock content %}\n```\n\n### Custom template\n\nSpecify a custom template with a `template` variable in the markdown frontmatter. The specified template context will include variables from the markdown frontmatter, the rendered markdown in `content`, and JSON data in `data`.\n\n#### `index.md`\n\n```markdown\n---\ntitle: This is good content\ntemplate: sample_app/new-template.html\n---\n\n# Heading 1\n\nThis will use sample_app/new-template.html to render content.\n```\n\n#### `sample_app/new-template.html`\n\n```html\n<title>{{ title }}</title>\n\n{{ content }}\n```\n\n#### Generated `index.html`\n\n```html\n<title>This is good content</title>\n\n<h1 id="heading-1">Heading 1</h1>\n\n<p>This will use sample_app/new-template.html to render content.</p>\n```\n\n## Use JSON data\n\n`coltrane` is designed to be used without a database, however, sometimes it\'s useful to have access to data inside your templates.\n\n### JSON data file\n\nCreate a file named `data.json` in your project folder: `touch data.json`. Add whatever data you want to that file and it will be included in the template context.\n\n#### `data.json`\n\n```JSON\n{\n    {"answer": 42}\n}\n```\n\n#### `index.md` file\n\n```markdown\n# index\n\nThe answer to everything is {{ data.answer }}\n```\n\n#### Generated `index.html`\n\n```html\n<h1>index</h1>\n\n<p>The answer to everything is 42</p>\n```\n\n### JSON data directory\n\nCreate a directory named `data` in your project folder: `mkdir data`. Create as many JSON files as you want. The name of the file (without the `json` extension) will be used as the key in the context data.\n\n#### `data/author.json`\n\n```JSON\n{\n    {"name": "Douglas Adams"}\n}\n```\n\n#### `index.md` file\n\n```markdown\n# index\n\n{{ data.author.name }} is the author\n```\n\n#### Generated `index.html`\n\n```html\n<h1>index.md</h1>\n\n<p>Douglas Adams is the author</p>\n```\n\n## Markdown frontmatter\n\nMarkdown frontmatter (i.e. YAML before the actual markdown content) is supported. It will be added to the context variable that is used to render the HTML. The default `base.html` template will use `lang` (to specify the HTML language; defaults to "en"), and `title` variables if they are specified in the frontmatter.\n\n### template\n\nUsed to specify a custom template that Django will use to render the markdown.\n\n## Build static HTML\n\n`coltrane record` will build the static HTML. Coming soon.\n\n## Settings\n\nSettings specified in a `COLTRANE` dictionary.\n\n```python\n# settings.py\n\nCOLTRANE = {\n    VIEW_CACHE_SECONDS=60*60,\n    MARKDOWN_EXTRAS=[\n        "metadata",\n    ]\n}\n```\n\n## VIEW_CACHE_SECONDS\n\nSpecifies how long the markdown should be cached when Django is dynamically serving the markdown.\n\n## MARKDOWN_EXTRAS\n\nThe features that should be enabled when rendering markdown. A list of all available features: https://github.com/trentm/python-markdown2/wiki/Extras. The default extras are:\n\n```python\n[\n    "fenced-code-blocks",\n    "header-ids",\n    "metadata",\n    "strike",\n    "tables",\n    "task_list",\n]\n```\n\n## What\'s with the name?\n\n`coltrane` is built on top of the Django web framework, which is named after [Django Reinhardt](https://en.wikipedia.org/wiki/Django_Reinhardt). Following in that tradition, I named this static site framework after [John Coltrane](https://en.wikipedia.org/wiki/John_Coltrane), another jazz musician.\n\n## Other Python static site builder alternatives\n\n- [Combine](https://combine.dropseed.dev/): uses Jinja templates under the hood\n- [Pelican](https://blog.getpelican.com/)\n- [Nikola](https://getnikola.com/)\n\n## Thanks\n\n- https://twitter.com/willmcgugan/status/1477283879841157123 for the initial inspiration\n- https://github.com/wsvincent/django-microframework for the `app.py` idea\n- https://olifante.blogs.com/covil/2010/04/minimal-django.html\n- https://simonwillison.net/2009/May/19/djng/\n- https://stackoverflow.com/questions/1297873/how-do-i-write-a-single-file-django-application\n- https://github.com/trentm/python-markdown2\n',
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
