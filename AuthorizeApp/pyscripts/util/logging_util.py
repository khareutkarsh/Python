"""
This is where the logger is initialized
"""
import logging


# Initialize the logger
def get_logger(level=logging.INFO):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(module)s[%(filename)s:%(lineno)d] %(message)s',
        datefmt='%y/%d/%m %H:%M:%S',
        level=level)
    return logging
