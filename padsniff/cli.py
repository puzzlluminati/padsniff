from importlib.util import module_from_spec, spec_from_file_location
import logging

import click

from .proxy import Proxy


def load_logging(level):
    logging.basicConfig()
    logging.getLogger().setLevel(level)


def load_script(path):
    spec = spec_from_file_location('script', path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--debug', '-d', default=False, is_flag=True)
@click.option('--port', '-p', default=8080)
@click.option('--script', '-s', multiple=True, type=click.Path(exists=True))
def run(debug, port, script):

    load_logging(logging.DEBUG if debug else logging.WARNING)

    # load scripts before instantiating the proxy to allow the use of the `on` decorator
    for path in script:
        load_script(path)

    proxy = Proxy(host='0.0.0.0', port=port)
    proxy.run()
