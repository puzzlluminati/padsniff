# Padsniff: A Puzzle & Dragons HTTP Sniffer

[![PyPI](https://img.shields.io/pypi/v/padsniff.svg?style=flat-square)](https://pypi.python.org/pypi/padsniff)[![CI](https://gitlab.com/wmedlar/padsniff/badges/develop/pipeline.svg)](https://gitlab.com/wmedlar/padsniff/pipelines)

## Quickstart

```shell
$ pip install padsniff
```

Padsniff can be used as either a cli:

```shell
$ padsniff run --port 8080 --script examples/log_plus_eggs.py
runs:   1 | hp:   1 | atk:   1 | rcv:   2
[...]
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

See the [device setup guide](docs/device-setup.md) to learn how to set up your phone to proxy through padsniff, and the [usage guide](docs/usage.md) for more advanced usage.

## Installation

Padsniff requires Python 3.5+. Install it with your package manager or using [pyenv](https://github.com/yyuu/pyenv).

```shell
$ pyenv update && pyenv install 3.5.2
$ pyenv shell 3.5.2
```

See the [suggested build environment](https://github.com/yyuu/pyenv/wiki#suggested-build-environment) page if you're having trouble getting pyenv to work.

### OSX

Apple removed the OpenSSL headers in _El Capitan_, so you'll have to set some environment variables before installing `padsniff`'s dependencies.

```shell
$ brew install openssl
$ export ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include"
$ pip install padsniff
```

Padsniff depends on mitmproxy's transparent proxying capabilities. Follow their [instructions](http://docs.mitmproxy.org/en/stable/transparent/osx.html) to set up your computer for proxying.

### Debian / Ubuntu

Padsniff includes a pretty heavy list of dependencies, including [lxml](http://lxml.de/) and [cryptography](https://cryptography.io/). You'll need to install some of their dependencies via your package manager.

```shell
$ sudo apt-get install -y build-essential libffi-dev libssl-dev libxml2-dev libxslt-dev python3-dev
$ export LC_ALL=C.UTF-8 LANG=C.UTF-8
$ pip install padsniff
```

This will also set up your environment to support [click](http://click.pocoo.org/), the library that powers padsniff's command line interface.

Padsniff depends on mitmproxy's transparent proxying capabilites. Follow their [instructions](http://docs.mitmproxy.org/en/stable/transparent/linux.html) to set up your computer for proxying.

### Development

```shell
$ git clone git@gitlab.com:wmedlar/padsniff.git
$ cd padsniff
$ pip install -r dev-requirements.txt -e .
```

This will install the testing dependencies -- padsniff uses [pytest](http://doc.pytest.org/) for unit testing -- and install padsniff in [editable mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).
