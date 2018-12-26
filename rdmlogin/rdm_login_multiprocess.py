from multiprocessing import Pool
from math import ceil
from rdm_login import login, select_task, fill_tasklog, process
import os
import json

if __name__ == '__main__':
    url = r'http://rdmprd.fiberhome.com.cn/main.do'

    jsfilepath = os.path.join(os.path.split(os.path.realpath(__file__))[0], r'rdmtask.json')

    with open(jsfilepath, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    task = []
    for i in range(len(data)):
        for j in range(len(data[i]['taskdiary'])):
            task.append({'taskid': data[i]['taskid'], 'taskdiary': data[i]['taskdiary'][j]})

    ncore = os.cpu_count()
    tasklen = len(task)
    if tasklen >= ncore:
        p = Pool(ncore)
        slilen = ceil(tasklen / ncore)
        tasksli = []
        for i in range(ncore):
            tasksli.append(task[slilen * i:slilen * (i + 1)])
        for i in range(ncore):
            print('start Total %d subprocess, %dth process fill %d days...' % (ncore, i + 1, len(tasksli[i])))
            p.apply_async(process, args=(tasksli[i], url))
    else:
        p = Pool(tasklen)
        print('start Total %d process...' % tasklen)
        tasksli = []
        for i in range(tasklen):
            tasksli.append(task[i:i + 1])

        for i in range(tasklen):
            print('this is the %dth process one date: ...' % (i + 1))
            p.apply_async(process, args=(tasksli[i], url))

    print('wait for all subprocess done...')
    p.close()
    p.join()
    print('All process done!')
