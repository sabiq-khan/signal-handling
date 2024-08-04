from logging import Logger
import signal
import unittest
import os
import sys
import time
from unittest.mock import MagicMock
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)
from src.signal_handling_example.signal_handling_example import SignalHandlingExample
from src.signal_handling_example.constants import LOGGER


class TestSignalHandlingExample(unittest.TestCase):
    def setUp(self):
        logger: Logger = LOGGER
        logger.name = "test_signal_handling_example"
        self.signal_handling_example: SignalHandlingExample = SignalHandlingExample(logger=logger)

    def test_handle_signal_sigint(self):
        self.signal_handling_example._handle_signal(signum=signal.SIGINT, frame=MagicMock())
        assert self.signal_handling_example.terminating_signal_received

    def test_handle_signal_sigterm(self):
        self.signal_handling_example._handle_signal(signum=signal.SIGTERM, frame=MagicMock())
        assert self.signal_handling_example.terminating_signal_received

    def test_terminate_gracefully(self):
        start_time: float = time.time()
        self.signal_handling_example._terminate_gracefully()
        end_time: float = time.time()

        # Checking that run time was ~10 seconds
        run_time: float = end_time - start_time
        assert run_time//1 == 10.0


if __name__ == "__main__":
    unittest.main()
