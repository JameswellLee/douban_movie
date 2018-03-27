# coding=utf-8
# author=Alan Lee
# date=2018-03-25

import random
import requests
import configparser
import constants
import time
import os
from login import CookiesHelper
from page_parser import MovieParser
from page_parser import CommentParser
from storage import DbHelper

# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')



fail_url_file = open(config['common']['fail_url_file'], 'w+')


def crawl_by_lines(lines, start_line):
    movie_parser = MovieParser.MovieParser()
    comment_parser = CommentParser.CommentParser()
    db_helper = DbHelper.DbHelper()
    for i in range(start_line, len(lines)):
        line = lines[i]
        if len(line) < 5:
            continue
        start_time = time.time()
        movie_data = eval(line)
        movie_url = movie_data['url']
        movie_id = movie_data['id']
        comment_url = constants.URL_COMMENTS_FORMAT % movie_id

        headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        # 获取豆瓣页面(API)数据
        r = requests.get(
            movie_url,
            headers=headers,
            # cookies=cookies
        )
        r.encoding = 'utf-8'

        # 提取豆瓣数据
        movie_parser.set_html_doc(r.text)
        movie = movie_parser.extract_movie_info()

        # 获取电影评论页面数据
        r = requests.get(
            comment_url,
            headers=headers,
            # cookies=cookies
        )
        r.encoding = 'utf-8'
        comment_parser.set_html_doc(r.text)
        comments = comment_parser.extract_comments_str(movie_id)

        # 如果没获取到电影评论数据要重新爬取
        if not comments:
            movie = None
        # 如果获取的数据为空，延时以减轻对目标服务器的压力,并跳过。
        if not movie:
            # 将没有获取到的电影url重新写入文件中
            fail_url_file.write(str(movie_data) + '\n')
            fail_url_file.flush()

        if movie:
            movie['link'] = movie_url
            movie['douban_id'] = str(movie_id)
            movie['comments'] = comments
            db_helper.insert_movie(movie)
        cost_time = time.time() - start_time
        print('crawl status : line=%d, url=%s, state=%s, time=%s' % (i, movie_data['url'], not not movie, cost_time))
        # 释放资源
    movie_parser = None
    db_helper.close_db()


if __name__ == '__main__':
    # 通过电影地区获取到的url进行电影爬取
    area_start_idx = 0
    start_line = 1573
    for i in range(area_start_idx, len(constants.ALL_AREAS)):
        url_file_name = os.path.join(config['common']['url_dir'], constants.ALL_AREAS[i] + '.txt')
        with open(url_file_name, 'r') as url_file:
            lines = url_file.readlines()
            crawl_by_lines(lines, start_line)



