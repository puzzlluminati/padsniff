from contextlib import suppress
from os import remove
from os.path import dirname, join

from OpenSSL.crypto import load_certificate, FILETYPE_PEM
import pytest

from padsniff.certs import generate_cert_files


FILENAMES = 'padsniff-ca.pem', 'padsniff-ca-cert.pem', 'padsniff-ca-key.pem'
HERE = dirname(__file__)


@pytest.fixture(autouse=True)
def cleanup():
    """Delete generated files after each test."""
    yield

    for filename in FILENAMES:
        path = join(HERE, filename)

        with suppress(FileNotFoundError):
            remove(path)


class TestCertGeneration:


    def test_subject(self):
        """Test certificate subject customization."""
        org, cn = 'test org', 'test name'
        _, certfile, _ = generate_cert_files(HERE, organization=org, common_name=cn)

        with open(certfile, 'rb') as f:
            certdata = f.read()

        cert = load_certificate(FILETYPE_PEM, certdata)
        subject = cert.get_subject()
        assert subject.O == org
        assert subject.CN == cn


    def test_no_overwrite(self):
        """Test certificate generation does not overwrite files by default."""
        expected = {join(HERE, filename) for filename in FILENAMES}

        generated = {str(path) for path in generate_cert_files(HERE)}
        assert generated == expected

        generated2 = generate_cert_files(HERE)
        assert not generated2


    def test_overwrite(self):
        """Test certificate generation does overwrite when specified."""
        expected = {join(HERE, filename) for filename in FILENAMES}

        generated = {str(path) for path in generate_cert_files(HERE)}
        assert generated == expected

        generated2 = {str(path) for path in generate_cert_files(HERE, overwrite=True)}
        assert set(generated2) == expected
