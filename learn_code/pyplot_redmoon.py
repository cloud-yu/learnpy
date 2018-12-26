#! env python
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.set_xticks([])
ax.set_yticks([])

theta = np.arange(0, 2 * np.pi + 0.1, 2 * np.pi / 800)
# x = np.cos(theta)
# y = np.sin(theta)

v = np.linspace(0, 10, 80)
v.shape = (80, 1)
# x = v * x
# y = v * y

mx = np.max(theta)
for tha in theta:
    x1 = v * np.cos(tha)
    y1 = v * np.sin(tha)
    c = tha / mx
    plt.plot(x1, y1, color=(c, x1[0], y1[0]))

plt.style.use('ggplot')
# plt.plot(x, y, color=(0.75, 0, 0))
plt.show()
