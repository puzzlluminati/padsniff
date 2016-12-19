## Quickstart

```python
import padsniff
import json

@padsniff.on(action='get_player_data')
def log_plus_eggs(request, response):
    username = json.loads(response.content.decode())['name']
    print('hello, %s!' % name)

if __name__ == '__main__':
    proxy = padsniff.Proxy()
    proxy.run()
```


## Installation

### OSX

```bash
$ brew install openssl
$ export ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include"
$ pip install padsniff
```

### Development

Install OpenSSL and configure your environment variables as above, then run:

```bash
$ git clone <repo>
$ cd padsniff
$ pip install -r dev-requirements.txt -e .
```