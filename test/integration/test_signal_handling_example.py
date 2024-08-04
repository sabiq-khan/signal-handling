import signal
from typing import Optional
import unittest
import os
import sys
import time
import subprocess
from subprocess import Popen, PIPE
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)


class TestSignalHandlingExample(unittest.TestCase):
    def setUp(self):
        self.signal_handling_example: Popen = subprocess.Popen(
            [
                "/usr/bin/env",
                "python3",
                "src/signal_handling_example/main.py"
            ],
            shell=False,
            stdout=PIPE,
            stderr=PIPE,
        )

        # Giving process time to start
        time.sleep(2)
    
    def tearDown(self):
        self.signal_handling_example.stdout.close()
        self.signal_handling_example.stderr.close()
        self.signal_handling_example.terminate()

    def test_signal_handling_example(self):
        self.signal_handling_example.send_signal(signal.SIGINT)
        # Waiting for graceful termination to complete
        time.sleep(11)

        return_code: Optional[int] = self.signal_handling_example.poll()
        if return_code is not None:
            stdout, stderr = self.signal_handling_example.communicate()
            if return_code != 0:
                error: str = bytes(stderr).decode("utf-8")
                raise ChildProcessError(error)
            else:
                output: str = bytes(stdout).decode("utf-8")
                assert f"Received signal {signal.SIGINT}" in output
                assert "Commencing graceful termination..." in output
                assert "10 seconds remaining till termination..." in output
                assert "1 seconds remaining till termination..." in output
                assert "Terminating..." in output


if __name__ == "__main__":
    unittest.main()
    