def move(a, c, step):
    print("step", step, ": move", a, "-->", c)


def hanoi(n, a='A', b='B', c='C', step=1):
    if n == 1:
        move(a, c, step)
    if n > 1:
        hanoi(n - 1, a, c, b, step)
        step = step + 2**(n - 1) - 1
        move(a, c, step)
        step += 1
        hanoi(n - 1, b, a, c, step)


# main
t = int(input('输入汉诺塔层数：'))
print('计算结果如下：')
hanoi(t)
