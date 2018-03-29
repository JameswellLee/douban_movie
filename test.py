# coding=utf-8
import random
import constants
import requests
import sys
from page_parser import MovieParser

def test_movie_parser():
    test_url = 'https://movie.douban.com/subject/27114911/'
    headers = {'User-Agent': random.choice(constants.USER_AGENT)}
    # 获取豆瓣页面(API)数据
    r = requests.get(
        test_url,
        headers=headers,
        # cookies=cookies
    )
    r.encoding = 'utf-8'
    # 提取豆瓣数据
    parser = MovieParser.MovieParser()
    parser.set_html_doc(r.text)
    entity = parser.extract_page_entity()
    #print(entity)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    test_movie_parser()