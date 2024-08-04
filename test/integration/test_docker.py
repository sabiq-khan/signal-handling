import os
import signal
import sys
import unittest
import time
from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container
from typing import List
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)

IMAGE_NAME: str ="signal-handling-example"
DOCKERFILE: str = "Dockerfile"
CONTAINER_APP_ROOT: str = f"/app"
ENTRYPOINT: List[str] = ["/usr/bin/env", "python3", "main.py"]


class TestDocker(unittest.TestCase):
    def setUp(self):
        self.docker_client: DockerClient = DockerClient()

        image: Image = self.docker_client.images.build(path=WORKSPACE_ROOT, dockerfile=DOCKERFILE, tag=IMAGE_NAME)[0]
        assert image.tags[0] == f"{IMAGE_NAME}:latest"
        assert image.attrs["ContainerConfig"]["WorkingDir"] == CONTAINER_APP_ROOT
        assert image.attrs["ContainerConfig"]["Entrypoint"] == ENTRYPOINT
        assert image.attrs["Size"] < 60000000

        self.container: Container = self.docker_client.containers.run(image=IMAGE_NAME, detach=True)
        time.sleep(2)

    def tearDown(self):
        self.container.remove(force=True)
        self.docker_client.containers.prune()
        self.docker_client.images.prune()

    def test_graceful_termination(self):
        # Adds margin of error to Docker's default timeout
        self.container.stop(timeout=12)
        # Waiting for graceful termination to complete
        time.sleep(11)
        logs: str = bytes(self.container.logs()).decode("utf-8")
        assert f"Received signal {signal.SIGTERM}" in logs
        assert "Commencing graceful termination..." in logs
        assert "10 seconds remaining till termination..." in logs
        assert "1 seconds remaining till termination..." in logs
        assert "Terminating..." in logs


if __name__ == "__main__":
    unittest.main()
