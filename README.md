# Padsniff: A Puzzle & Dragons HTTP Sniffer
---------------

[![PyPI](https://img.shields.io/pypi/v/padsniff.svg?style=flat-square)](https://pypi.python.org/pypi/padsniff)[![CircleCI](https://img.shields.io/circleci/project/bitbucket/necromanteion/padsniff.svg?style=flat-square)](https://circleci.com/bb/necromanteion/padsniff)

## Quickstart

Padsniff can be used as either a cli:

```bash
$ padsniff run --port 8080 --script examples/log_plus_eggs.py
runs:   1 | hp:   1 | atk:   1 | rcv:   2
```

... or as a library!

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

Padsniff requires Python 3.5+. I recommend using [pyenv](https://github.com/yyuu/pyenv) to install this if you don't already have it.

```bash
$ pyenv update && pyenv install 3.5.2
$ pyenv shell 3.5.2
```

### OSX

Apple removed the OpenSSL headers in _El Capitan_, so you'll have to set some environment variables before installing `padsniff`'s dependencies.

```bash
$ brew install openssl
$ export ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include"
$ pip install padsniff
```

Padsniff depends on mitmproxy's transparent proxying capabilities. Follow their [instructions](http://docs.mitmproxy.org/en/stable/transparent/osx.html) to set up your device.

### Development

Install OpenSSL and configure your environment variables (if necessary), then run:

```bash
$ git clone git@bitbucket.org:necromanteion/padsniff.git padsniff
$ cd padsniff
$ pip install -r dev-requirements.txt -e .
```
