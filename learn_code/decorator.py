#!/usr/bin/env python3
import functools
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

logger.addHandler(sh)


def log(text):
    '''
    A decorator can have parameter or not

    >>> @log
    ... def test_def():
    ...   print('2017-8-8')
    ...
    >>> test_def()
    begin test_def:
    2017-8-8
    end test_def
    >>> @log('run')
    ... def test_def1():
    ...   print('2017-8-8:1')
    ...
    >>> test_def1()
    begin run test_def1:
    2017-8-8:1
    end call run test_def1
    '''
    if isinstance(text, str):

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                print('begin %s %s:' % (text, func.__name__))
                func(*args, **kw)
                print('end call %s %s' % (text, func.__name__))

            return wrapper

        return decorator

    else:

        @functools.wraps(text)
        def wrapper(*args, **kw):
            print('begin %s:' % text.__name__)
            text(*args, **kw)
            print('end %s' % text.__name__)

        return wrapper


if __name__ == "__main__":
    import doctest
    doctest.testmod()
