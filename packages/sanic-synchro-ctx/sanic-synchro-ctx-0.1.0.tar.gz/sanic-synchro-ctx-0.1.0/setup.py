# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benchmarks', 'examples', 'sanic_synchro_ctx', 'test']

package_data = \
{'': ['*']}

install_requires = \
['sanic>=21.9.3']

extras_require = \
{'redis': ['aioredis[hiredis]>=2.0.1', 'hiredis>=1.0.0']}

setup_kwargs = {
    'name': 'sanic-synchro-ctx',
    'version': '0.1.0',
    'description': 'Synchronize Sanic contects between instances when using multiple workers',
    'long_description': '\n# Sanic-Synchro-Ctx\nPlugin to provide an App context that is shared across multiple workers\n\nCan use native python SyncManager backend, or Redis if you want. (Redis is much faster).\n\n## Installation\n```bash\n$ pip3 install sanic-synchro-ctx\n```\n\nOr in a python virtualenv _(these example commandline instructions are for a Linux/Unix based OS)_\n```bash\n$ python3 -m virtualenv --python=python3 --no-site-packages .venv\n$ source ./.venv/bin/activate\n$ pip3 install sanic sanic-synchro-ctx\n```\n\nTo exit the virtual enviornment:\n```bash\n$ deactivate\n```\n\n## Redis Extension\nYou can install the relevant Redis libraries for this plugin, with the installable redis extension:\n```bash\n$ pip3 install sanic-synchro-ctx[redis]\n```\nThat is the same as running:\n```bash\n$ pip3 install "sanic-synchro-ctx" "aioredis>=2.0" "hiredis>=1.0"\n```\n\n## Compatibility\n* Works with Python 3.8 and greater.\n* Works with Sanic v21.9.0 and greater.\n* If you are installing the redis library separately, use aioredis >= 2.0\n\n\n## Usage\nA very simple example, it uses the native python SyncManager backend, doesn\'t require a Redis connection.\n```python3\nfrom sanic_synchro_ctx import SanicSynchroCtx\napp = Sanic("sample")\ns = SanicSynchroCtx(app)\n\n@app.after_server_start\ndef handler(app, loop=None):\n    # This will only set this value if it doesn\'t already exist\n    # So only the first worker will set this value\n    app.ctx.synchro.set_default({"counter": 0})\n\n@app.route("/inc")\ndef increment(request: Request):\n    # atomic increment operation\n    counter = request.app.ctx.synchro.increment("counter")\n    print("counter: {}".format(counter), flush=True)\n    return html("<p>Incremented!</p>")\n\n@app.route("/count")\ndef increment(request: Request):\n    # Get from shared context:\n    counter = request.app.ctx.synchro.counter\n    print("counter: {}".format(counter), flush=True)\n    return html(f"<p>count: {counter}</p>")\n\napp.run("127.0.0.1", port=8000, workers=8)\n```\n\nRedis example:\n```python3\nfrom sanic_synchro_ctx import SanicSynchroCtx\nredis = aioredis.from_url("redis://localhost")\napp = Sanic("sample")\ns = SanicSynchroCtx(app, backend="redis", redis_client=redis)\n\n@app.after_server_start\nasync def handler(app, loop=None):\n    # This will only set this value if it doesn\'t already exist\n    # So only the first worker will set this value\n    await app.ctx.synchro.set_default({"counter": 0})\n\n@app.route("/inc")\nasync def increment(request: Request):\n    # atomic increment operation\n    counter = await request.app.ctx.synchro.increment("counter")\n    print(f"counter: {counter}", flush=True)\n    return html("<p>Incremented!</p>")\n\n@app.route("/count")\nasync def increment(request: Request):\n    # Get from shared context:\n    counter = await request.app.ctx.synchro.counter\n    print(f"counter: {counter}", flush=True)\n    return html(f"<p>count: {counter}</p>")\n\napp.run("127.0.0.1", port=8000, workers=8)\n```\n\n\n## Changelog\nA comprehensive changelog is kept in the [CHANGELOG file](https://github.com/ashleysommer/sanic-synchro-ctx/blob/master/CHANGELOG.md).\n\n\n## Benchmarks\nI\'ve done some basic benchmarks. SyncManager works surprisingly well, but Redis backend is much faster. \n\n\n## License\nThis repository is licensed under the MIT License. See the [LICENSE deed](https://github.com/ashleysommer/sanic-synchro-ctx/blob/master/LICENSE.txt) for details.\n\n',
    'author': 'Ashley Sommer',
    'author_email': 'ashleysommer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ashleysommer/sanic-synchro-ctx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
