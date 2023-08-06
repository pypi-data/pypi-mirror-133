from logging import getLogger


class LoggingObject(object):
    def __init__(self, name: str):
        self._logger = getLogger(name)
