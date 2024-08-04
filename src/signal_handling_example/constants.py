from logging import INFO, Formatter, Logger, StreamHandler
import sys

LOGGER: Logger = Logger("signal_handling")
LOGGER.setLevel(INFO)
HANDLER = StreamHandler(sys.stdout)
HANDLER.setLevel(INFO)
FORMATTER = Formatter(
    "[%(asctime)s][%(name)s][%(filename)s:%(lineno)d][%(funcName)s][%(levelname)s]: %(message)s")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
