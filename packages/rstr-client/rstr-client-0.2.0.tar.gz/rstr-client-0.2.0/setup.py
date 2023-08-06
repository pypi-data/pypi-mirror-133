# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rstr']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'rstr-client',
    'version': '0.2.0',
    'description': 'A client for the rstr blob-store.',
    'long_description': '# rstr-client\n\nA lightweight `python` API client for the [`rstr`](https://github.com/giuppep/rstr) blob store.\n\n## Installation\n\nYou can install the `rstr-client` library with `pip`\n\n```\npip install rstr-client\n```\n\n## Usage\n\n```python\nfrom rstr import Rstr\n\n# Initialise the rstr client with the URL to your rstr server\n# and your API Token.\n# NOTE: these can be specified as environment variables\n# >>> export RSTR_URL="https://my-rstr.rs"\n# >>> export RSTR_TOKEN="MY_API_TOKEN"\nurl = "https://my-rstr.rs"\ntoken = "MY_API_TOKEN"\n\nwith Rstr(url=url, token=token) as rstr:\n    # Add a file to the blob store\n    refs = rstr.add(["/path/to/my/file.txt"])\n\n    # You will get a list of references to your blobs\n    # e.g. ["f29bc64a9d3732b4b9035125fdb3285f5b6455778edca72414671e0ca3b2e0de"]\n\n    # You can then use the reference to retrieve your blob\n    ref = refs[0]\n    blob = rstr.get(ref)\n\nprint(blob)\n# Blob(f29bc64a9d)\n\nprint(blob.metadata)\n# BlobMetadata(\'file.txt\', \'text/plain\', 20 bytes)\n\n# You can access the binary content of the blob with:\n# content = blob.content\n\n# The blob can be permanently deleted from the blob store with:\nwith Rstr(url=url, token=token) as rstr:\n    rstr.delete(ref)\n```\n\n## License\n\nCopyright (c) 2021 giuppep\n\n`rstr-client` is made available under the [MIT License](LICENSE)',
    'author': 'Giuseppe Papallo',
    'author_email': 'giuseppe@papallo.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giuppep/rstr-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
