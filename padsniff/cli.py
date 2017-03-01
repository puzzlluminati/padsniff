from importlib.util import module_from_spec, spec_from_file_location
import logging

import click

from .proxy import Proxy


log = logging.getLogger(__name__)


def configure_logging(verbosity):
    level = logging.ERROR - verbosity * 10
    logging.basicConfig(format='[%(levelname)s] :: %(message)s', level=level)


def load_script(path):
    spec = spec_from_file_location('script', path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    log.info('Loaded script %s.', path)


@click.group()
@click.version_option(message='%(version)s')
def cli():
    """Padsniff: A Puzzle & Dragons HTTP Sniffer"""


@cli.command()
@click.option('--port', '-p', default=8080, help='Proxy service port.')
@click.option('--script', '-s', 'scripts', multiple=True, type=click.Path(exists=True),
              help='Load a Python script containing a callback. Can be supplied multiple times.')
@click.option('--verbose', '-v', 'verbosity', count=True,
              help='Increase logging level (default: ERROR). Can be supplied multiple times.')
def run(port, scripts, verbosity):
    """Run the proxy service."""
    configure_logging(verbosity)

    # load scripts before instantiating the proxy to allow the use of the `on` decorator
    for path in scripts:
        load_script(path)

    proxy = Proxy(host='0.0.0.0', port=port)
    proxy.run()
