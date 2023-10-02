import logging


class Logger:
    def __init__(
            self,
            name: str,
            user_name: str = 'username',
            log_path: str = 'logs/log.log',
            log_format: str = f'[%(levelname)s] - %(asctime)s - %(username)s - %(name)s - '
                              f'(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    ):
        self.name = name
        self.user_name = user_name
        self.log_path = log_path
        self.log_format = log_format

    def get_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        logger.addHandler(self.__get_file_handler(
            log_path=self.log_path,
            log_format=self.log_format)
        )
        logger.addHandler(self.__get_stream_handler(self.log_format))
        logger = logging.LoggerAdapter(logger, {'username': self.user_name})

        return logger

    @staticmethod
    def __get_file_handler(log_path: str, log_format: str):
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter(log_format))

        return file_handler

    @staticmethod
    def __get_stream_handler(log_format: str):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(log_format))

        return stream_handler
