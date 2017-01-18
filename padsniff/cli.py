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
def cli():
    pass


@cli.command()
@click.option('--port', '-p', default=8080)
@click.option('--script', '-s', 'scripts', multiple=True, type=click.Path(exists=True))
@click.option('--verbose', '-v', 'verbosity', count=True)
def run(port, scripts, verbosity):
    configure_logging(verbosity)

    # load scripts before instantiating the proxy to allow the use of the `on` decorator
    for path in scripts:
        load_script(path)

    proxy = Proxy(host='0.0.0.0', port=port)
    proxy.run()
