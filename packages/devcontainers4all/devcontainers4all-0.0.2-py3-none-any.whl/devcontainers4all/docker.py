"""Docker container backend
"""
import io
from dataclasses import dataclass
from pathlib import Path

import pexpect
from logzero import setup_logger

import docker

from .factories import ContainerBuilderFactory, DevContainerFactory
from .interfaces import Configuration, ContainerBuilder, ContainerTech
from .utils import stream_load

# pylint: disable=too-few-public-methods


class Builder(ContainerBuilder):
    """Container builder"""

    type = ContainerTech.DOCKER

    def __init__(self, location: Path, base_url="unix://var/run/docker.sock") -> None:
        super().__init__()
        self.__client = docker.APIClient(base_url=base_url)
        self.__logger = setup_logger(name="Builder")
        self.__location = location

    def build(self, buildargs: dict, tag: str) -> str:
        """Build the container"""
        builder = self.__client.build(
            str(self.__location), buildargs=buildargs, tag=tag, rm=False, nocache=False
        )

        # consume the builder's steps and send its output to the logger

        for build_out in builder:
            steps = stream_load(io.BytesIO(build_out))

            for step in steps:
                if "stream" not in step:
                    continue

                for line in step["stream"].splitlines():
                    if not line:
                        continue
                    self.__logger.debug(line)

        return tag


class Runner:
    """Docker Runner"""

    def __init__(
        self, config: Configuration, base_url="unix://var/run/docker.sock"
    ) -> None:
        self.__client = docker.DockerClient(base_url=base_url)
        self.__config = config
        self.__logger = setup_logger(name="Runner")

    def run(self, image_id: str):
        """Run"""
        manifest = DevContainerFactory(self.__config)
        post_create_command = manifest.get("build").get("postCreateCommand")

        volumes = {
            Path(self.__config.repository).resolve(): {
                "bind": "/workspace",
                "mode": "rw",
            }
        }
        self.__logger.debug(f"Using volumes {volumes}")

        container = self.__client.containers.create(
            image_id,
            tty=True,
            detach=True,
            command="/bin/bash",
            stdin_open=True,
            volumes=volumes,
        )
        container.start()
        # attach via CLI: managing the terminal is too complex for now
        attached_container = pexpect.spawn(f"docker attach {container.id}")

        try:
            if post_create_command:
                attached_container.sendline(post_create_command)
            attached_container.interact()
        finally:
            container.stop()
            container.remove()


class Controller:
    """Control the process"""

    def __init__(self, configuration: Configuration) -> None:
        self.__config = configuration
        self.__logger = setup_logger(name="Controller")

    def run(self):
        """Execute controller"""
        devcontainer = DevContainerFactory(self.__config)
        builder = ContainerBuilderFactory(self.__config)

        args = devcontainer.get("build").get("args")
        image_name = builder.build(buildargs=args, tag="devcontainers4all_test")

        runner = Runner(config=self.__config)
        self.__logger.info(f"Executing {image_name} in container")
        runner.run(image_id=image_name)
