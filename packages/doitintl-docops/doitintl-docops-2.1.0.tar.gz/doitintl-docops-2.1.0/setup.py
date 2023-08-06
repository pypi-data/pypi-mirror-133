# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['doitintl',
 'doitintl.docops',
 'doitintl.docops.gitbook',
 'doitintl.docops.gitbook.cli',
 'doitintl.docops.gloss',
 'doitintl.docops.gloss.analyzers',
 'doitintl.docops.gloss.cli',
 'doitintl.docops.screenshots',
 'doitintl.docops.screenshots.cli']

package_data = \
{'': ['*'],
 'doitintl.docops': ['data/corpora/*'],
 'doitintl.docops.screenshots': ['assets/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'api-client>=1.3.1,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'charset-normalizer>=2.0.4,<3.0.0',
 'docopt>=0.6.2,<0.7.0',
 'inflect>=5.3.0,<6.0.0',
 'inflection>=0.5.1,<0.6.0',
 'nltk>=3.6.2,<4.0.0',
 'pastel>=0.2.1,<0.3.0',
 'simplejson>=3.17.5,<4.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['docops-gitbook = doitintl.docops.gitbook.cli:run',
                     'docops-gloss-terms = doitintl.docops.gloss.cli.terms:run',
                     'docops-screenshots = '
                     'doitintl.docops.screenshots.cli:run']}

setup_kwargs = {
    'name': 'doitintl-docops',
    'version': '2.1.0',
    'description': 'Python library and CLI tools for doing DocOps at DoiT',
    'long_description': '# DoiT DocOps Utilities\n\n_Python library and CLI tools for doing DocOps at DoiT_\n\n[![Tests][action-packaging-img]][action-packaging] [![DocOps][action-docops-img]][action-docops]\n\n**Table of contents:**\n\n- [Install](#install)\n- [Documentation](#documentation)\n  - [Users](#users)\n  - [Developers](#developers)\n\n## Install\n\nThe [doitintl-docops][pypi-project] package is published to [PyPI][pypi] and\nyou can install it using [Pip][pip], like so:\n\n<!-- cspell:disable -->\n```console\n$ pip install doitintl-docops\nCollecting doit-docops\n  Downloading doitintl_docops-2.0.1-py3-none-any.whl (175 kB)\n[...]\nSuccessfully installed doitintl_docops-2.0.1\n```\n<!-- cspell:emable -->\n\nThe [project releases][releases] page has a complete list of all releases and\neach release page has links to multiple release assets.\n\n## Documentation\n\n> 📝&nbsp;&nbsp;**Note**\n>\n> Documentation is sparse at the moment because this project is still in the\n> early stages of development.\n\n### Users\n\n- [Glossary utilities][user-gloss]\n- [GitBook client][user-gitbook]\n\n### Developers\n\n- [Python development][dev-python]\n\n[action-docops-img]: https://github.com/doitintl/docops-utils/actions/workflows/docops.yaml/badge.svg\n[action-docops]: https://github.com/doitintl/docops-utils/actions/workflows/docops.yaml\n[action-packaging-img]: https://github.com/doitintl/docops-utils/actions/workflows/packaging.yaml/badge.svg\n[action-packaging]: https://github.com/doitintl/docops-utils/actions/workflows/packaging.yaml\n[dev-python]: https://github.com/doitintl/docops-python/blob/main/docs/dev/python.md\n[pip]: https://pip.pypa.io/en/stable/\n[pypi-project]: https://pypi.org/project/doitintl-docops\n[pypi]: https://pypi.org/\n[releases]: https://github.com/doitintl/docops-python/releases\n[user-gitbook]: https://github.com/doitintl/docops-python/blob/main/docs/user/gitbook.md\n[user-gloss]: https://github.com/doitintl/docops-python/blob/main/docs/user/gloss.md\n',
    'author': 'DoiT International',
    'author_email': 'engineering@doit-intl.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/doitintl/docops/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
