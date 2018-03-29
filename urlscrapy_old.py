# coding=utf-8
# author=XingLong Pan
# date=2016-11-07

import random
import requests
import configparser
import json
import constants
from bs4 import BeautifulSoup
from login import CookiesHelper
from utils import Utils

# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')


def fliter_movie_url(url_set, url_list):
    movie_urls = []
    for url in url_list:
        if 'subject' in url and url not in url_set:
            url_set.add(url)
            print('crawled url: %s' % url)
    return url_set


def crawl_movie_now_playing(now_playing_urls):
    ret_urls = set()
    for now_playing_url in now_playing_urls:
        headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        r = requests.get(
            now_playing_url,
            headers=headers
        )
        bs = BeautifulSoup(r.text, 'html.parser')
        nowplaying = bs.find('div', {'id':'nowplaying'})
        infos = nowplaying.find_all('a')
        fliter_movie_url(ret_urls, [info['href'] for info in infos])
    return ret_urls


def crawl_movie_up_playing(up_playing_url):
    ret_urls = set()
    headers = {'User-Agent': random.choice(constants.USER_AGENT)}
    r = requests.get(
        up_playing_url,
        headers=headers
    )
    bs = BeautifulSoup(r.text, 'html.parser')
    nowplaying = bs.find('table', {'class': 'coming_list'})
    infos = nowplaying.find_all('a')
    fliter_movie_url(ret_urls, [info['href'] for info in infos])
    return ret_urls


def crawl_movie_url_by_tag(tag, limit=10000):
    payload = {'sort': 'rank',
               'type': 'movie',
               'page_limit': '20',
               'tag': '',
               'page_start': None}
    payload['tag'] = tag
    start = 0
    count = 0
    movie_list_fn = 'urls/%s.txt' % tag
    movie_list_f = open(movie_list_fn, 'w+')
    movie_urls = []
    print(movie_list_fn)
    while True:
        payload['page_start'] = start
        headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        r = requests.get(
          constants.URL_MOVIE_TYPE_OLD,
          headers=headers,
          params=payload
        )
        start = start + 20
        r.encoding = 'utf-8'
        data_dic = json.loads(r.text)
        movie_list = data_dic['subjects']
        for movie in movie_list:
            movie_list_f.write(str(movie) + '\n')
            movie_urls.append(movie[u'url'])
        movie_list_f.flush()
        count = count + len(movie_list)
        print('tag=%s, count=%d' % (tag, count))
        if len(movie_list) == 0 or count >= limit:
            return movie_urls
            break
        Utils.Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)


if __name__ == '__main__':
    city_list = [u'beijing', u'shanghai', u'guangzhou', u'shenzhen', u'chengdu', u'wuhan', u'hangzhou', u'chongqing', u'zhengzhou', u'nanjing', u'xian', u'suzhou', u'tianjin', u'changsha', u'fuzhou', u'jinan', u'shenyang', u'hefei', u'qingdao', u'haerbin', u'wenzhou', u'xiamen', u'dalian', u'dongguan', u'changchun']
    up_playing_url = "https://movie.douban.com/coming"
    now_playing_url = "https://movie.douban.com/cinema/nowplaying/"
    tags = ["热门", "经典", "豆瓣高分"]
    all_tags = ["热门", "最新", "经典", "可播放", "豆瓣高分", "冷门佳片", "华语", "欧美", "韩国", "日本", "动作", "喜剧", "爱情", "科幻", "悬疑", "恐怖", "治愈"]
    # #爬去正在热播的电影url
    # now_playing_url_sets = crawl_movie_now_playing([now_playing_url + city for city in city_list])
    # #爬去即将上映的电影url
    # up_playing_url_set = crawl_movie_up_playing(up_playing_url)
    # playing_url_set = up_playing_url_set | up_playing_url_set
    # up_and_now_play_file = open('up_now_playing.txt', 'w')
    # for url in playing_url_set:
    #     up_and_now_play_file.write(url + '\n')
    #     up_and_now_play_file.flush()
    for tag in tags:
        movie_urls = crawl_movie_url_by_tag(tag)
        movie_file = open('%s.txt' % tag, 'w')
        for url in movie_urls:
            movie_file.write(url + '\n')
            movie_file.flush()



