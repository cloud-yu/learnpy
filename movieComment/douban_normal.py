from urllib import request
from bs4 import BeautifulSoup as bs
import logging
import re
import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
matplotlib.rcParams['figure.figsize']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

logger.addHandler(sh)

movieurl = 'https://movie.douban.com/cinema/nowplaying/wuhan/'


# 获取网页正在播放影片列表，记录每部电影的id和title
def getNowPlayingList(movieurl):
    try:
        resp = request.urlopen(movieurl)
    except:
        logger.error('error url!')

    html_data = resp.read().decode('utf-8')

    soup = bs(html_data, 'html.parser')
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all(
        'li', class_='list-item')

    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['title'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
    return nowplaying_list


# 获取评论详情
def getCommentsById(movieId, pageNum):
    commentList = []
    if pageNum > 0:
        start = (pageNum - 1) * 20
    else:
        logger.error('pageNum must bigger than 0')
        return False

    commentUrl = 'https://movie.douban.com/subject/' + (
        movieId + '/comments?start=' + str(start) + '&limit=20')
    print(commentUrl)
    try:
        resp = request.urlopen(commentUrl)
    except:
        logger.error('no more comment page!')

    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    comment_div_list = soup.find_all('div', class_='comment')
    for item in comment_div_list:
        if item.find_all('p')[0].string is not None:
            commentList.append(item.find_all('p')[0].string)
    return commentList


# 获取前N个电影，每个电影前M页的评论
def getNmovieMpagecomment(N, M):
    # 获取正在播放电影列表
    nowpl_list = getNowPlayingList(movieurl)
    if len(nowpl_list) < N:
        logger.info('only %d movies nowplaying, set N to %d' %
                    (len(nowpl_list), len(nowpl_list)))

        N = len(nowpl_list)
    # 循环前N个电影,每个电影前M页评论
    comm_list_all = []
    for i in range(N):
        comm_dict = {}
        comm_dict['name'] = nowpl_list[i]['title']
        movie_Id = nowpl_list[i]['id']
        com_List = []
        for i in range(M):
            num = i + 1
            com_list_temp = getCommentsById(movie_Id, num)
            for item in com_list_temp:
                com_List.append(item)

        comm_dict['comm'] = com_List
        comm_list_all.append(comm_dict)
    return comm_list_all


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [.299, .587, .114])


def gray2bw(gray):
    for raw in range(len(gray)):
        for col in range(len(gray[raw])):
            gray[raw][col] = (0 if gray[raw][col] > 50 else 255)
    return gray


# 定义main函数
def main():
    comm_list = getNmovieMpagecomment(2, 4)
    for item in range(len(comm_list)):
        movie_dict = comm_list[item]
        movie_comment_list = movie_dict['comm']

        # 将该电影评论列表中数据转换为字符串
        comments = ''
        for k in range(len(movie_comment_list)):
            comments = comments + (str(movie_comment_list[k])).strip()

        # 使用正则表达式去除标点符号
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        filterdata = re.findall(pattern, comments)
        cleaned_comment = ''.join(filterdata)

        # 使用结巴分词进行分词
        segment = jieba.lcut(cleaned_comment)
        words_df = pd.DataFrame({'segment': segment})

        # 去掉停词, quoting=3 全不引用
        stopwords = pd.read_csv(
            "./stopwords-list/stop_words_zh_UTF-8.txt",
            index_col=False,
            quoting=3,
            sep="\t",
            names=['stopword'],
            encoding='utf-8')
        words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
        # 统计词频
        words_df = words_df.groupby(by=['segment'])['segment']
        words_stat = words_df.agg({'count'}).rename(columns={'count': "计数"})
        # words_stat = words_df.agg(["计数"])
        words_stat = words_stat.reset_index().sort_values(
            by=["计数"], ascending=False)

        # print(words_stat.head())
        img = plt.imread('/home/archie/Pictures/mm.jpg')
        mask = rgb2gray(img)
        bw = gray2bw(mask)
        bw = np.array(bw, dtype='uint32')
        # 用词云进行显示
        wordcloud = WordCloud(
            background_color='white', max_font_size=80, mask=bw)
        word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}

        # word_frequence_list = []
        # for key in word_frequence:
        #     temp = (key, word_frequence[key])
        #     word_frequence_list.append(temp)

        wordcloud = wordcloud.fit_words(word_frequence)
        # wordcloud = wordcloud.fit_words(word_frequence_list)

        plt.subplot(131)
        plt.imshow(img)
        plt.axis("off")
        plt.subplot(132)
        plt.imshow(bw, cmap='gray')
        plt.axis("off")
        plt.subplot(133)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()


if __name__ == '__main__':
    main()
