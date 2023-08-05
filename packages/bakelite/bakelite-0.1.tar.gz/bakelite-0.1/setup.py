# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bakelite',
 'bakelite.generator',
 'bakelite.proto',
 'bakelite.tests',
 'bakelite.tests.proto']

package_data = \
{'': ['*'],
 'bakelite.generator': ['runtimes/cpptiny/*', 'templates/*'],
 'bakelite.tests': ['generator/.gitignore',
                    'generator/.gitignore',
                    'generator/.gitignore',
                    'generator/.gitignore',
                    'generator/.gitignore',
                    'generator/Makefile',
                    'generator/Makefile',
                    'generator/Makefile',
                    'generator/Makefile',
                    'generator/Makefile',
                    'generator/cpptiny.cpp',
                    'generator/cpptiny.cpp',
                    'generator/cpptiny.cpp',
                    'generator/cpptiny.cpp',
                    'generator/cpptiny.cpp',
                    'generator/doctest.h',
                    'generator/doctest.h',
                    'generator/doctest.h',
                    'generator/doctest.h',
                    'generator/doctest.h',
                    'generator/struct.ex',
                    'generator/struct.ex',
                    'generator/struct.ex',
                    'generator/struct.ex',
                    'generator/struct.ex']}

install_requires = \
['bitstring>=3.1.7,<4.0.0',
 'click>=8.0.3,<9.0.0',
 'crcmod>=1.7,<2.0',
 'dataclasses-json>=0.5.2,<0.6.0',
 'jinja2>=2.11.2,<3.0.0',
 'lark-parser>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['bakelite = bakelite.generator.cli:main']}

setup_kwargs = {
    'name': 'bakelite',
    'version': '0.1',
    'description': 'Bakelite is a utility that automates the tedious tasks involved in communicating with hardware. You define your protocol defenition, and Bakelite will generate source code for you. Common tasks such as framing and error detection are handled out of the box.',
    'long_description': "# Bakelite\n\nBakelite is a utility that automates the tedious tasks involved in communicating with hardware.\nYou define your protocol defenition, and Bakelite will generate source code for you.\nCommon tasks such as framing and error detection are handled out of the box.\n\n## Features\n* Supported languages:\n  * C++\n  * Python\n* Protocol supports:\n  * Enums, Structs, strings, binary data, integers and floating point numbers of varying widths.\n  * Variable length strings and binary data.\n* Framing (COBS)\n* Error checking (CRC 8/16/32)\n\nDocumentation hasn't been written yet, but a more formal overview of the protocol can be found\n[here](./docs/protocol.md), and examples can be found [here](./examples).\n\n## Status\nThis project is in early development. The C++ implementation is currently WIP.\nThe API and data format are not stable, and will change without notice.\nThe package has not yet been published to pypi.\nIf you'd like to try out an early version, see the [contributing](./CONTRIBUTING.md) guide for installation instructions.\n\n\n# Usage\n\n## Installation\n\nBakelite requires Python 3.8 or above.\n\nInstall it via pip.\n```bash\n$ pip install bakelite\n```\n__This is for future reference, it hasn't been published to pypi yet.__\nIf you'd like to try out an early version, see the [contributing](./CONTRIBUTING.md) guide.\n\n## Code Generation\n\nAfter installation, a new CLI tool `bakelite` is now available.\n\nCraete a protocol defenition file `my_proto.bakelite`.\n```text\nstruct TestMessage {\n  message: string[128]\n}\n\nstruct Ack {\n  code: uint8\n}\n\nprotocol {\n  maxLength = 256\n  framing = COBS\n  crc = CRC8\n\n  messageIds {\n    TestMessage = 1\n    Ack = 2\n  }\n}\n```\n\nThen generate bindings for the languages you use.\n\n```bash\n# Generate C++ Bindings\n$ bakelite runtime -l cpptiny -o bakelite.h\n$ bakelite gen -l cpptiny -i my_proto.bakelite -o my_proto.h\n\n# Generate Python Bindings\n$ bakelite gen -l python -i my_proto.bakelite -o my_proto.py\n```\n\nA more full features example can be found [here](./examples/arduino).",
    'author': 'Brendan Powers',
    'author_email': 'brendan0powers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/bakelite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
