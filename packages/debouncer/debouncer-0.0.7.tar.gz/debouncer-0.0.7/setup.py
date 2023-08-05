# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['debouncer']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.1,<0.71.0',
 'httpx>=0.21.1,<0.22.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.2,<2.0.0',
 'sqlitedict>=1.7.0,<2.0.0',
 'uvicorn>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'debouncer',
    'version': '0.0.7',
    'description': 'Debouncer is a proxy that debounce requests.',
    'long_description': '# Debouncer\n\n`Debouncer` is a proxy that debounce requests.\n\n[![](https://mermaid.ink/svg/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgcGFydGljaXBhbnQgYyBhcyBDbGllbnRcbiAgICBwYXJ0aWNpcGFudCBmIGFzIEZ1bm5lbFxuICAgIHBhcnRpY2lwYW50IHMgYXMgU2VydmVyXG5cbiAgICBjLT4-ZjogTmV3IHJlcXVlc3RcbiAgICBhY3RpdmF0ZSBmXG5cbiAgICBmLT4-czogRGlzcGF0Y2ggcmVxdWVzdFxuICAgIFxuICAgIGFsdCB3aGVuIFRpbWVvdXQgPiAwXG4gICAgICAgIGYtPj5mOiBXYWl0IHJlcXVlc3QgdGltZW91dFxuICAgICAgICBjLS0-PmY6IDJuZCByZXF1ZXN0IChpZ25vcmVkIHdoZW4gdGltZW91dCBub3QgZWxhcHNlZClcbiAgICBlbHNlIHdoZW4gZm9yY2luZyByZXF1ZXN0IGRlbGV0aW9uIFxuICAgICAgICBzLT4-ZjogRm9yY2UgZGVsZXRlIHJlcXVlc3RcbiAgICBlbmRcblxuICAgIGYtPj5mOiBEZWxldGUgcmVxdWVzdFxuXG4gICAgZGVhY3RpdmF0ZSBmXG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid.live/edit/#eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgcGFydGljaXBhbnQgYyBhcyBDbGllbnRcbiAgICBwYXJ0aWNpcGFudCBmIGFzIEZ1bm5lbFxuICAgIHBhcnRpY2lwYW50IHMgYXMgU2VydmVyXG5cbiAgICBjLT4-ZjogTmV3IHJlcXVlc3RcbiAgICBhY3RpdmF0ZSBmXG5cbiAgICBmLT4-czogRGlzcGF0Y2ggcmVxdWVzdFxuICAgIFxuICAgIGFsdCB3aGVuIFRpbWVvdXQgPiAwXG4gICAgICAgIGYtPj5mOiBXYWl0IHJlcXVlc3QgdGltZW91dFxuICAgICAgICBjLS0-PmY6IDJuZCByZXF1ZXN0IChpZ25vcmVkIHdoZW4gdGltZW91dCBub3QgZWxhcHNlZClcbiAgICBlbHNlIHdoZW4gZm9yY2luZyByZXF1ZXN0IGRlbGV0aW9uIFxuICAgICAgICBzLT4-ZjogRm9yY2UgZGVsZXRlIHJlcXVlc3RcbiAgICBlbmRcblxuICAgIGYtPj5mOiBEZWxldGUgcmVxdWVzdFxuXG4gICAgZGVhY3RpdmF0ZSBmXG4iLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGVmYXVsdFwiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)\n\n## Config\n\nTo configure `Debouncer`, you can set the following environment variables:\n\n```sh\n# Path to the key/value store, default is "debouncer.db"\nSTORE_PATH=your-app.db\n# Port for the http server, default is "4000"\nPORT=8000\n# Auth key for a key based auth, default is not set\nAUTH_KEY=your-secret-auth-key\n```\n\n# Release\n\nTo release a new version, first bump the version number in `pyproject.toml` by hand or by using:\n\n```sh\n# poetry version --help\npoetry version <patch|minor|major>\n```\n\nMake a release:\n\n```sh\nmake release\n```\n\nFinally, push the release commit and tag to publish them to Pypi:\n\n```sh\ngit push --follow-tags\n```\n',
    'author': 'Joola',
    'author_email': 'jooola@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
