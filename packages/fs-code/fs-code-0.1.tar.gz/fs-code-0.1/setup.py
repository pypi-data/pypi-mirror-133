# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['codefs', 'codefs.gitfs', 'codefs.githubfs', 'codefs.gitlabfs']

package_data = \
{'': ['*']}

install_requires = \
['fs>=2.4,<3.0', 'schema>=0.7,<0.8']

extras_require = \
{'all': ['dulwich>=0.20,<0.21',
         'python-gitlab>=3.0,<4.0',
         'werkzeug>=2.0,<3.0',
         'PyGithub>=1.55,<2.0',
         'requests>=2.26,<3.0'],
 'gitfs': ['dulwich>=0.20,<0.21'],
 'githubfs': ['werkzeug>=2.0,<3.0',
              'PyGithub>=1.55,<2.0',
              'requests>=2.26,<3.0'],
 'gitlabfs': ['python-gitlab>=3.0,<4.0', 'werkzeug>=2.0,<3.0']}

entry_points = \
{'fs.opener': ['gitfs = codefs.gitfs.opener:Opener [gitfs]',
               'github = codefs.githubfs.opener:Opener [githubfs]',
               'gitlab = codefs.gitlabfs.opener:Opener [gitlabfs]']}

setup_kwargs = {
    'name': 'fs-code',
    'version': '0.1',
    'description': 'PyFilesystems for GitLab, GitHub, and Git',
    'long_description': '# fs-code\n\n![pipeline status][pipeline status] ![3.8 coverage][3.8 coverage] ![3.10 coverage][3.10 coverage]\n\n[PyFilesystems](https://www.pyfilesystem.org/) for GitLab, GitHub, and Git.\n\n---\n\n## Installation\n\nTODO\n\n## Usage\n\n### with <a target="_blank" href="https://docs.pyfilesystem.org/en/latest/openers.html">FS URL</a>\n\n```python\nimport fs\n\nuser_fs = fs.open_fs("gitlab://?user=dAnjou")\nreadme = user_fs.open("fs-code/main/README.md")\nprint(readme.read())\n```\n\n### with class\n\n```python\nfrom gitlab import Gitlab\nfrom codefs.gitlabfs import UserFS\n\nuser_fs = UserFS(Gitlab(), user="dAnjou")\nreadme = user_fs.open("fs-code/main/README.md")\nprint(readme.read())\n```\n\n[pipeline status]: https://gitlab.com/dAnjou/fs-code/badges/main/pipeline.svg\n[3.8 coverage]: https://gitlab.com/dAnjou/fs-code/badges/main/coverage.svg?job=test%3A%20%5Bpython%3A3.8%5D&key_text=3.8+coverage&key_width=90\n[3.10 coverage]: https://gitlab.com/dAnjou/fs-code/badges/main/coverage.svg?job=test%3A%20%5Bpython%3A3.10%5D&key_text=3.10+coverage&key_width=90\n',
    'author': 'Max Ludwig',
    'author_email': 'mail@danjou.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://danjou.gitlab.io/fs-code',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
