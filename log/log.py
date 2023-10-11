import logging
import colorlog


class CustomLogger:
    def __init__(self, log_file_name):
        self.logger = self.setup_logger(log_file_name)

    def setup_logger(self, log_file_name):
        root_logger = logging.getLogger()
        if root_logger.handlers:
            for handler in root_logger.handlers:
                root_logger.removeHandler(handler)

        logger = colorlog.getLogger()
        logger.setLevel(logging.DEBUG)

        console_handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(log_file_name, mode='w')
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s')
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    custom_logger = CustomLogger()
    logger = custom_logger.get_logger()
    logger.info("This is an example info message.")
    logger.debug("This is an example debug message.")
