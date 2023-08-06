# simpleUID (unique ID) for Python

[![GitHub releases](https://img.shields.io/github/v/release/w-kuipers/simpleUID)](https://github.com/w-kuipers/simpleUID/releases)
[![PyPI release](https://img.shields.io/pypi/v/simpleUID.svg)](https://pypi.org/project/simpleUID/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple and intuitive Python package for generating unique IDs.

This package helps developers by giving them some "quality of life" features. Stop rewriting the same piece of code in every project.

## Installation

### Requirements

Use this section to list unusual dependencies or dependencies that must be installed manually.

### Install using PIP

    pip install simpleUID

Note the `pip` refers to the Python 3 package manager. In environment where Python 2 is also available the correct command may be `pip3`.

## Usage

Import simpleUID:

    import simpleUID

Create a random string:

    simpleUID.string()

You can specify the string length and a prefix:

    simpleUID.string(length=20, prefix='start')

All functions will take the same arguments, existing functions are:
| Function        | Args(with default)           | Returns  |
| ------------- |:-------------:| -----:|
| string      | length=6, prefix  | 6 character long string excl. prefix |
| integer     | length=6, prefix      |   6 character long integer excl. prefix |

Keep in mind that the prefix for the `integer` function should be of type `int`.
## Support

If you found a problem with the software, please [create an issue](https://github.com/w-kuipers/simpleUID/issues) on GitHub.

## Maintainer

This project is maintained by [Filmage](https://www.filmage.nl/).

## Contributing

Your contributions are highly appreciated. Please [create a pull request](https://github.com/w-kuipers/simpleUID/pulls) on GitHub. Bigger changes need to be discussed with the development team via the [issues section at GitHub](https://github.com/w-kuipers/simpleUID/issues) first.


## License

[MIT LICENSE](https://github.com/w-kuipers/simpleUID/blob/master/LICENSE)