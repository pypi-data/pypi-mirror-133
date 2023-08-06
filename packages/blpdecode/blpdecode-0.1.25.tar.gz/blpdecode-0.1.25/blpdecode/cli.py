"""Console script for blpdecode."""

import sys

import click

from .blpdecode import decode


@click.command("blpdecode")
@click.version_option()
@click.option("-d", "--debug", is_flag=True, help="debug mode")
@click.argument("encoded-url", type=str)
def cli(debug, encoded_url):
    def exception_handler(
        exception_type, exception, traceback, debug_hook=sys.excepthook
    ):

        if debug:
            debug_hook(exception_type, exception, traceback)
        else:
            click.echo(f"{exception_type.__name__}: {exception}", err=True)

    sys.excepthook = exception_handler

    click.echo(decode(encoded_url))
    return 0


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
