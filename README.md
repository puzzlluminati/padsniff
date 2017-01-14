# Padsniff: A Puzzle & Dragons HTTP Sniffer
---------------

[![PyPI](https://img.shields.io/pypi/v/padsniff.svg?style=flat-square)](https://pypi.python.org/pypi/padsniff)[![CircleCI](https://img.shields.io/circleci/project/bitbucket/necromanteion/padsniff.svg?style=flat-square)](https://circleci.com/bb/necromanteion/padsniff)

## Quickstart

```python
import padsniff
import json

@padsniff.on(action='get_player_data')
def hello(request, response):
    username = json.loads(response.content.decode())['name']
    print('Hello, %s!' % username)

if __name__ == '__main__':
    proxy = padsniff.Proxy()
    proxy.run()
```


## Installation

### OSX

Apple removed the OpenSSL headers in _El Capitan_, so you'll have to set some environment variables before installing `padsniff`'s dependencies.

```bash
$ brew install openssl
$ export ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include"
$ pip install padsniff
```

### Development

Install OpenSSL and configure your environment variables (if necessary), then run:

```bash
$ git clone git@bitbucket.org:necromanteion/padsniff.git padsniff
$ cd padsniff
$ pip install -r dev-requirements.txt -e .
```
