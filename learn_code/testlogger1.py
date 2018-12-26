# -*- coding:utf-8 -*-
import logging
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf8')

logger = logging.getLogger()
# logger的setlevel决定哪些等级的日志会被送到handler进行处理
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
# handler的setlevel决定这个handler会处理哪些等级的日志，其他等级的将被handler忽略
sh.setLevel(logging.INFO)
fmtter = logging.Formatter('')

ft = logging.Filter

logger.addHandler(sh)


class Person:

    def __init__(self, name, gender, age, power):
        self.__name = name
        self.__gender = gender
        self._age = age
        self.power = power

    def grassbattle(self):
        logger.info('草丛战斗，战力 -200')
        self.power -= 200
        return self.power

    def exercise(self):
        logger.info('自我修炼，战力 +100')
        self.power += 100
        return self.power

    def groupbattle(self):
        logger.error('多人战斗，战力 -500')
        self.power -= 500
        return self.power

    def brief(self):
        logger.info('当前状态：')
        logger.info('姓名：%s, 性别：%s, 年龄：%d, 战力：%d' % (self.__name, self.__gender, self._age, self.power))


if __name__ == '__main__':
    cang = Person('aoi sola', 'female', 18, 1000)
    cang.exercise()
    cang.groupbattle()
    cang.brief()
    logger.info('这是中文')
