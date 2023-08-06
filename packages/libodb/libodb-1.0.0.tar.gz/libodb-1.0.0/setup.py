# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libodb']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'libodb',
    'version': '1.0.0',
    'description': 'A client library for accessing the OpenDiscordBots API',
    'long_description': '# libodb\n\nA client library for accessing the OpenDiscordBots API\n\n## Example Usage\n\n```py\nfrom asyncio import run\n\nfrom libodb import APIClient\nfrom pydantic import BaseModel\n\n\nclass GuildConfig(BaseModel):\n    test: str\n\n\nasync def main():\n    c = APIClient("api_key")\n\n    await c.kv_set("abc", "123")\n    print(await c.kv_get("abc"))\n\n    await c.set_guild_config(1234, "example", GuildConfig(test="test"))\n    print(await c.get_guild_config(1234, "example", GuildConfig))\n\n    await c.close()\n\nrun(main())\n```\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OpenDiscordBots/libodb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
