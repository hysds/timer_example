#!/usr/bin/env python
"""
Example of an evaluator job with a configurable timer.
"""
import os
import json
import argparse
import backoff
import logging


# set logger
log_format = "[%(asctime)s: %(levelname)s/%(name)s/%(funcName)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)


class LogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "id"):
            record.id = "--"
        return True


logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
logger.setLevel(logging.INFO)
logger.addFilter(LogFilter())


# backoff configuration
BACKOFF_CONF = {}


def lookup_max_value():
    """Runtime configuration of backoff max_value."""
    return BACKOFF_CONF["max_value"]


def lookup_max_time():
    """Runtime configuration of backoff max_time."""
    return BACKOFF_CONF["max_time"]


def check_condition(path, count):
    """
    Check condition and dump out state config of current state.
    Return True if condition is met, False otherwise.
    """

    files = os.listdir(path)
    found = len(files)
    logger.info("found: {}".format(found))
    logger.info("files: {}".format(files))
    with open("state_config.json", "w") as f:
        json.dump(
            {"files": files, "success": count == found}, f, indent=2, sort_keys=True
        )
    return count == found


class ConditionNotMetError(Exception):
    pass


@backoff.on_exception(
    backoff.expo,
    ConditionNotMetError,
    max_value=lookup_max_value,
    max_time=lookup_max_time,
)
def evaluate(path, count):
    """Evaluate conditions. Raise error if not met."""

    if check_condition(path, count):
        logger.info("Conditions met.")
    else:
        raise ConditionNotMetError("Conditions not met.")


def main(path, count):
    """Evaluate conditions until they are met or the time out has been reached."""

    try:
        evaluate(path, count)
    except ConditionNotMetError as e:
        logger.error(str(e))
        logger.error("Continuing on without non-zero exit code.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="directory to monitor for files")
    parser.add_argument("count", type=int, help="number of files to expect")
    parser.add_argument(
        "--max_value", type=int, default=13, help="maximum backoff time"
    )
    parser.add_argument("--max_time", type=int, default=60, help="maximum total time")
    args = parser.parse_args()
    BACKOFF_CONF["max_value"] = args.max_value
    BACKOFF_CONF["max_time"] = args.max_time
    main(args.path, args.count)
