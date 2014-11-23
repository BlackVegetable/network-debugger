import logging

logger = logging.getLogger('mytool')
handler = logging.FileHandler('/mytool.log') # create a file handler
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s') # create a logging format
handler.setFormatter(formatter)
logger.addHandler(handler) # add it to the handler
logger.setLevel(logging.info)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')# not sure if we will need that
logger.error('error message')# not sure if we will need that 
logger.critical('critical message') # not sure if we will need that




