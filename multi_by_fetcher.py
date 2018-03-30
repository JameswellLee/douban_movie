# coding=utf-8
# author=Alan Lee
# date=2018-03-25

import random
import requests
import configparser
import json
import constants
import sys
import multiprocessing as mp
import MovieFetcher
from utils import Utils
from page_parser import MovieParser
from page_parser import CommentParser
from storage import DbHelper
requests.packages.urllib3.disable_warnings()
# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def getHtml(movie_url):
    try:
        proxy_string = "46.218.85.101:3129"
        proxies = {"https": "https://{}".format(proxy_string),
                   "http": "http://{}".format(proxy_string)}
        proxies
        r = requests.get(movie_url, proxies=proxies, timeout=constants.CHECK_PROXY_TIMEOUT)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None


def crawl_page_by_url(url, parser):
    text = getHtml(url)
    if not text:
        return None
    parser.set_html_doc(text)
    entity = parser.extract_page_entity()
    return entity


def crawl_movie_and_save(movie_url, db_helper):
    parts = movie_url.split('/')
    douban_id = parts[-2]
    if db_helper.is_contains_movie(douban_id):
        print('contains movie url=%s' % movie_url)
        return False

    movie_parser = MovieParser.MovieParser()
    comment_parser = CommentParser.CommentParser()
    movie = crawl_page_by_url(movie_url, movie_parser)
    if not movie:
        print('failed crawl movie url=%s' % movie_url)
        return False
    # if movie['want_to_watch'] < constants.WHAT_TO_WATCH_LIMIT:
    #     print('want_to_watch=%d, failed crawl movie url: url=%s' %(movie['want_to_watch'], movie_url))
    #     return False
    comment_url = constants.URL_COMMENTS_FORMAT % douban_id
    comments = crawl_page_by_url(comment_url, comment_parser)
    if not comments or not movie:
        print('failed crawl comments, url=%s' % movie_url)
        return False
    if movie:
        movie['link'] = movie_url
        movie['douban_id'] = str(douban_id)
        movie['comments'] = json.dumps(comments)
        db_helper.insert_movie(movie)
        print('crawl success url=%s' % movie_url)
        return True


def load_urls(url_file):
    url_set = []
    url_file = open(url_file, 'r')
    for line in url_file:
        if 'http' in line:
            url = line.strip()
            url_set.append(url)
    return url_set


def run_func(args):
    dp_helper = DbHelper.DbHelper()
    for url in args:
        crawl_movie_and_save(url, dp_helper)


def multi_process_crawl():
    reload(sys)
    sys.setdefaultencoding('utf8')
    thread_num = 1
    pool = mp.Pool(thread_num)
    up_now_playing_urls = load_urls('热门.txt')
    hot_movie_urls = load_urls('up_now_playing.txt')
    dianyin_urls = load_urls('电影.txt')
    classical_urls = load_urls('经典.txt')
    high_score_urls = load_urls('豆瓣高分.txt')
    all_urls = []
    all_urls.extend(up_now_playing_urls)
    all_urls.extend(hot_movie_urls)
    all_urls.extend(classical_urls)
    all_urls.extend(high_score_urls)
    all_urls.extend(dianyin_urls)
    all_urls = [url.replace('https', 'http') for url in all_urls]
    start_url = "http://movie.douban.com/subject/1301757/"
    start_url_idx = 0
    all_urls = all_urls[start_url_idx:]
    print("start from %d, url=%s" % (start_url_idx, start_url))
    args = []
    step = len(all_urls) / thread_num
    for i in range(thread_num):
        if i < thread_num-1:
            args.append((all_urls[i * step: (i + step)]))
        else:
            args.append((all_urls[i * step:]))
    args.append(all_urls)
    pool.map(run_func, args)
    pool.close()
    pool.join()


if __name__ == '__main__':
    multi_process_crawl()


