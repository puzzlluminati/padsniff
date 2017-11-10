from pathlib import Path

from mitmproxy.certs import create_ca
from OpenSSL.crypto import dump_certificate, dump_privatekey, FILETYPE_PEM

from .constants import DEFAULT_CN, DEFAULT_EXP, DEFAULT_ORG


def generate_root_pair(organization, common_name, expiry):
    """
    Creates a new root key and certificate.

    The pair is returned as a two-tuple of bytes objects (key, ca) in PEM format.
    """
    key, ca = create_ca(o=organization, cn=common_name, exp=expiry)
    key_bytes = dump_privatekey(FILETYPE_PEM, key)
    ca_bytes = dump_certificate(FILETYPE_PEM, ca)
    return key_bytes, ca_bytes


def generate_cert_files(directory, organization=DEFAULT_ORG, common_name=DEFAULT_CN, expiry=DEFAULT_EXP, overwrite=False):
    """
    Creates a new root key and certificate, and dumps them to file in PEM format.

    The following files are created:
        padsniff-ca-key.pem, containing the root key.
        padsniff-ca-cert.pem, containing the root certificate.
        padsniff-ca.pem, containing the root key and certificate together.

    The written filenames are returned as `pathlib.Path` objects, in the order
    enumerated above.
    """
    path = Path(directory).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)

    keyfile = path / (DEFAULT_ORG + '-ca-key.pem')
    certfile = path / (DEFAULT_ORG + '-ca-cert.pem')
    pairfile = path / (DEFAULT_ORG + '-ca.pem')
    filenames = keyfile, certfile, pairfile

    if not overwrite and any(f.exists() for f in filenames):
        return ()

    key, ca = generate_root_pair(organization, common_name, expiry)

    # mitmproxy also generates Diffie-Hellman parameters, but this is
    # both unsupported by pyOpenSSL (as of v16.2.0), and takes forever
    # to generate with `openssl dhparam`, so we'll just let mitmproxy
    # handle it

    with open(keyfile, 'wb') as f:
        f.write(key)

    with open(certfile, 'wb') as f:
        f.write(ca)

    with open(pairfile, 'wb') as f:
        f.write(key)
        f.write(ca)

    return filenames
