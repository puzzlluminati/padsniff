# Padsniff: A Puzzle & Dragons HTTP Sniffer
---------------

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

Check out the [examples](examples/) for more cool ideas.

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

Padsniff depends on mitmproxy's transparent proxying capabilities. Follow their [instructions](http://docs.mitmproxy.org/en/stable/transparent/osx.html) to set up your device.

### Debian / Ubuntu

Padsniff includes a pretty heavy list of dependencies, including [lxml](http://lxml.de/) and [cryptography](https://cryptography.io/). You'll need to install some of their dependencies via your package manager.

```shell
$ sudo apt-get install -y build-essential libffi-dev libssl-dev libxml2-dev libxslt-dev python3-dev
$ export LC_ALL=C.UTF-8 LANG=C.UTF-8
$ pip install padsniff
```

This will also set up your environment to support [click](http://click.pocoo.org/), the library that powers padsniff's command line interface.

Padsniff depends on mitmproxy's transparent proxying capabilites. Follow their [instructions](http://docs.mitmproxy.org/en/stable/transparent/linux.html) to set up your device.

### A Note on Android 7.0+

Prior to Android 7.0 (Nougat), apps would trust both the user-supplied and system certificate stores. Nougat introduced a breaking change to apps' default network security config to only trust the system certificate store. Unfortunately many apps, PAD included, don't modify this default behavior, and as of PAD v12.2 the target SDK version has been bumped to 24 (7.0 Nougat), breaking standard `padsniff` setups that depend on `mitmproxy`'s user-installed, fake CA. Android devices below version 7.0 are not subject to this behavior.

There is a fix, described below; *unfortunately it requires root access*.

- Find your root CA certificate (default: `~/.mitmproxy/mitmproxy-ca.pem`).
- Compute the legacy hash of the file.
```shell
$ # openssl version >= 1.0.0
$ HASH=$(openssl x509 -inform PEM -subject_hash_old -in "$MITMPROXY_CA" | head -1)
$ # < 1.0.0
$ HASH=$(openssl x509 -inform PEM -subject_hash -in "$MITMPROXY_CA" | head -1)
```
- Copy the cert to your device at `/system/etc/security/cacerts/${HASH}.0` and set permissions to `644`. You can do this with a file manager with root access on your device, or through `adb`.
```shell
$ sudo adb start-server
* daemon not running. starting it now on port 5037 *
* daemon started successfully *
$ adb push "$MITMPROXY_CA" "/sdcard/${HASH}.0"
[100%] /sdcard/<filename>
$ adb shell
device:/ $ # this will probably ask for root access on your device
device:/ $ su
device:/ # mount -o remount,rw /system
device:/ # # this shell doesn't contain our environment variable above
device:/ # # so be sure to manually substitute the filename
device:/ # mv /sdcard/<filename> /system/etc/security/cacerts/
device:/ # chmod 644 /system/etc/security/cacerts/<filename>
device:/ # mount -o remount,ro /system
device:/ # exit
device:/ $ exit
```
- Reboot your device and confirm the certificate is installed under Settings > Security > Trusted Credentials > System. If using the default it will be named simply "mitmproxy".

You should now be able to sniff traffic to and from PAD with no trouble.

### Development

```shell
$ git clone git@gitlab.com:wmedlar/padsniff.git
$ cd padsniff
$ pip install -r dev-requirements.txt -e .
```

This will install the testing dependencies -- padsniff uses [pytest](http://doc.pytest.org/) for unit testing -- and install padsniff in [editable mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).
