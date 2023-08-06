from dataclasses import dataclass
from importlib import import_module

from .interfaces import (Configuration, ContainerBuilder, ContainerTech,
                         DevContainer, DevContainerProvider)
from .vsc import VisualStudioManifest

NAMESPACE = __name__.split('.')[0]

# Factory names are CamelCase even if functions
# pylint: disable=invalid-name

def DevContainerFactory(config: Configuration) -> DevContainer:
    """Obtain the DevContainer implementation requested by configuration"""
    assert config.devcontainer_provider is DevContainerProvider.VSC
    return VisualStudioManifest(
        location=config.location, manifest_file=config.manifest_file
    )


def ContainerBuilderFactory(config: Configuration) -> ContainerBuilder:
    """Obtain the ContainerBuilder implementation requested by configuration"""
    container_tech = ContainerTech(config.container_tech)
    assert container_tech is ContainerTech.DOCKER

    container_tech_module = import_module(f'{NAMESPACE}.{container_tech.name.lower()}')
    Builder = getattr(container_tech_module, 'Builder')
    return Builder(location=config.location)
