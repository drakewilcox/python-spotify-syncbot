import logging
from logging.handlers import RotatingFileHandler

def configure_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logFile = 'sync_log.txt'
    logHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                     backupCount=2, encoding=None, delay=0)
    logHandler.setFormatter(log_formatter)
    logHandler.setLevel(logging.INFO)

    appLogger = logging.getLogger('root')
    appLogger.setLevel(logging.INFO)
    appLogger.addHandler(logHandler)
    return appLogger