import threading

balance = 0


def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(10):
        with threading.Lock() as lock:
            print('thread (%s) changing...' % threading.currentThread().name)
            change_it(n)
            print('change %s' % i)


t1 = threading.Thread(target=run_thread, args=(4, ))
t2 = threading.Thread(target=run_thread, args=(8, ))
t1.start()
t2.start()

t1.join()
t2.join()

print(balance)
