# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbd',
 'dbd.cli',
 'dbd.config',
 'dbd.db',
 'dbd.executors',
 'dbd.generator',
 'dbd.log',
 'dbd.tasks',
 'dbd.utils']

package_data = \
{'': ['*'],
 'dbd': ['resources/template/*', 'resources/template/model/*'],
 'dbd.generator': ['generator_templates/*']}

install_requires = \
['cerberus>=1.3.4,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'jinja2>=3.0.3,<4.0.0',
 'networkx>=2.6.3,<3.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'psycopg2>=2.9.3,<3.0.0',
 'pyarrow>=6.0.0,<7.0.0',
 'pyyaml>=6.0,<7.0',
 'sql-metadata>=2.3.0,<3.0.0',
 'sqlalchemy>=1.4.29,<2.0.0',
 'sqlparse>=0.4.2,<0.5.0']

entry_points = \
{'console_scripts': ['dbd = dbd.cli.dbdcli:cli']}

setup_kwargs = {
    'name': 'dbd',
    'version': '0.5.5',
    'description': 'Framework for declarative database creation and management.',
    'long_description': "# DBD - framework for declarative database definition\nDBD framework allows you to define your database schema and content \ndeclaratively. Database is represented by a hierarchy of directories and\nfiles stored in your DBD project files. \n\n## TLDR: Whetting Your Appetite\n\n1. `dbd init test`\n2. `cd test`\n3. `dbd validate .`\n4. `dbd run .`\n5. Connect to the newly created `states.db` database and review `area`, `population`, and `state` tables that have been created from the files in the `model` directory.\n\nNow you can delete the example files from the `model` directory, copy your Excel, JSON, or CSV files there instead. \nThen execute `dbd run .` again. Your files should get loaded into the database.\n\nYou can create a YAML configuration files for your Excel, JSON, or CSV files to specify individual column's\ndata types, indexes or constraints (e.g. primary key, foreign key, or check). See below for more details. \n\nThen you can also create an SQL file that performs SQL insert-from-select to transform the loaded data.\n\n## Install DBD\nDBD requires Python 3.7.1 or higher. \n\n### PyPI\n\n```shell\npip3 install dbd\n```\n\nOR\n\n```shell\ngit clone https://github.com/zsvoboda/dbd.git\ncd dbd\npip3 install .\n```\n\n### Poetry\n\n```shell\ngit clone https://github.com/zsvoboda/dbd.git\ncd dbd\npoetry install\n``` \n\n## Generate a new DBD project\nYou can generate initial layout of your DBD project using the `init` command:\n\n```shell\ndbd init <new-project-name>\n```\n\nThe `init` command generates a new DBD project directory with the following content: \n\n- `model` directory that contains the content files. dbd supports files with `.sql`, `.ddl`, `.csv`, `.json`, `.xlsx` and other extensions.  \n- `dbd.project` project configuration file \n\nDBD also requires `dbd.profile` configuration file that contains connections to your databases. \nThis file is located in the current directory or in your home directory.  \n\n## DBD profile configuration file\nDBD stores database connections in a profile configuration file. It searches for `dbd.profile` file in the current or in \nyour home directory. You can always specify a custom profile file location using the `--profile` option of the `dbd` command. \n\nThe profile file is YAML file with the following structure:\n\n```yaml\ndatabases:\n  states:\n    db.url: <sql-alchemy-database-url>\n```\n\nRead more about [SQL Alchemy database URLs here](https://docs.sqlalchemy.org/en/14/core/engines.html). \n\nThe profile file can contain Jinja2 macros that substitute your environment variables. For example, you can reference \ndatabase password stored in a `$SQLITE_PASSWORD` environment variable via `{{ SQLITE_PASSWORD }}` in your DBD profile.\n\n## DBD project configuration file\nDBD stores project configuration in a project configuration file that is usually stored in your DBD project directory. \nDBD searches for `dbd.project` file in the current directory. You can also use the `--project` option pf the `dbd` \ncommand to specify a custom project configuration file. \n\nThe project configuration file also uses YAML format and references the DBD model directory with the `.sql`, `.csv` \nand other supported files. It also references the database configuration from the profile config file. For example:\n\n```yaml\nmodel: model\ndatabase: states\n```\n\nSimilarly like the profile file, you can use the environment variables substitution in the procet config file too \n(e.g. `{{ SQLITE_DB_NAME }}`).\n\n## Model directory\nThe model directory contains directories and DBD files. Each subdirectory of the model directory represents \na database schema. For example, this model directory structure\n\n```text\ndbd-project-directory\n+- schema1\n +-- us_states.csv\n+- schema2\n +-- us_counties.csv\n```\n\ncreates two database schemas: `schema1` and `schema2` and creates two database tables: `us_states` in `schema1` \nand `us_counties` in `schema2`. Both tables are populated with the data from the CSV files.  \n\nThe following file types are supported:\n\n* __DATA files:__ `.csv`, `.json`, `.xls`, `.xlsx`, `.parquet` files are loaded to the database as tables\n* __SQL files:__ with SQL SELECT statements are executed using insert-from-select SQL construct. The INSERT command is generated (the SQL file only contains the SQL SELECT statement)\n* __DDL files:__ contain a sequence of SQL statements separated by semicolon. The DDL files can be named `prolog.ddl` and `epilog.ddl`. The `prolog.ddl` is executed before all other files in a specific schema. The `epilog.ddl` is executed last. The `prolog.ddl` and `epilog.ddl` in the top-level model directory are executed as the very first and tne very last files in the model. \n* __YAML files:__ specify additional configuration to the __DATA__ and __SQL__ files. \n\n## YAML model files\nYAML file specify additional configuration for a corresponding __DATA__ or __SQL__ file with the same base file name.\nhere is an `area.csv` YAML configuration example:\n\n```yaml\ntable:\n  columns:\n    state_name:\n      nullable: false\n      index: true\n      primary_key: true\n      foreign_keys:\n        - state.state_name\n      type: VARCHAR(50)\n    area_sq_mi:\n      nullable: false\n      index: true\n      type: INTEGER\nprocess:\n  materialization: table\n  mode: drop\n```\n\n### Process section\nThe `process` section specifies the following processing options:\n\n* __materialization:__ specifies whether DBD creates a physical `table` or a `view` when processing a SQL file.\n* __mode:__ specifies how DBD works with a table. You can specify values `drop`, `truncate`, or `keep`. The  __mode__ option is ignored for views.\n\n### Table section\nYAML file's columns are mapped to the `area.csv` data file columns by the column name. \nThe following column parameters are supported:\n\n* __type:__ column's SQL type.\n* __primary_key:__ is the column part of table's primary key (true|false)?\n* __foreign_keys:__ all other database table columns that are referenced from a column in <table>.<column> format\n* __nullable:__ does column allow null values (true|false)?\n* __index:__ is column indexed (true|false)?\n* __unique:__ does column store unique values (true|false)?\n",
    'author': 'zsvoboda',
    'author_email': 'zsvoboda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zsvoboda/dbd/blob/master/README.md',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
