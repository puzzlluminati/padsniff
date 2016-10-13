from importlib.util import module_from_spec, spec_from_file_location
import logging

import click

from .proxy import Proxy


log = logging.getLogger(__name__)


def configure_logging(level):
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
@click.option('--debug', '-d', default=False, is_flag=True)
@click.option('--port', '-p', default=8080)
@click.option('--script', '-s', multiple=True, type=click.Path(exists=True))
def run(debug, port, script):

    configure_logging(logging.DEBUG if debug else logging.WARNING)

    # load scripts before instantiating the proxy to allow the use of the `on` decorator
    for path in script:
        load_script(path)

    proxy = Proxy(host='0.0.0.0', port=port)
    proxy.run()
