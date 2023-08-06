# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envolved']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'envolved',
    'version': '0.5.0',
    'description': '',
    'long_description': '# Envolved\nEnvolved is a library to make environment variable parsing powerful and effortless.\n\n```python\nfrom envolved import env_var, EnvVar\n\n# create an env var with an int value\nfoo: EnvVar[int] = env_var(\'FOO\', type=int, default=0)\nvalue_of_foo = foo.get()  # this method will check for the environment variable FOO, and parse it as an int\n\n# we can also have some more complex parsers\nfrom typing import List, Optional\nfrom envolved.parsers import CollectionParser\n\nfoo = EnvVar(\'FOO\', type=CollectionParser(\',\', int))\nfoo.get()  # now we will parse the value of FOO as a comma-separated list of ints\n\n# we can also use schemas to combine multiple environment variables\nfrom dataclasses import dataclass\n\n\n@dataclass\n# say we want the environment to describe a ConnectionSetting\nclass ConnectionSetting:\n    host: str\n    port: int\n    user: Optional[str]\n    password: Optional[str]\n\n\nconnection_settings: EnvVar[ConnectionSetting] = env_var(\'service_\', type=ConnectionSetting, args={\n    \'host\': env_var(\'hostname\'),\n    # we now define an env var as an argument. Its suffix will be "hostname", and its type will be inferred from the\n    # type\'s annotation\n    \'port\': env_var(\'port\'),\n    \'user\': env_var(\'username\', type=str),  # for most types, we can infer the type from the annotation, though we can\n    # also override it if we want\n    \'password\': env_var(\'password\', type=str, default=None)  # we can also set a default value per arg\n})\nservice_connection_settings: ConnectionSetting = connection_settings.get()\n# this will look in 4 environment variables:\n# host will be extracted from service_hostname\n# port will be extracted from service_port, then converted to an int\n# user will be extracted from service_username\n# password will be extracted from service_password, and will default to None\n# finally, ConnectionSetting will be called with the parameters\n```\n',
    'author': 'ben avrahami',
    'author_email': 'avrahami.ben@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bentheiii/envolved',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
