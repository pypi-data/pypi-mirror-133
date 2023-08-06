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
    'version': '0.0.8',
    'description': 'Debouncer is a proxy that debounce requests.',
    'long_description': '# Debouncer\n\n`Debouncer` is a proxy that debounce requests.\n\n[![](https://mermaid.ink/svg/eyJjb2RlIjoic3RhdGVEaWFncmFtLXYyXG4gICAgc3RhdGUgXCJSZWNlaXZlZCBhIHJlcXVlc3RcIiBhcyByZWNlaXZlZFxuXG4gICAgWypdIC0tPiByZWNlaXZlZFxuXG4gICAgc3RhdGUgaWZfd2FpdGluZyA8PGNob2ljZT4-XG4gICAgc3RhdGUgXCJEaXNwYXRjaGluZyB0aGUgcmVxdWVzdFwiIGFzIGRpc3BhdGNoaW5nXG4gICAgc3RhdGUgXCJJbmdlc3RpbmcgdGhlIHJlcXVlc3RcIiBhcyBpbmdlc3RpbmdcblxuICAgIHJlY2VpdmVkIC0tPiBpZl93YWl0aW5nOiBJcyBhIHJlcXVlc3QgYWxyZWFkeSB3YWl0aW5nID9cbiAgICBpZl93YWl0aW5nIC0tPiBkaXNwYXRjaGluZzogTm9cbiAgICBpZl93YWl0aW5nIC0tPiBpbmdlc3Rpbmc6IFllc1xuXG4gICAgc3RhdGUgaWZfbG9ja2VkIDw8Y2hvaWNlPj5cbiAgICBzdGF0ZSBcIklnbm9yaW5nXCIgYXMgaWdub3JpbmdcbiAgICBzdGF0ZSBcIk1hcmsgYXMgcmVkaXNwYXRjaGFibGVcIiBhcyBtYXJrX3JlZGlzcGF0Y2hcblxuICAgIGluZ2VzdGluZyAtLT4gaWZfbG9ja2VkOiBJcyB0aGUgcmVxdWVzdCBsb2NrZWQgP1xuICAgIGlmX2xvY2tlZCAtLT4gaWdub3Jpbmc6IE5vXG4gICAgaWZfbG9ja2VkIC0tPiBtYXJrX3JlZGlzcGF0Y2g6IFllc1xuXG4gICAgc3RhdGUgaWZfdGltZW91dCA8PGNob2ljZT4-XG4gICAgc3RhdGUgXCJXYWl0aW5nIHRpbWVvdXRcIiBhcyB3YWl0aW5nXG4gICAgc3RhdGUgXCJDbG9zaW5nIHRoZSByZXF1ZXN0XCIgYXMgY2xvc2luZ1xuXG4gICAgZGlzcGF0Y2hpbmcgLS0-IGlmX3RpbWVvdXQ6IEhhcyB0aGUgcmVxdWVzdCBhIHRpbWVvdXQgPyBcbiAgICBpZl90aW1lb3V0IC0tPiB3YWl0aW5nOiBUaW1lb3V0ID4gMFxuICAgIHdhaXRpbmcgLS0-IGNsb3NpbmdcbiAgICBpZl90aW1lb3V0IC0tPiBjbG9zaW5nXG5cbiAgICBzdGF0ZSBpZl9yZWRpc3BhdGNoYWJsZSA8PGNob2ljZT4-XG4gICAgc3RhdGUgXCJDbG9zZWQgdGhlIHJlcXVlc3RcIiBhcyBjbG9zZWRcbiAgICBzdGF0ZSBcIlJlZGlzcGF0Y2hpbmcgdGhlIHJlcXVlc3RcIiBhcyByZWRpc3BhdGNoaW5nXG5cbiAgICBjbG9zaW5nIC0tPiBpZl9yZWRpc3BhdGNoYWJsZTogSXMgdGhlIHJlcXVlc3QgbWFya2VkIGFzIHJlZGlzcGF0Y2hhYmxlP1xuICAgIGlmX3JlZGlzcGF0Y2hhYmxlIC0tPiBjbG9zZWQ6IE5vXG4gICAgaWZfcmVkaXNwYXRjaGFibGUgLS0-IHJlZGlzcGF0Y2hpbmc6IFllc1xuICAgIHJlZGlzcGF0Y2hpbmcgLS0-IHJlY2VpdmVkXG5cbiAgICBjbG9zZWQgLS0-IFsqXVxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid.live/edit#eyJjb2RlIjoic3RhdGVEaWFncmFtLXYyXG4gICAgc3RhdGUgXCJSZWNlaXZlZCBhIHJlcXVlc3RcIiBhcyByZWNlaXZlZFxuXG4gICAgWypdIC0tPiByZWNlaXZlZFxuXG4gICAgc3RhdGUgaWZfd2FpdGluZyA8PGNob2ljZT4-XG4gICAgc3RhdGUgXCJEaXNwYXRjaGluZyB0aGUgcmVxdWVzdFwiIGFzIGRpc3BhdGNoaW5nXG4gICAgc3RhdGUgXCJJbmdlc3RpbmcgdGhlIHJlcXVlc3RcIiBhcyBpbmdlc3RpbmdcblxuICAgIHJlY2VpdmVkIC0tPiBpZl93YWl0aW5nOiBJcyBhIHJlcXVlc3QgYWxyZWFkeSB3YWl0aW5nID9cbiAgICBpZl93YWl0aW5nIC0tPiBkaXNwYXRjaGluZzogTm9cbiAgICBpZl93YWl0aW5nIC0tPiBpbmdlc3Rpbmc6IFllc1xuXG4gICAgc3RhdGUgaWZfbG9ja2VkIDw8Y2hvaWNlPj5cbiAgICBzdGF0ZSBcIklnbm9yaW5nXCIgYXMgaWdub3JpbmdcbiAgICBzdGF0ZSBcIk1hcmsgYXMgcmVkaXNwYXRjaGFibGVcIiBhcyBtYXJrX3JlZGlzcGF0Y2hcblxuICAgIGluZ2VzdGluZyAtLT4gaWZfbG9ja2VkOiBJcyB0aGUgcmVxdWVzdCBsb2NrZWQgP1xuICAgIGlmX2xvY2tlZCAtLT4gaWdub3Jpbmc6IE5vXG4gICAgaWZfbG9ja2VkIC0tPiBtYXJrX3JlZGlzcGF0Y2g6IFllc1xuXG4gICAgc3RhdGUgaWZfdGltZW91dCA8PGNob2ljZT4-XG4gICAgc3RhdGUgXCJXYWl0aW5nIHRpbWVvdXRcIiBhcyB3YWl0aW5nXG4gICAgc3RhdGUgXCJDbG9zaW5nIHRoZSByZXF1ZXN0XCIgYXMgY2xvc2luZ1xuXG4gICAgZGlzcGF0Y2hpbmcgLS0-IGlmX3RpbWVvdXQ6IEhhcyB0aGUgcmVxdWVzdCBhIHRpbWVvdXQgPyBcbiAgICBpZl90aW1lb3V0IC0tPiB3YWl0aW5nOiBUaW1lb3V0ID4gMFxuICAgIHdhaXRpbmcgLS0-IGNsb3NpbmdcbiAgICBpZl90aW1lb3V0IC0tPiBjbG9zaW5nXG5cbiAgICBzdGF0ZSBpZl9yZWRpc3BhdGNoYWJsZSA8PGNob2ljZT4-XG4gICAgc3RhdGUgXCJDbG9zZWQgdGhlIHJlcXVlc3RcIiBhcyBjbG9zZWRcbiAgICBzdGF0ZSBcIlJlZGlzcGF0Y2hpbmcgdGhlIHJlcXVlc3RcIiBhcyByZWRpc3BhdGNoaW5nXG5cbiAgICBjbG9zaW5nIC0tPiBpZl9yZWRpc3BhdGNoYWJsZTogSXMgdGhlIHJlcXVlc3QgbWFya2VkIGFzIHJlZGlzcGF0Y2hhYmxlP1xuICAgIGlmX3JlZGlzcGF0Y2hhYmxlIC0tPiBjbG9zZWQ6IE5vXG4gICAgaWZfcmVkaXNwYXRjaGFibGUgLS0-IHJlZGlzcGF0Y2hpbmc6IFllc1xuICAgIHJlZGlzcGF0Y2hpbmcgLS0-IHJlY2VpdmVkXG5cbiAgICBjbG9zZWQgLS0-IFsqXVxuIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRlZmF1bHRcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)\n\n## Config\n\nTo configure `Debouncer`, you can set the following environment variables:\n\n```sh\n# Path to the key/value store, default is "debouncer.db"\nSTORE_PATH=your-app.db\n# Port for the http server, default is "4000"\nPORT=8000\n# Credentials for a basic auth or token based authentication, default is not set\nCREDENTIALS={"username": "password"}\n```\n\n# Release\n\nTo release a new version, first bump the version number in `pyproject.toml` by hand or by using:\n\n```sh\n# poetry version --help\npoetry version <patch|minor|major>\n```\n\nMake a release:\n\n```sh\nmake release\n```\n\nFinally, push the release commit and tag to publish them to Pypi:\n\n```sh\ngit push --follow-tags\n```\n',
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
