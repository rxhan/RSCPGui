from logging import Logger


class RSCPFrameError(Exception):
    def __init__(self, message: str, logger: Logger):
        if message is None:
            message = self.__class__.__name__
        logger.exception(message)


class RSCPDataError(Exception):
    def __init__(self, message: str, logger: Logger):
        if message is None:
            message = self.__class__.__name__
        logger.exception(message)


class RSCPAuthenticationError(Exception):
    def __init__(self, message: str, logger: Logger):
        if message is None:
            message = self.__class__.__name__
        logger.exception(message)


class RSCPCommunicationError(Exception):
    def __init__(self, message, logger: Logger):
        if message is None:
            message = self.__class__.__name__
        logger.exception(message)
