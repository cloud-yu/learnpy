import logging

__all__ = [
    'logger', 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET', 'StreamHandler',
    'Formatter', 'Filter'
]

# 定义变量
CRITICAL = logging.CRITICAL
FATAL = CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

StreamHandler = logging.StreamHandler
Formatter = logging.Formatter
Filter = logging.Filter
# def should_log(record):
#     if record.levelno <= logging.INFO:
#         return False
#     return True

# 生成一个日志对象
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
sh = StreamHandler()
sh.setLevel(logging.INFO)

formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
# sh.format("%%(names)s: [%(levelname)s] %(message)s")
sh.setFormatter(formatter)

# ft = logging.Filter()
# ft.filter = should_log

# sh.addFilter(ft)
logger.addHandler(sh)

if __name__ == '__main__':
    logger.debug('dbg_msg')
    logger.info('info_msg')
    logger.warn('warn_msg')
    logger.error('err_msg')
    logger.fatal('fatal_msg')
    logger.critical('crit_msg')

    def funca():
        funlog = logger.getChild('funca')
        print(type(funlog))
        funlog.error('test log funca')
        print("logger %s's parent is %s" % (funlog.name, funlog.parent.name))

    funca()
    print(dir(logger))
