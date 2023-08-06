# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['check_uncommitted_git_changes']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['check_uncommitted_git_changes = '
                     'check_uncommitted_git_changes.main:main']}

setup_kwargs = {
    'name': 'check-uncommitted-git-changes',
    'version': '1.0.0',
    'description': 'check for uncommitted git changes to identify outdated generated content during continuous integration',
    'long_description': '# check_uncommitted_get_changes\n\n`Check_uncommitted_get_changes` is a command line tool to check for\nuncommitted git changes to identify outdated generated content during\ncontinuous integration.\n\n## The problem\n\nWhile generated code generally should not be committed, there are cases for\nwhere it can make sense, for example `*.po` files containing translations that\nare derived from source code.\n\nDevelopers might change the underlying source code but forget to generate\nthe files derived from it. This causes headache for the next developer\nwho wants to a translated message while implementing a separate task, and\nnot has to deal with the outdated content in some way.\n\n## The solution\n\nIf your project uses continuous integration, you can use it to run the\ncode generators. Ideally they produce the same code that has already been\ncommitted to the repository.\n\nHowever, if a developer forgot to commit up to date generated code, the\ncode generators will produce slightly different code that can for example\nbe viewed using\n\n```bash\ngit status\n```\n\nCalling `check_uncommitted_get_changes` after the generators have run can\ncheck for such changes. If there are none, its exit code is 0 and\ncontinuous integration can continue. If changes are found, the exit code is\n1 and continuous integration fails.\n\n## Usage\n\nAdd `check_uncommitted_get_changes` to your projects using the respective\ncommand depending on how you manage your Python packages.\n\nFor poetry, run:\n\n```bash\npoetry add --dev check_uncommitted_get_changes\n```\n\nFor setuptools, run:\n\n```bash\npip install --upgrade check_uncommitted_get_changes\n```\n\nor add an entry to your `*requirements.txt`.\n\nThe following example outlines a\n[GitHub action](https://github.com/features/actions) step that first collects\nall translated messages of a Django project and then checks if they differ\nfrom the versions found in the repository:\n\n```yaml\n...\njobs:\n  build:\n    ...\n    steps:\n      ...\n      - name: Check that translations are up to date\n        run: |\n          python manage.py makemessages --all --ignore venv --no-location --no-obsolete\n          check_uncommitted_git_changes\n```\n\nThe same principle can be applied to\n[other continuous integration platforms](https://en.wikipedia.org/wiki/Comparison_of_continuous_integration_software).\n\n## License\n\n`Check_uncommitted_git_changes` is open source and distributed under the BSD\nlicense. The source code is available from\n<https://github.com/roskakori/check_uncommitted_get_changes>.\n\n## Change history\n\nSee "CHANGES".\n\n## Development and contributing\n\nFor information on how to build the project and contribute to it see "CONTRIBUTING".\n',
    'author': 'Thomas Aglassinger',
    'author_email': 'roskakori@users.sourceforge.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roskakori/check_uncommitted_git_changes',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
