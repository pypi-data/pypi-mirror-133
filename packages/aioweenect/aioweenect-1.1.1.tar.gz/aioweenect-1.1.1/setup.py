# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioweenect']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aioweenect',
    'version': '1.1.1',
    'description': 'Asynchronous Python client for the weenect API',
    'long_description': '# aioweenect\n\nAsynchronous Python client for the weenect API\n\n[![GitHub Actions](https://github.com/eifinger/aioweenect/workflows/CI/badge.svg)](https://github.com/eifinger/aioweenect/actions?workflow=CI)\n[![PyPi](https://img.shields.io/pypi/v/aioweenect.svg)](https://pypi.python.org/pypi/aioweenect)\n[![PyPi](https://img.shields.io/pypi/l/aioweenect.svg)](https://github.com/eifinger/aioweenect/blob/master/LICENSE)\n[![codecov](https://codecov.io/gh/eifinger/aioweenect/branch/master/graph/badge.svg)](https://codecov.io/gh/eifinger/aioweenect)\n[![Downloads](https://pepy.tech/badge/aioweenect)](https://pepy.tech/project/aioweenect)\n\n## Installation\n\n```bash\n$ pip install aioweenect\n```\n\n## Usage\n\n```python\nfrom aioweenect import AioWeenect\n\nimport asyncio\n\nUSER = "<YOUR_USER>"\nPASSWORD = "<YOUR_PASSWORD>"\n\n\nasync def main():\n    """Show example how to get location of your tracker."""\n    async with AioWeenect(username=USER, password=PASSWORD) as aioweenect:\n        trackers_response = await aioweenect.get_trackers()\n        tracker_id = trackers_response["items"][0]["id"]\n        tracker_name = trackers_response["items"][0]["name"]\n\n        position_response = await aioweenect.get_position(tracker_id=tracker_id)\n        lat = position_response[0]["latitude"]\n        lon = position_response[0]["longitude"]\n        last_message = position_response[0]["last_message"]\n        print(\n            f"Location for {tracker_name}: lat: {lat}, lon: {lon}. Last message received: {last_message}"\n        )\n\n\nif __name__ == "__main__":\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(main())\n```\n',
    'author': 'Kevin Stillhammer',
    'author_email': 'kevin.stillhammer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/eifinger/aioweenect',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
