from atexit import register
from random import randrange
from threading import BoundedSemaphore, Lock, Thread
from time import sleep, ctime

lock = Lock()
MAX = 5
candytrace = BoundedSemaphore(MAX)


def refill():
    lock.acquire()
    print('>>>Refilling candy...')
    try:
        candytrace.release()
    except ValueError:
        print('\tfull, skipping')
    else:
        print('\tOK, candy remains %d' % candytrace._value)
    lock.release()


def buy():
    lock.acquire()
    print('>>>Buying candy...')
    if candytrace.acquire(False):
        print('\tOK, candy remains %d' % candytrace._value)
    else:
        print('\tempty, skipping')
    lock.release()


def producer(loops):
    for i in range(loops):
        refill()
        sleep(randrange(3))


def consumer(loops):
    for i in range(loops):
        buy()
        sleep(randrange(3))


def main():
    print('[===]starting at: %s' % ctime())
    nloops = randrange(2, 6)
    print('[===]THE CANDY MACHINE (full with %d bars)![===]' % MAX)
    Thread(target=consumer, args=(randrange(nloops, nloops + 2 + MAX), )).start()
    Thread(target=producer, args=(nloops, )).start()


@register
def _atexit():
    print('[===]ALL DONE at: %s' % ctime())


if __name__ == '__main__':
    main()