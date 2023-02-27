from loguru import logger


class Logger():

    def __init__(self, need_log=True, log_file='./report/debug.log'):
        self.my_logger = logger

        # 判断是否需要写入日志
        if need_log is True:
            self.my_logger.add(log_file)

    def info(self, content):
        """
            info日志
        """
        self.my_logger.info(content)

    def debug(self, content):
        """
            debug日志
        """
        self.my_logger.debug(content)

    def error(self, content):
        """
            error日志
        """
        self.my_logger.error(content)

    def critical(self, content):
        """
            critical日志
        """
        self.my_logger.critical(content)


if __name__ == "__main__":
    logger = Logger(log_file='./123.log')
    logger.info("12312312")
    logger.error("12312312")
    logger.debug("12312312")
    logger.critical("12312312")