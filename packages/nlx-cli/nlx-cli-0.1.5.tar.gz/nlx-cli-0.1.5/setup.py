# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlx', 'nlx.conf', 'nlx.utils']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.16.1,<11.0.0']

entry_points = \
{'console_scripts': ['nlx = nlx.main:main']}

setup_kwargs = {
    'name': 'nlx-cli',
    'version': '0.1.5',
    'description': 'Python SDK for interacting with the NLx API and other affiliated tools',
    'long_description': '## Installation\nInstall via pip\n```bash\npip install nlx-cli\n```\n\n## Configuration\nYou can configure cli settings with a .env file and/or environment variables.\nThe only configuration you will need to modify out of the box is `NLX_API_KEY`.\nTo list the current active configuration, you can use the `config` command:\n```bash\nnlx config | jq\n{\n  "NLX_ENV_PATH": ".env",\n  "NLX_SUPPRESS_ENV_NOTICE": true,\n  "NLX_LOG_LEVEL": "INFO",\n  "NLX_API_KEY": "<redacted>",\n  "NLX_API_URL": "https://api.nlxresearchhub.org",\n  "NLX_REPORT_HISTORY_STORAGE": "nlx.pickle",\n  "NLX_REPORT_DOWNLOAD_DIR": ".reports"\n}\n```\n\n## Usage\nYou can use any access methods defined directly by the CLI or you can define a custom\nrunner module. For details on CLI methods, you can run `nlx --help`.\n\n### Custom Runner Module\nCustom runner modules allow you to specify a client class and a list of operations to perform with\nthat client class. Custom runner modules must define the following:\n- `RUNNER_CLIENT` python module style import path to your Client class definition\n- `RUNNER_OPS` list of operations which will be performed by your client\n- `RUNNER_OP_ERROR_HANDLER` function which wraps each operation and handles thrown errors\n\nBelow is an example of a custom runner module (the current revision of which can be found in [./examples/example_run_config.py](./examples/example_run_config.py)).\nTo run this example, copy the contents of the runner into a `example_run_config.py` in you current working directory\nand execute the command `nlx run example_run_config`. To preview the operations that this will run, you can use\n`nlx show_ops example_run_config`\n\n```python\n"""\nThis runner will create, await, and download async reports for all job listings\ncompiled in the years 2017-2022 for Kansas.\n\nYou want to place this file in your current working directory or a location that\nis importable from your current python path.\n"""\nimport logging\n\nfrom nlx.helpers import helpers\nfrom nlx.utils.misc import basic_logger\n\nlogger = basic_logger(__name__, logging.DEBUG)\n\n# python module style import path of the Client class to be executed by the runner.\nRUNNER_CLIENT = "nlx.client.AsyncReport"\n\n# years 2017-2022, inclusive\nYEARS = [*range(2017, 2023)]\n# Kansas\nSTATES = ["KS"]\n\nRUNNER_OPS = []\nfor state in STATES:\n    for year in YEARS:\n        # generate twelve months of the arguments for start, end, state, auto\n        for generated_kwargs in helpers.generate_year_kwargs(year, state=state, auto=True):\n            # indicate that the kwargs will be passed to RUNNER_CLIENT.create, e.g.\n            # nlx.client.AsyncReport().create(**generated_kwargs)\n            RUNNER_OPS.append(("create", generated_kwargs))\n\n\ndef error_handler(func, *args, **kwargs):\n    try:\n        return func(*args, **kwargs)\n    except KeyboardInterrupt:\n        raise\n    except:  # noqa\n        logger.exception(\n            f"Something unexpected happened when executing func={func} args={args}, kwargs={kwargs}"\n        )\n\n\nRUNNER_OP_ERROR_HANDLER = error_handler\n\n```\n\n### Programmatic Usage\nIf custom runner modules don\'t provide enough flexibility for your use-case, you can always import anything\navailable in the nlx-cli package for use as you see fit.\n```python\nfrom nlx.client import AsyncReport\n\nassert AsyncReport().is_authorized\n```\n\n### Build & Publish\n```bash\n# asks for credentials\npoetry publish --build\n\n# OR\npip install twine\nrm -rf ./dist/\npoetry build\n# uses ~/.pypirc\ntwine upload -r testpypi dist/*\ntwine upload -r pypi dist/*\n```\n',
    'author': 'jjorissen52',
    'author_email': 'jjorissen52@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CorrDyn/nlx-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
