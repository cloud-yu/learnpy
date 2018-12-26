import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import os
import numpy as np
from PIL import Image
# from scipy.misc import imread
curdir = os.path.dirname(__file__)
text = open(os.path.join(curdir, 'page10.txt'), 'rb').read()

wordlist = jieba.cut(text, cut_all=True)
wl = ' '.join(wordlist)

with open(os.path.join(curdir, 'aftercut.txt'), 'w+') as f:
    f.writelines(wl)

picmask = np.array(Image.open(os.path.join(curdir, 'shen.png')))
wc = WordCloud(
    background_color="white",
    mask=picmask,  # imread('shen.png')
    max_words=2000,  # 最大显示字数
    stopwords=["的", "这种", "这样", "还是", "就是", "这个"],  # 停词
    font_path=r'C:\Windows\Fonts\simkai.ttf',  # 字体路径
    max_font_size=60,  # 字体最大值
    random_state=30)  # 设置有多少种随机生成状态

myword = wc.generate(wl)
wc.to_file(os.path.join(curdir, 'result.jpg'))

plt.imshow(myword)
plt.axis("off")

# image_colors = ImageColorGenerator(picmask, default_color=(255,255,255))
# plt.imshow(myword.recolor(color_func=image_colors), interpolation='bilinear')
# plt.axis("off")
# plt.figure()
# plt.imshow(picmask, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis("off")
# plt.show()
