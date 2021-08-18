import logging


def returns_notes_logger():
    """
    this method is used to create and configure logger
    :return: returns configured logger
    """
    log_file_format = '%(asctime)s %(message)s {%(pathname)s:%(lineno)d}'
    notes_logger = logging.getLogger("another")
    notes_log_handler = logging.FileHandler('notes_error_files.log', mode='w')
    notes_log_handler.setLevel(logging.DEBUG)
    notes_log_handler.setFormatter(logging.Formatter(log_file_format))
    notes_logger.addHandler(notes_log_handler)
    return notes_logger


notes_log = returns_notes_logger()
