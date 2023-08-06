# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vxt',
 'vxt.audio',
 'vxt.misc',
 'vxt.speech2text',
 'vxt.view',
 'vxt.view.task',
 'vxt.view.task.audio',
 'vxt.view.task.misc',
 'vxt.view.task.speech2text']

package_data = \
{'': ['*']}

install_requires = \
['SpeechRecognition>=3.8.0,<4.0.0',
 'click>=8.0.3,<9.0.0',
 'inquirer>=2.8.0,<3.0.0',
 'pydub>=0.25.0,<0.26.0',
 'termcolor>=1.1.0,<2.0.0',
 'yaspin>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'vxt',
    'version': '0.1.0.post1',
    'description': 'A python CLI tool to extract voice sentences from audio files with speech recognition',
    'long_description': '# VoiceXTractor\n\n<p align="center">~ A python CLI tool to extract voice sentences from audio files with speech recognition ~</p>\n<p align="center">\n  <a href="https://ko-fi.com/veeso" target="_blank">Ko-fi</a>\n  ·\n  <a href="#get-started">Installation</a>\n  ·\n  <a href="CHANGELOG.md" target="_blank">Changelog</a>\n</p>\n\n<p align="center">Developed by <a href="https://veeso.github.io/" target="_blank">@veeso</a></p>\n<p align="center">Current version: 0.1.0 (09/01/2022)</p>\n\n<p align="center">\n  <a href="https://opensource.org/licenses/MIT"\n    ><img\n      src="https://img.shields.io/badge/License-MIT-teal.svg"\n      alt="License-MIT"\n  /></a>\n  <a href="https://github.com/veeso/vxt/stargazers"\n    ><img\n      src="https://img.shields.io/github/stars/veeso/vxt.svg"\n      alt="Repo stars"\n  /></a>\n  <a href="https://pepy.tech/project/vxt"\n    ><img\n      src="https://pepy.tech/badge/vxt"\n      alt="Downloads counter"\n  /></a>\n  <a href="https://pypi.org/project/vxt/"\n    ><img\n      src="https://badge.fury.io/py/vxt.svg"\n      alt="Latest version"\n  /></a>\n  <a href="https://ko-fi.com/veeso">\n    <img\n      src="https://img.shields.io/badge/donate-ko--fi-red"\n      alt="Ko-fi"\n  /></a>\n</p>\n<p align="center">\n  <a href="https://github.com/veeso/vxt/actions"\n    ><img\n      src="https://github.com/veeso/vxt/workflows/Ci/badge.svg"\n      alt="CI"\n  /></a>\n</p>\n\n---\n\n## About VXT 🚜\n\nVXT, which stands for VoiceXTractor is a Python command-line utility to extract voice tracks from audio.\n\nHow it works:\n\n1. You provide VXT with an audio file\n2. The audio file is split by silence\n3. for each "track" chunked by the audio file, it gets the speech for it using a customisable speech-to-text engine\n4. you can at this point work on tracks (amplify, normalize, split, remove...)\n5. export the tracks to files with the format you prefer\n\n---\n\n## Get started 🚀\n\nYou can install VXT with pip:\n\n```sh\npip3 install vxt\n```\n\nthen you can run VXT with the following arguments:\n\n```sh\nvxt -l it_IT -o ./output/ ./hackerino.mp3\n```\n\nthis will split the `hackerino.mp3` audio file into tracks by voice into `output/`, the `-l` option specifies the audio language is Italian.\n\nvxt supports these options:\n\n```txt\n  -e, --engine TEXT            Specify speech2text engine [bing, google,\n                               google-cloud, houndify, ibm, sphinx] (default:\n                               google)\n\n  -l, --language TEXT          Specify audio language (e.g. it_IT), system\n                               language will be used otherwise\n\n  -f, --output-fmt TEXT        Specify output format (See readme)\n  -o, --output-dir TEXT        Specify output directory\n  -A, --api-key TEXT           Specify api key (required for: bing, google\n  -J, --json-credentials TEXT  Specify json credentials (required for: google-\n                               cloud)\n\n  -C, --client-id TEXT         Specify client id (required for: houndify)\n  -K, --client-key TEXT        Specify client key (required for: houndify)\n  -U, --username TEXT          Specify username (required for: ibm)\n  -P, --password TEXT          Specify user password (required for: ibm)\n  --keyword-entries TEXT       Specify keyword entries (required for: sphinx)\n  --grammar-file TEXT          Specify grammar file (required for: sphinx)\n  --help                       Show this message and exit.\n```\n\nby default the `google` engine will be used for speech-to-text.\n\n### Output format\n\nTrack filename fmt.\nThe syntax use parameters which must be preceeded by `%`, everything in between will be kept the same.\nThe following parameters are supported.\n\n- `%%`: print percentage symbol\n- `%d`: current day\n- `%H`: current hours\n- `%I`: current timestamp ISO8601 syntax\n- `%M`: current minutes\n- `%m`: current month\n- `%S`: current seconds\n- `%s`: track speech\n- `%s.NUMBER` track speech cut at length (e.g. `%s.24`)\n- `%t`: track number in track list (from 1 to n)\n- `%y`: current year with 2 digits\n- `%Y`: current year with 4 digits\n\n---\n\n## Support the developer ☕\n\nIf you like VXT and you\'re grateful for the work I\'ve done, please consider a little donation 🥳\n\nYou can make a donation with one of these platforms:\n\n[![ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/veeso)\n[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.me/chrisintin)\n\n---\n\n## Contributing and issues 🤝🏻\n\nContributions, bug reports, new features and questions are welcome! 😉\nIf you have any question or concern, or you want to suggest a new feature, or you want just want to improve VXT, feel free to open an issue or a PR.\n\nPlease follow [our contributing guidelines](CONTRIBUTING.md)\n\n---\n\n## Changelog ⏳\n\nView VXT\'s changelog [HERE](CHANGELOG.md)\n\n---\n\n## Powered by 💪\n\nVXT is powered by these awesome projects:\n\n- [PyInquirer](https://github.com/CITGuru/PyInquirer)\n- [pydub](http://pydub.com/)\n- [speech_recognition](https://github.com/Uberi/speech_recognition)\n- [yaspin](https://pypi.org/project/yaspin/)\n\n---\n\n## License 📃\n\nVXT is licensed under the MIT license.\n\nYou can read the entire license [HERE](LICENSE)\n',
    'author': 'veeso',
    'author_email': 'christian.visintin1997@gmail.com',
    'maintainer': 'veeso',
    'maintainer_email': 'christian.visintin1997@gmail.com',
    'url': 'https://github.com/veeso/vxt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
