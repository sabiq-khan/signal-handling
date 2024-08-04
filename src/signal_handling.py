#!/usr/bin/env python3
from logging import INFO, Formatter, Logger, StreamHandler
import signal
import sys
import time

LOGGER: Logger = Logger("signal_handling")
LOGGER.setLevel(INFO)
HANDLER = StreamHandler(sys.stdout)
HANDLER.setLevel(INFO)
FORMATTER = Formatter(
    "[%(asctime)s][%(name)s][%(filename)s:%(lineno)d][%(funcName)s][%(levelname)s]: %(message)s")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)


class SignalHandlingExample:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger
        self.sigterm_received: bool = False
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum, frame):
        self.sigterm_received = True

    def _terminate_gracefully(self):
        self.logger.info("Signal received, commencing graceful termination...")
        for i in range(10, 0, -1):
            LOGGER.info(f"{i} seconds remaining till termination...")
            time.sleep(1)
        
        self.logger.info("Terminating...")
    
    def run_main_loop(self):
        while not self.sigterm_received:
            self.logger.info("Currently no SIGTERM or SIGINT received. Proceeding with normal operation...")
            time.sleep(1)
        
        self._terminate_gracefully()

def main():
    signal_handling_example: SignalHandlingExample = SignalHandlingExample(logger=LOGGER)
    signal_handling_example.run_main_loop()


if __name__ == "__main__":
    main()