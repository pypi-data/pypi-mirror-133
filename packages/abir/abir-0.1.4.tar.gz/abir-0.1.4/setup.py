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
    'version': '0.1.4',
    'description': 'python project load config from yaml and environment.',
    'long_description': '# Abir--Python项目配置方案 yaml/environ\n\n## 安装\n```shell\npip install abir\n```\n\n## 快速上手\n#### django project\n\n1. 在 `settings.py` 中添加\n\n```python\nimport abir  \n\n# other settings\n\nabir.load() # at the end of settings.py\n```\n\n2. 在项目根文件夹下添加`config.yaml`\n\n添加后的项目结构如下：\n\n```shell\n├── project\n│\xa0\xa0 ├── project\n│\xa0\xa0 |   ├── __init__.py\n│\xa0\xa0 |   ├── asgi.py\n│\xa0\xa0 |   ├── wsgi.py\n│\xa0\xa0 |   ├── urls.py\n│\xa0\xa0 |   ├── settings.py\n│\xa0\xa0 ├── manange.py\n│\xa0\xa0 ├── config.yaml  # 添加到根下\n```\n\n在yaml中添加对应的配置项\n\n```yaml\n# settings 中已配置，只希望修改部分配置项时，使用 dot 查询并修改：\nDATABASES.default.NAME: \'db_name\'\nDATABASES.default.HOST: \'dh_host\'  # 未配置时，会添加配置项\nDATABASES.default.PORT: \'port\'\nDATABASES.default.USER: \'db_user_name\'\nDATABASES.default.PASSWORD: \'db_password\'\n\n# settings中无配置，或已配置，但希望全部替换，不使用 dot 查询：\nCACHE: \n  default:\n    BACKEND: \'django_redis.cache.RedisCache\'\n    LOCATION: \'redis://127.0.0.1:6379/1\'\n    OPTIONS:\n      CLIENT_CLASS: \'django_redis.client.DefaultClient\'\nLANGUAGE_CODE: \'zh-CN\'\nUSE_TZ: true\nALLOWED_HOSTS:\n  - *\n\n```\n⚠️ dot`.`将会查询`settings.py`，并更新查询路径下的值。 \n\n3. 启动服务。\n```shell\npython manmage.py runserver\n# or wsgi\n```\n\n\n\n#### 其他python项目\n\n假设项目结构如下：\n\n```shell\n├── project\n│\xa0\xa0 ├── packagges\n│\xa0\xa0 ├── modules \n…… \n```\n\n1. 添加config_module.py (module名称可自定义)\n\n   如下添加代码\n\n   ```python\n   import abir\n   abir.load(base_dir=BASE_DIR, conf_module=\'conf_module\')  \n   # 如果config_module不在根下，输入完整查询路径即可，如：project.packageA.moduleB\n   # confi_module 也可以是任何可设置property的对象：getattr and setattr\n   ```\n\n   \n\n2. 添加config.yaml\n\n   添加后的项目结构如下：\n\n   ```shell\n   ├── project\n   │\xa0\xa0 ├── config_module.py\n   │\xa0\xa0 ├── config.yaml # 添加到根下\n   ```\n\n3. 执行应用，即可获取配置\n\n   \n\n## environment 通过环境变量来进行配置\n\n⚠️ 环境变量拥有最高优先级：当yaml/settings中存在配置，且环境变量中也存在，优先取环境变量的配置值，即：`environ > yaml > settings`（当`load()`在conf_module末尾调用时）\n\n### 前缀\n\nabir通过前缀 `ABIR_`捕获环境变量。\n\n##### 1. 字符串类型\n\n```shell\nABIR_LANGUAGE_CODE=es-us\n```\n\n##### 2. 其他类型\n\nabir读取环境变量时，会识别 `:`定义，当定义为 :json ，将运行 `json.loads`进行值转换，因此可以通过赋值环境变量为json-string的方式，来满足非字符串类型的配置\n\n```shell\nABIR_LANGUAGE_CODE=zh-CN\nABIR_USE_TZ:json=false\nABIR_TIMEOUT:json=20\nABIR_BLACK_UIDS:json=[101,39,847,11]\nABIR_LIFETIME:json={"days": 1, "key": "some-key"}  # 注意 json-string 与 前端书写json的区别。\n```\n\n以上配置，将会被abir解读为：\n\n```python\nLANGUAGE_CODE=\'zh-CN\'\nUSE_TZ=False\nTIMEOUT=20\nBLACK_UIDS=[101,39,847,11]\nLIFETIME={\'days\': 1, \'key\': \'some-key\'}\n```\n\n',
    'author': 'Jone',
    'author_email': 'zjhjin@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jioone/abir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
