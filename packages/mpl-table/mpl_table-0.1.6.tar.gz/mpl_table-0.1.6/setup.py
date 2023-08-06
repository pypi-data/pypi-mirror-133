# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpl_table']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'pandas>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'mpl-table',
    'version': '0.1.6',
    'description': 'Create custom table using matplotlib.',
    'long_description': '# MPL Table\n\nCreate a table with row explanations, column headers, using matplotlib. Intended usage\nwas a small table containing a custom heatmap.\n\n## Installation\n\n`pip install mpl-table`\n\n## Usage\n\nExample usage can be found within `tests/test_create_table.py`, the table is created by\npassing dataframes containing text values, cell colour values, and text colour values.\nYou\'ll probably want to use `bbox_inches="tight"` when you `fig.savefig`.\n\n## Example output\n\nTable with row headers:\n\n![Example output table.](./tests/baseline/test_table_image.png)\n\nTable in subplots:\n\n![Example output in subplots.](./tests/baseline/test_subplots_1.png)\n\nTable with no row headers:\n\n![Example output table without row headers.](./tests/baseline/test_table_with_no_row_headers.png)\n\nTable with no row or column headers:\n\n![Example output table without row or column headers.](./tests/baseline/test_table_with_no_row_headers_and_no_column_headers.png)\n\n## Why\n\nWanted to be able to create tables containing heatmaps, along with row explanations and\ndifferent treatment of high/low values for each row. For some rows the formatting of\n`100%` should be considered positive (typically green), whereas others it should be\nconsidered negative (typically\nred).\n\n## TODO\n\nSimplify creating a table without any row-headers.\n\nConsider makign the spacing for rows/cols dynamic, based on figsize might work.\n\nUsage within subplots, wasn\'t required for what was needed, but there could be some use\nin having subplots with these tables.\n\nDifferent styles - might want to have the header row / row information column without any\nbackground colour, or similar stylings. Shouldn\'t be hard to do from what\'s here, just\nhasn\'t been done.\n',
    'author': 'George Lenton',
    'author_email': 'georgelenton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/geo7/mpl_table',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
