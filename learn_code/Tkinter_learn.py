from tkinter import Tk, Button, X
from functools import partial as pto
from tkinter.messagebox import showinfo, showwarning, showerror

WARN = 'warn'
CRIT = 'crit'
REGU = 'regu'

SIGNS = {
    'do not enter': CRIT,
    'railroad crossing': WARN,
    '55 speed limit': REGU,
    'wrong way': CRIT,
    'merging traffic': WARN,
    'one way': REGU
}


# critCB = lambda: showerror('ERROR', 'Error Button Pressed!')
def critCB():
    showerror('ERROR', 'Error Button Pressed!')


warnCB = lambda: showwarning('WARNING', 'Warning Button Pressed!')
infoCB = lambda: showinfo('INFO', 'Info Button Pressed!')

top = Tk()
top.title('Road Signs')
Button(top, text='QUIT', command=top.quit, background='red', fg='white').pack()

MyButton = pto(Button, top)
CritButton = pto(MyButton, command=critCB, bg='white', fg='red')
WarnButton = pto(MyButton, command=warnCB, bg='goldenrod1')
ReguButton = pto(MyButton, command=infoCB, bg='white')

for eachSign in SIGNS:
    signType = SIGNS[eachSign]
    cmd = '%sButton(text=%r%s).pack(fill=X, expand=True)' % (signType.title(), eachSign, '.upper()'
                                                             if signType == CRIT else '.title()')
    eval(cmd)

top.mainloop()
