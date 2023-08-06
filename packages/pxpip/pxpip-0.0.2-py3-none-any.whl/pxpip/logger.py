import logging
import os

import sys
from datetime import datetime

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def logger(logger_name, log_level=LOG_LEVEL):
    logging.basicConfig()
    logger_obj = logging.getLogger(logger_name)
    logger_obj.propagate = False

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(LogFormatter())

    logger_obj.addHandler(log_handler)
    logger_obj.setLevel(log_level)

    return logger_obj


class LogFormatter(logging.Formatter):
    """
    Custom formatter for logging.logger instances
    """
    LOG_ATTRS = {"created", "levelname", "msg", "name"}
    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self):
        super(LogFormatter, self).__init__()
        self.extended = (LOG_LEVEL == "DEBUG")

    def format(self, record) -> str:
        """
        Used by logger instance to parse a log record and print an alternative string
        """

        obj = {attr: getattr(record, attr) for attr in self.LOG_ATTRS}
        obj["msg"] = obj.get("msg") % record.args if record.args else obj.get("msg")
        new_asctime = datetime.fromtimestamp(obj["created"]).strftime(self.DATE_TIME_FORMAT)[:-3]
        del obj["created"]
        return (
            obj['msg'] if not self.extended
            else
            f"{new_asctime} || {obj['name']} || {obj['levelname']} || {obj['msg']} "
        )
