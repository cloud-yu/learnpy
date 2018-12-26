import logging
import sys
import os


def should_log(record):
    if record.levelno <= logging.INFO:
        return False
    return True


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# print("logger %s's parent is %s" % (logger.name, logger.parent.name))
# print("logger %s's root is %s" % (logger.name, logger.root.name))
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
# sh.format("%%(names)s: [%(levelname)s] %(message)s")
sh.setFormatter(formatter)

ft = logging.Filter()
ft.filter = should_log

sh.addFilter(ft)
logger.addHandler(sh)

logger.debug('dbg_msg')
logger.info('info_msg')
logger.warn('warn_msg')
logger.error('err_msg')
logger.fatal('fatal_msg')
logger.critical('crit_msg')


def funca():
    funlog = logging.getLogger('funca')
    funlog.error('test log funca')


funca()
print(os.getcwd())
sys.path.append(os.getcwd())
print(sys.path)
