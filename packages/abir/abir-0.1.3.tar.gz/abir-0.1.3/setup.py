# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abir']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'abir',
    'version': '0.1.3',
    'description': 'python project load config from yaml or environment.',
    'long_description': "# Abir--Python项目配置读取方案，yaml/environ\n\n## 安装\n```shell\npip install abir\n```\n\n## 快速上手\n#### django project\n\n1. 在 `settings.py` 底部添加\n\n```python\nimport abir  # at the top of settings.py\n\n# another settings\n\nabir.load()\n```\n\n2. 在项目首页添加`configure.yaml`\n```yaml\nDATABASES.default.ENGINE: 'django.db.backends.postgresql'\nDATABASES.default.NAME: 'db_name'\nCACHE:\n  default:\n    BACKEND: 'django_redis.cache.RedisCache'\n    LOCATION: 'redis://127.0.0.1:6379/1'\n    OPTIONS:\n      CLIENT_CLASS: 'django_redis.client.DefaultClient'\nLANGUAGE_CODE: 'zh-CN'\nUSE_TZ: true\nALLOWED_HOSTS:\n  - *\n```\n⚠️ 注意：dot`.`将会查询`settings.py`，并更新查询路径下的值。 \n\n3. 启动服务。\n```shell\npython manmage.py runserver\n# or wsgi\n```\n\n## environment\n```shell\nABIR_USE_TZ:json=false\nABIR_LANGUAGE_CODE=es-us\n```\n",
    'author': 'Jone',
    'author_email': 'zjhjin@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MattiooFR/package_name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
