import logging

from logging_module.context import correlation_id


class ContextFilter(logging.Filter):
    """"Provides correlation id parameter for the logger"""

    def filter(self, record):
        record.correlation_id = correlation_id.get()
        return True


logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)-15s %(name)-5s %(levelname)-8s %(correlation_id)s %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)

file_handler = logging.FileHandler(filename='logs/Migration.log')
file_handler.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(file_handler)

logger.addFilter(ContextFilter())
