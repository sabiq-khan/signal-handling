#!/usr/bin/env python3
from constants import LOGGER
from signal_handling_example import SignalHandlingExample


def main():
    signal_handling_example: SignalHandlingExample = SignalHandlingExample(logger=LOGGER)
    signal_handling_example.run_main_loop()


if __name__ == "__main__":
    main()