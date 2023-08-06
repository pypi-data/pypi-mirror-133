"""Docker technology"""
# pylint: disable=import-error
import click  # type: ignore
import click_pathlib  # type: ignore

from .interfaces import Configuration
from .docker import Controller


@click.command()
@click.option(
    "--repository",
    default=".",
    type=click_pathlib.Path(exists=True),
    help="The repository checkout to mount in the devcontainer",
)
@click.option(
    "--location",
    default="./.devcontainer",
    type=click_pathlib.Path(exists=True),
    help="The location of the devcontainer definition",
)
def run(repository, location):
    """Manage the devcontainer"""
    config = Configuration(location=location, repository=repository)
    controller = Controller(config)
    controller.run()


if __name__ == "__main__":
    run()  # pylint: disable=no-value-for-parameter
