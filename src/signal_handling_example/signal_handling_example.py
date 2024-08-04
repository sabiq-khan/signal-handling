from logging import Logger
import signal
import time
from types import FrameType


class SignalHandlingExample:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger
        self.terminating_signal_received: bool = False
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum: int, frame: FrameType):
        self.logger.info(f"Received signal {signum}!")
        self.terminating_signal_received = True

    def _terminate_gracefully(self):
        self.logger.info("Commencing graceful termination...")
        for i in range(10, 0, -1):
            self.logger.info(f"{i} seconds remaining till termination...")
            time.sleep(1)
        
        self.logger.info("Terminating...")
    
    def run_main_loop(self):
        while not self.terminating_signal_received:
            self.logger.info("Currently no SIGTERM or SIGINT received. Proceeding with normal operation...")
            time.sleep(1)
        
        self._terminate_gracefully()
