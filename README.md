## Signal Handling Example
This example program demonstrates how to handle [signals](https://man7.org/linux/man-pages/man7/signal.7.html) in Python code. 

## Explanation
By default, when a program receives a `SIGTERM` or `SIGINT` from the kernel, it is immediately terminated. However, if the program catches and handles the signal instead, it can run some last-minute operations and terminate gracefully.

A program can catch a signal if it has a signal handler function defined containing the operations it needs to perform when a signal is received. The program must then invoke the [signal()](https://man7.org/linux/man-pages/man2/signal.2.html) or [sigaction()](https://man7.org/linux/man-pages/man2/sigaction.2.html) system call, passing the signal to be handled and the handler function as arguments, in order to make the kernel aware that the program will gracefully handle the signal.

The [signal()](https://docs.python.org/3/library/signal.html#signal.signal) method from the Python [signal](https://docs.python.org/3/library/signal.html) library provides a means of invoking this functionality.

## Usage
An instance of the `SignalHandlingExample` class defined in [signal_handling_example.py](./src/signal_handling_example/signal_handling_example.py) runs continuously until it receives a `SIGTERM` or `SIGINT`. Upon receiving one of these signals, the program counts down 10 seconds before terminating.

[main.py](./src/signal_handling_example/main.py) is the entrypoint of the program. If it is run from the shell, a `SIGINT` can be induced by hitting `Ctrl-C`. Alternatively, in a separate terminal tab, the PID of the running program can be found with `ps -ef` and a `SIGINT` or `SIGTERM` can be sent with the `kill` command.

There is also a [Dockerfile](./Dockerfile) for a container image build, to demonstrate that this signal handling still applies when the process is running in a container. While the previous methods of sending a signal still apply, the Docker [/containers/{id}/stop](https://docs.docker.com/engine/api/v1.45/#tag/Container/operation/ContainerStop) API provides another means of sending a terminating signal to a container. This API can be invoked with the [docker stop](https://docs.docker.com/reference/cli/docker/container/stop/) CLI command and the [Container.stop()](https://docker-py.readthedocs.io/en/stable/containers.html) method from the Docker Python SDK. While invoking this API results in Docker sending a `SIGTERM` to the container by default, other signals can be passed as parameters.

## Tests
There are unit and integration tests defined in the [test](./test) directory as well as configurations for running them with the VS Code debugger defined in [.vscode/launch.json](./.vscode/launch.json). In addition to verifying that signals are being handled as expected, these tests can be used to pause the execution of the program and step through it.

`Unit Test: SignalHandlingExample` tests the output of methods from the `SignalHandlingExample` class containing the core logic of the program.

`Integration Test: SignalHandlingExample` creates and runs an instance of the `SignalHandlingExample` class to ensure that signal trapping and graceful termination are performed correctly.

`E2E Test: main.py` runs the program from its entrypoint at [main.py](./src/signal_handling_example/main.py). There are no assertions in this test, but the execution of the progarm can still be paused for inspection.

`E2E Test: Docker` builds a container image with the [Dockerfile](./Dockerfile), starts a running container, and then calls the [/containers/{id}/stop](https://docs.docker.com/engine/api/v1.45/#tag/Container/operation/ContainerStop) API to send a `SIGTERM` to the container. It contains assertions to verify that the signal is handled correctly.
