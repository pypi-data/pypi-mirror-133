# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiontai']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'dataclasses-json>=0.5.6,<0.6.0',
 'injector>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'aiontai',
    'version': '1.0.6',
    'description': 'Async wrapper for nhentai API',
    'long_description': 'Aiontai\n=======\n\nAsync wrapper for nhentai API\n\n\n============\nInstallation\n============\n\n.. code:: shell\n\n    $ pip install git+https://github.com/LEv145/aiontai\n\n\n==========\nHow to use\n==========\n\n\nCreate client\n\n.. code:: python\n\n    import asyncio\n\n    from aiohttp import ClientSession\n\n    from aiontai import (\n        NHentaiClient,\n        NHentaiAPI,\n        Conventer,\n    )\n\n\n    async def main():\n        client_object = NHentaiClient(\n            api=NHentaiAPI(\n                ClientSession(),\n            ),\n            conventer=Conventer(),\n        )\n\n    asyncio.run(main())\n\n\nOr can use ``injector`` that will create the object itself (Next examples will be using it)\n\n.. code:: python\n\n    import asyncio\n\n    from injector import Injector\n\n    from aiontai import (\n        NHentaiClient,\n        ClientModule,\n    )\n\n\n    async def main():\n        injector = Injector(ClientModule())\n        client_object = injector.get(NHentaiClient)\n\n    asyncio.run(main())\n\n\nExample of using the client\n\n.. code:: python\n\n    async def main():\n        injector = Injector(ClientModule())\n        client_object = injector.get(NHentaiClient)\n\n        async with client_object as client:  # Will close the session itself\n            doujin = await client.get_random_doujin()\n\n            for page in doujin.images:\n                print(page.url)\n\n            print(doujin.to_json())\n\n    asyncio.run(main())\n\n\nExample of using the proxy\n\n.. code:: python\n\n    ...\n    from injector import (\n        provider,\n        Injector,\n        Module,\n    )\n    from aiohttp_proxy import ProxyConnector  # pip install aiohttp_proxy\n    ...\n\n    class AiohttpProxyModule(Module):\n        def __init__(self, proxi_url: str) -> None:\n            self._proxi_url = proxi_url\n\n        @provider\n        def provide_client_session(self) -> ClientSession:\n            connector = ProxyConnector.from_url(self._proxi_url)\n            return ClientSession(connector=connector)\n\n\n    async def main():\n        injector = Injector(\n            modules=[\n                ClientModule(),\n                AiohttpProxyModule("http://user:password@127.0.0.1:1080"),\n            ],\n        )\n        client_object = injector.get(NHentaiClient)\n\n    asyncio.run(main())\n\n\nExample of using the Low level api\n\n.. code:: python\n\n    async def main():\n        injector = Injector(ClientModule())\n        client_object = injector.get(NHentaiAPI)\n        async with client_object as client:\n            doujin = await client.get_random_doujin()  # Return: Dict[str, Any]\n                                                       # from api without loss of information\n\n            print(doujin)\n\n\n    asyncio.run(main())\n',
    'author': 'LEv145',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LEv145/aiontai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
