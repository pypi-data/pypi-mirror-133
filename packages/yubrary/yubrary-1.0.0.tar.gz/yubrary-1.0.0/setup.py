# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yubrary']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.0,<3.0.0']

setup_kwargs = {
    'name': 'yubrary',
    'version': '1.0.0',
    'description': 'yuuta_library',
    'long_description': '# yubrary\nyu_requests()\n  入力\n  第一引数 URL 第二引数 cookie(なくてもいい)\n  出力\n  URLを投げるとBeautifulSoupに入れるテキスト\n  別のページに飛ばされていないかをbool型(True=飛ばされていない)\n  cookieを返す\n\n\n',
    'author': 'YAMASHITA Yuta',
    'author_email': 'proyuuta0618188188@gmail.com',
    'maintainer': 'YAMASHITA Yuta',
    'maintainer_email': 'proyuuta0618188188@gmail.com',
    'url': 'https://github.com/funnelyuuta/yubrary',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
