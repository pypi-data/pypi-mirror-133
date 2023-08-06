# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_databricks']

package_data = \
{'': ['*']}

install_requires = \
['PyHive>=0,<1', 'SQLAlchemy>=1,<2', 'databricks-sql-connector>=0,<1']

entry_points = \
{'sqlalchemy.dialects': ['databricks.connector = '
                         'sqlalchemy_databricks:DatabricksDialect']}

setup_kwargs = {
    'name': 'sqlalchemy-databricks',
    'version': '0.1.0',
    'description': 'SQLAlchemy Dialect for Databricks',
    'long_description': '# sqlalchemy-databricks\n\n![pypi](https://img.shields.io/pypi/v/sqlalchemy-databricks.svg)\n![pyversions](https://img.shields.io/pypi/pyversions/sqlalchemy-databricks.svg)\n\nA SQLAlchemy Dialect for Databricks using the officially supported ``databricks-sql-connector`` dbapi. Compatible with workspace and sql analytics clusters. (Thanks to [@Tom-Newton](https://github.com/Tom-Newton) for pointing this out)\n\n## Installation\n\nInstall using pip.\n\n```bash\npip install sqlalchemy-databricks\n```\n\n## Usage\n\nInstalling registers the ``databricks+connector`` dialect/driver with SQLAlchemy. Fill in the required information when passing the engine URL. The http path can be for either a workspace or sql analytics cluster.\n\n```python\nfrom sqlalchemy import *\nfrom sqlalchemy.engine import create_engine\n\n\nengine = create_engine(\n    "databricks+connector://token:<databricks_token>@<databricks_host>:443/default",\n    connect_args={"http_path": "<cluster_http_path>"}\n)\n\nlogs = Table("my_table", MetaData(bind=engine), autoload=True)\nprint(select([func.count("*")], from_obj=logs).scalar())\n```\n',
    'author': 'flynn',
    'author_email': 'crf204@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/crflynn/sqlalchemy-databricks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
