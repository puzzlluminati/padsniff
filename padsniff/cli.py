from importlib.util import module_from_spec, spec_from_file_location
import logging

import click

from .certs import generate_cert_files
from .constants import CADIR, DEFAULT_CN, DEFAULT_EXP, DEFAULT_ORG
from .proxy import Proxy, patch_mitmproxy_certfile_prefix


log = logging.getLogger(__name__)


def configure_logging(verbosity):
    level = logging.WARNING - verbosity * 10
    logging.basicConfig(format='[%(levelname)s] :: %(message)s', level=level)


def load_script(path):
    spec = spec_from_file_location('script', path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    log.info('Loaded script %s.', path)


@click.group()
@click.version_option(message='%(version)s')
@click.pass_context
def cli(ctx):
    """Padsniff: A Puzzle & Dragons HTTP Sniffer"""
    patch_mitmproxy_certfile_prefix()
    ctx.max_content_width = 120


@cli.command()
@click.option('--directory', '-d', default=CADIR, metavar='PATH',
              help='Directory to write files to. (default: ~/.padsniff)')
@click.option('--organization', '--org', '-o', default=DEFAULT_ORG,
              help='Organization name specified in the certificate signing request. (default: "padsniff")')
@click.option('--common-name', '--cn', '-c', default=DEFAULT_CN,
              help='Common name specified in the certificate signing request. (default: "Puzzle & Dragons HTTP Sniffer")')
@click.option('--expiry', '--exp', '-x', default=DEFAULT_EXP, metavar='SECONDS',
              help='Root certificate validity period in seconds. (default: 3 years)')
@click.option('--overwrite', '-f', is_flag=True,
              help='Overwrite certificate files if they exist.')
@click.option('--quiet', '-q', is_flag=True,
              help='Silence non-error output.')
def certs(directory, org, cn, exp, overwrite, quiet):
    """Generate a new root key and certificate."""
    filenames = generate_cert_files(directory, org, cn, exp, overwrite)

    if not quiet:
        for filename in filenames:
            click.echo(filename)


@cli.command()
@click.option('--cadir', '-d', default=CADIR, metavar='PATH',
              help='Path to directory containing certificate authority. (default: ~/.padsniff)')
@click.option('--port', '-p', default=8080,
              help='Proxy service port. (default: 8080)')
@click.option('--script', '-s', 'scripts', multiple=True, type=click.Path(exists=True),
              help='Load a Python script containing a callback. Can be supplied multiple times.')
@click.option('--verbose', '-v', 'verbosity', count=True,
              help='Increase logging level (default: WARNING). Can be supplied multiple times.')
def run(cadir, port, scripts, verbosity):
    """Run the proxy service."""
    configure_logging(verbosity)

    # load scripts before instantiating the proxy to allow the use of the `on` decorator
    for path in scripts:
        load_script(path)

    proxy = Proxy(host='0.0.0.0', port=port, cadir=cadir)
    proxy.run()
