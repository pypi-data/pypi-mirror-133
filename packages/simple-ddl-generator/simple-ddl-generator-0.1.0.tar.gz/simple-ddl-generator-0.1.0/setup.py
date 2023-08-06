# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_ddl_generator']

package_data = \
{'': ['*'], 'simple_ddl_generator': ['templates/*']}

install_requires = \
['jinja2>=3.0.3,<4.0.0', 'table-meta>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'simple-ddl-generator',
    'version': '0.1.0',
    'description': 'Library to generate DDL for different dialects',
    'long_description': '\nSimple DDL Generator\n--------------------\n\n\n.. image:: https://img.shields.io/pypi/v/simple-ddl-generator\n   :target: https://img.shields.io/pypi/v/simple-ddl-generator\n   :alt: badge1\n \n.. image:: https://img.shields.io/pypi/l/simple-ddl-generator\n   :target: https://img.shields.io/pypi/l/simple-ddl-generator\n   :alt: badge2\n \n.. image:: https://img.shields.io/pypi/pyversions/simple-ddl-generator\n   :target: https://img.shields.io/pypi/pyversions/simple-ddl-generator\n   :alt: badge3\n \n.. image:: https://github.com/xnuinside/simple-ddl-generator/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/xnuinside/simple-ddl-generator/actions/workflows/main.yml/badge.svg\n   :alt: workflow\n\n\nWhat is it?\n-----------\n\nSimple DDL Generator generate SQL DDL from 3 different inputs. Idea of the generator same as for parser to support as much as possible DDLs in future.\n\nSimple DDL Generator generate SQL DDL from 3 input formats - 1st from output Simple DDL Parser (https://github.com/xnuinside/simple-ddl-parser), 2nd from py-models-parser - https://github.com/xnuinside/py-models-parser. Or you can directly pass TableMeta classes (https://github.com/xnuinside/table-meta) to generator\n\nHow to use\n----------\n\nAs usually - more samples in tests/ \n\n.. code-block:: bash\n\n\n       pip install simple-ddl-generator\n\n.. code-block:: python\n\n\n       from simple_ddl_generator import DDLGenerator\n       from simple_ddl_parser import DDLParser\n\n       # take initial DDL\n       ddl = """CREATE EXTERNAL TABLE IF NOT EXISTS database.table_name\n           (\n               day_long_nm     string,\n               calendar_dt     date,\n               source_batch_id string,\n               field_qty       decimal(10, 0),\n               field_bool      boolean,\n               field_float     float,\n               create_tmst     timestamp,\n               field_double    double,\n               field_long      bigint\n           ) PARTITIONED BY (batch_id int);"""\n       # get result from parser\n       data = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")\n\n       # rename, for example, table name\n\n       data["tables"][0]["table_name"] = "new_table_name"\n       g = DDLGenerator(data)\n       g.generate()\n       print(g.result)\n\n       # and result will be:\n\n       """\n       CREATE EXTERNAL TABLE "database.new_table_name" (\n       day_long_nm string,\n       calendar_dt date,\n       source_batch_id string,\n       field_qty decimal(10, 0),\n       field_bool boolean,\n       field_float float,\n       create_tmst timestamp,\n       field_double double,\n       field_long bigint)\n       PARTITIONED BY (batch_id int);\n       """\n\nChangelog\n---------\n\n**v0.1.0**\n\nBase Generator Functionality with several test cases.\n',
    'author': 'Iuliia Volkova',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
