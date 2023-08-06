# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ipyvuetify_app']

package_data = \
{'': ['*']}

install_requires = \
['char>=0.1.2,<0.2.0', 'ipyvuetify>=1.8.1,<2.0.0', 'ipywidgets>=7.6.5,<8.0.0']

setup_kwargs = {
    'name': 'ipyvuetify-app',
    'version': '0.1.2',
    'description': '',
    'long_description': '===================\nipyvuetify_app\n===================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/ipyvuetify_app\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/ipyvuetify_app\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/ipyvuetify_app\n    :target: https://github.com/stas-prokopiev/ipyvuetify_app/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://img.shields.io/pypi/v/ipyvuetify_app\n   :target: https://img.shields.io/pypi/v/ipyvuetify_app\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/ipyvuetify_app\n   :target: https://img.shields.io/pypi/pyversions/ipyvuetify_app\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nShort Overview.\n=========================\nipyvuetify_app is a python package (**py>=3.7**) with a scaffold/template for writing ipyvuetify application\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install ipyvuetify_app\n\nHow to use it\n===========================\n\n| To create an application by the given template you need to create a class\n| That will be in charge of what to show in the main application section\n| For every selected menu item -> subitem\n| Then you just give it to ipyvuetify_app.VueApp and it does all the magic for you\n\n.. code-block:: python\n\n    from ipyvuetify_app import VueApp\n    from ipyvuetify_app import VueAppRouter\n    vue_app_router = VueAppRouter()\n    VueApp(\n        vue_app_router,\n        list_footer_vw_children=["Footer example"],\n    )\n\nExamples how your app can look like\n----------------------------------------\n\n.. image:: images/light_1.PNG\n.. image:: images/dark_1.PNG\n\nRouter example\n*********************\n\n| Every router should satisfy 2 conditions:\n| 1) It has method **get_main_content(self, item, subitem)** which should return page main content\n| 2) It has attribute **self.dict_list_subitems_by_item** with all subitems for every menu item\n\n.. code-block:: python\n\n    class VueAppRouter():\n        """Routing for VueApp to emulate transition over pages in the app"""\n\n        def __init__(self) -> None:\n            """Initialize dictionary with all menus and their subitems"""\n            self.dict_list_subitems_by_item = {}\n            for item in range(5):\n                list_subitems = [str(subitem) for subitem in range(item, 5 + item)]\n                self.dict_list_subitems_by_item[str(item)] = list_subitems\n\n        def get_main_content(self, item, subitem):\n            """Router to get main content for clicked submenu element\n\n            Args:\n                item (str): selected menu\n                subitem (str): submenu element for which to build a page\n\n            Returns:\n                ipyvuetify container or string: page content to show at main section\n            """\n            try:\n                sleep(int(item))\n                return f"{item} -> {subitem}"\n            except Exception as ex:\n                return self.error_page_content(str(ex))\n\n        def error_page_content(self, str_error="Unable to get page content"):\n            """Return content of error message to show when something going wrong\n\n            Args:\n                str_error (str, optional): Error message to show\n\n            Returns:\n                [str]: Error message to display\n            """\n            return f"ERROR: {str_error}"\n\nFull VuaApp signature\n=============================\n\n.. code-block:: python\n\n    VueApp(\n        vue_app_router,\n        list_vw_fab_app_bar_left=None,\n        list_vw_fab_app_bar_right=None,\n        list_footer_vw_children=None,\n    )\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/ipyvuetify_app/>`_\n    * `readthedocs <https://ipyvuetify_app.readthedocs.io/en/latest/>`_\n    * `GitHub <https://github.com/stas-prokopiev/ipyvuetify_app>`_\n\nProject local Links\n===================\n\n    * `CHANGELOG <https://github.com/stas-prokopiev/ipyvuetify_app/blob/master/CHANGELOG.rst>`_.\n    * `CONTRIBUTING <https://github.com/stas-prokopiev/ipyvuetify_app/blob/master/CONTRIBUTING.rst>`_.\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.',
    'author': 'stanislav',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stas-prokopiev/ipyvuetify_app',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
