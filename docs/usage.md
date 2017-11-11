# Usage

## Summary

- `certs` generates a new root CA key and certificate, used by padsniff to generate on-the-fly certificates for HTTPS traffic interception.
- `run` starts up the proxy listener, sending events to subscribers as they come in.

All commands accept a `--help` flag to display usage information and argument defaults.

## certs

In it's simplest form, `padsniff certs` generates three new files:
- `~/.padsniff/padsniff-ca-cert.pem` containing the root CA certificate
- `~/.padsniff/padsniff-ca-key.pem` containing the root CA key
- `~/.padsniff/padsniff-ca.pem` containing the root CA key and certificate pair

By default these files are installed to `~/.padsniff`, however this can be changed with the `--directory` flag. The specified directory will be created if it doesn't already exist.

```shell
$ padsniff certs --directory /tmp/padsniff
/tmp/padsniff/padsniff-ca-key.pem
/tmp/padsniff/padsniff-ca-cert.pem
/tmp/padsniff/padsniff-ca.pem
```

Padsniff will not attempt to overwrite files that already exist, to prevent accidental data loss. If a new root pair is desired, pass in the `--overwrite` flag.

```shell
$ ls /tmp/padsniff
padsniff-ca-cert.pem	padsniff-ca-key.pem	padsniff-ca.pem
$ padsniff certs --directory /tmp/padsniff
$ padsniff certs --directory /tmp/padsniff --overwrite
/tmp/padsniff/padsniff-ca-key.pem
/tmp/padsniff/padsniff-ca-cert.pem
/tmp/padsniff/padsniff-ca.pem
```

Certificate generation can be customized with the `--organization`, `--common-name`, and `--expiry` flags.

```shell
$ padsniff certs --directory /tmp/padsniff --organization 'Not GungHo' --common-name 'My Padsniff Cert' --overwrite
/tmp/padsniff/padsniff-ca-key.pem
/tmp/padsniff/padsniff-ca-cert.pem
/tmp/padsniff/padsniff-ca.pem
$ openssl x509 -noout -text -in /tmp/padsniff/padsniff-ca-cert.pem | grep Subject:
        Subject: CN=My Padsniff Cert, O=Not GungHo
```

See the [device setup guide](device-setup.md) to learn how to install these to your device.

## run

`padsniff run` starts up a proxy on your device listening for incoming requests from the PAD app. On its own it's not very useful, but coupled with scripts can become a very powerful tool for monitoring traffic and reverse-engineering the PAD API. See the [examples](../examples/) for some scripting inspiration.

Load scripts with the `--script` flag. Additional scripts can be loaded by supplying the flag multiple times.

```shell
$ padsniff run --script examples/log_plus_eggs.py --verbose
[INFO] :: Loaded script examples/log_plus_eggs.py.
[INFO] :: Using certificate from ~/.padsniff.
[INFO] :: Starting proxy on port 8080.
```

Run some dungeons to see your script in action.

```shell
$ padsniff run --script examples/log_plus_eggs.py
runs:   1 | hp:   0 | atk:   1 | rcv:   0
runs:   2 | hp:   2 | atk:   1 | rcv:   0
runs:   3 | hp:   3 | atk:   2 | rcv:   2
```

By default the proxy binds to port 8080, although this can be changed with the `--port` flag.

```shell
$ padsniff run --port 9999 --verbose
[INFO] :: Using certificate from ~/.padsniff.
[INFO] :: Starting proxy on port 9999.
```

You can also specify the directory containing your padsniff-generated or custom root certificate with `--cadir`. The specified directory should contain the same credentials installed to your device.

```shell
$ padsniff run --cadir /tmp/padsniff --verbose
[INFO] :: Using certificate from /tmp/padsniff.
[INFO] :: Starting proxy on port 8080.
```

To maintain sensible out-of-the-box behavior, a new root pair will be silently generated if not found in the specified directory. If padsniff isn't working as expected, double-check your spelling here.

```shell
$ ls /tmp/padsniff
$ padsniff run --cadir /tmp/padsniff --verbose
[INFO] :: Using certificate from /tmp/padsniff.
[INFO] :: Starting proxy on port 8080.
^C[INFO] :: Shutting down.
$ ls /tmp/padsniff
padsniff-ca-cert.pem	padsniff-ca-key.pem	padsniff-ca.pem
```
