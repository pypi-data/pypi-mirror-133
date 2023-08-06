# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csql',
 'csql._',
 'csql._.cacher',
 'csql._.input',
 'csql._.models',
 'csql._.renderer',
 'csql.contrib.render.param',
 'csql.render']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['Sphinx[docs]>=4.3.1,<5.0.0',
          'sphinx-autobuild[docs]>=2021.3.14,<2022.0.0',
          'sphinx-rtd-theme[docs]>=1.0.0,<2.0.0'],
 'notebooks': ['openpyxl>=3.0.9,<4.0.0',
               'duckdb>=0.3.1,<0.4.0',
               'ipykernel>=6.6.0,<7.0.0'],
 'pandas': ['pandas>=1.3.4,<2.0.0']}

setup_kwargs = {
    'name': 'csql',
    'version': '0.9.0a12',
    'description': 'Simple library for writing composeable SQL queries',
    'long_description': '# csql - Composeable SQL\n\n**csql** is a Python library to help you write more manageable SQL queries. You can write your queries as small, self-contained chunks, preview the results without pulling a whole result-set down from your database, then refer to them in future queries.\n\nThere are also useful features for handling database parameters properly.\n\nThe intended use-case is for data analysis and exploration.\n\n[![PyPI version](https://badge.fury.io/py/csql.svg)](https://pypi.org/project/csql/)\n\n## Example:\n\n```py\nfrom csql import Q, Parameters\nimport pandas as pd\nfrom datetime import date\n\ncon = your_database_connection()\n```\n\nStart with a straightforward query:\n```py\np = Parameters(\n\tcreated_on = date(2020,1,1)\n)\nq1 = Q(f"""\nselect\n\tcustomers.id,\n\tfirst(customers.name) as name,\n\tfirst(created_on) as created_on,\n\tsum(sales.value) as sales\nfrom\n\tcustomers\n\tjoin sales on customers.id = sales.customer_id\nwhere created_on > {p[\'created_on\']}}\ngroup by customers.id\n""")\n\nprint(q1.preview_pd(con))\n```\n\n|  | id | name | created_on | sales |\n|--|----|------|------------|-------|\n|1 |111 |John Smith | 2020-02-05 | 32.0 |\n|2 |112 |Amy Zhang | 2020-05-01 | 101.5 |\n|3 |115 |Tran Thanh | 2020-03-02 | 100000.0 |\n\n\nThe preview will pull down 10 rows to a) sanity-check the result of what you\'ve just written, and b) validate your sql.\n\n-----\n\nNow, try building some new queries *that build on your previous queries*:\n```py\nq2 = Q(f"""\nselect\n\tntile(100) over (order by sales)\n\t\tas ntile_100,\n\tname,\n\tsales\nfrom {q1}\n""")\n\nprint(q2.preview_pd(con))\n```\n\n|  | ntile_100 | name | sales |\n|--|-----------|------|-------|\n| 1|29| John Smith| 32.0 |\n| 2|50|Amy Zhang | 101.5 |\n| 3|99|Tran Thanh | 100000.0 |\n\n-----\n\n```py\nq3 = Q(f"""\nselect\n\tntile_100,\n\tmin(sales),\n\tmax(sales)\nfrom {q2}\ngroup by ntile_100\norder by ntile_100\n""")\n\n# this time, we\'ll pull the whole result instead of just previewing:\nresult = pd.read_sql(**q3.pd(), con=con)\nprint(result)\n```\n|  | ntile_100 | min(sales) | max(sales) |\n|--|-----------|----------|--------------|\n| 28| 29 | 25 | 33.3 |\n| 49| 50 | 98 | 120 |\n| 98| 99 | 5004 | 100000.0 |\n\n-----\n\n## Cool! But, how does it work?\n\nThe basic idea is to turn your queries into a CTE by keeping track of what builds on top of what. For example, for the last query shown, `q3`, what actually gets sent to the database is:\n\n```sql\nwith _subQuery0 as (\n\tselect\n\t\tcustomers.id,\n\t\tfirst(customers.name) as name,\n\t\tfirst(created_on) as created_on,\n\t\tsum(sales.value) as sales\n\tfrom\n\t\tcustomers\n\t\tjoin sales on customers.id = sales.customer_id\n\twhere created_on > :1\n\tgroup by customers.id\n),\n_subQuery1 as (\n\tselect\n\t\tntile(100) over (order by sales)\n\t\t\tas ntile_100,\n\t\tname,\n\t\tsales\n\tfrom {q1}\n)\nselect\n\tntile_100,\n\tmin(sales),\n\tmax(sales)\nfrom {q2}\ngroup by ntile_100\norder by ntile_100\n```\n\nwhich is exactly the sort of unmaintainable and undebuggable monstrosity that this library is designed to help you avoid.\n\n## Design Notes:\n\nI am perhaps overly optimistic about this, but currently I think this should work with most SQL dialects. It doesn\'t attempt to parse your SQL, uses CTEs which are widely supported, and passes numeric style parameters.\nIt\'s also not actually tied to `pandas` at all - `.pd()` is just a convenience method to build a dict you can splat into pd.read_sql.\n\n## Dialects (TODO: API DOCS INSTEAD OF MORE SHITTY README SECTIONS)\n\nDifferent dialects can be specified at render time, or as the default dialect of your Queries. Currently the only thing dialects control is parameter rendering, but I expect to see some scope creep around here...\nDialects are instances of `SQLDialect` and can be found in `csql.dialect`. The default dialect is `DefaultDialect`, which uses a numeric parameter renderer. You can specify your own prefered dialect per-query:\n```py\nimport csql\nimport csql.dialect\n\nq = csql.Q(\n\tf"select 1 from thinger",\n\tdialect=csql.dialect.DuckDB\n)\n```\n\nIf you want to set a default, use `functools.partial` like so:\n```py\nimport csql\nimport csql.dialect\nimport functools\nQ = functools.partial(csql.Q, dialect=csql.dialect.DuckDB)\nq = Q(f"select 1 from thinger")\n```\n\nYou can also construct your own dialects:\n```py\nimport csql.dialect\nMyDialect = csql.dialect.SQLDialect(\n\tparamstyle=csql.dialect.ParamStyle.qmark\n)\n```\n\n### Dialect Options:\n\n#### paramstyle: csql.dialect.ParamStyle\n\n`paramstyle` can be one of\n - `ParamStyle.numeric` (`where abc = :1`)\n - `ParamStyle.numeric_dollar` (`where abc = $1`)\n - `ParamStyle.qmark` (`where abc = ?`)\n\n## TODO / Future Experiments:\n\n - Document the API (for now, just read the tests)\n - Implement other preview systems than `pandas` (input wanted! what would be useful for you?)\n - Finalize API to be as ergonomic as possible for interactive use (input wanted!)\n - Implement some way of actually storing previous results, e.g. into temp tables. (uh oh, this would need DB-specific awareness :( )\n',
    'author': 'Jarrad Whitaker',
    'author_email': 'akdor1154@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/akdor1154/python-csql',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
