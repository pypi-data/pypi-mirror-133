# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['futurecandy', 'futurecandy.hooks']

package_data = \
{'': ['*']}

install_requires = \
['enquiries>=0.1.0,<0.2.0',
 'prompt-toolkit>=3.0.20,<4.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'futurecandy',
    'version': '1.2.1',
    'description': 'Project initialization utility for Linux.',
    'long_description': '# futurecandy\n`><=><`\n\nLinux utility for launching projects in a single command.\n\nInstall with `pip install futurecandy`.\n\nRun with `python3 -m futurecandy` or add a command alias to your shell RC file with `python3 -m futurecandy rc` to run with command `futurecandy`.\n\nfuturecandy will create directory `.futurecandy` in the user\'s home directory.\nEdit configuration files and hooks there.\n\nRun `python3 -m futurecandy update` or `futurecandy update` to fetch base hooks.\n\n## Hooks\nUsers may add their own hooks, by creating a file in directory `~/.futurecandy/hook`, with file extension `.hook.futurecandy`.\n\nBelow is an example hook,\n```\n[meta]\nname = "LICENSE"\ndescription = "Hook for generating LICENSE files."\n\n[exec]\nscript = "python3 -m futurecandy.hooks.License {}"\nwant_path = True\ncheck_bin = False\n```\n\nHooks must have a `meta` section with the name of the hook, and its description.\nThis will appear on the hook selection menu.\n\nFollowed is the `exec` section with a command to run, defined with property `script`.\n\nTo specify the path to the project directory for the command, include `{}` as a placeholder in the `script` command, which will be replaced with the directory path, and set `want_path` to `True`.\n\nIf `check_bin` is true, futurecandy will split the `script` string by spaces into an array, then extract the first element as the script command for validation. If the "command" does not exist, the user will enter the shell to rectify the situation, before the command is re-ran.\n\n## Updating\nUpdate the package through PIP, then remove and regenerate `~/.futurecandy/`.\n\n## Acknowledgements\n`gitignore.hook.futurecandy` based off of [perpetualCreations/auto-gitignore](https://github.com/perpetualCreations/auto-gitignore) forked from [Mux-Mastermann/auto-gitignore](https://github.com/Mux-Mastermann/auto-gitignore).\n',
    'author': 'perpetualCreations',
    'author_email': 'tchen0584@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dreamerslegacy.xyz/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
