# coding=utf-8
import requests
import editdistance
import Utils
import sys
import json
import re

from bs4 import BeautifulSoup


logger = Utils.Utils.get_logger('crawl_box_office', 'box_office.log')


def crawl_box_office_cbooo(title_short):
    searh_url ='http://www.cbooo.cn/search?'
    param = {'k': title_short}
    r = requests.get(searh_url, params=param)
    bs = BeautifulSoup(r.text, 'html.parser')
    lis = bs.find('ul', {'class': 'ulzx03'}).find_all('li')
    info_list = []
    for li in lis:
        name = li.find('a')['title']
        url = li.find('a')['href']
        distance = editdistance.eval(title_short.encode('utf-8'), name.encode('utf-8'))
        info_list.append((title_short, name, distance, url))
    if len(info_list) == 0:
        logger.info('not found for title_short=%s' % title_short)
        return 'not found'
    #found match movie by editdistance
    sort_list = sorted(info_list, key=lambda x: x[2])
    best_match = info_list[0]
    #如果能找到完美匹配的使用完美匹配，不能则直接获取第一个搜索结果
    if sort_list[0][2] == 0:
        best_match = sort_list[0]
    else:
        best_match = info_list[0]
    r = requests.get(best_match[3])
    bs = BeautifulSoup(r.text, 'html.parser')
    info = bs.find('span', {'class': 'm-span'})
    if not info:
        logger.info('not found for title_short=%s' % title_short)
        return 'not found'
    infos = info.contents
    box_office = infos[2]
    logger.info('best_match info:title_short=%s, name=%s, box_office=%s, distance=%s' % (best_match[0], best_match[1], box_office, best_match[2]))
    return box_office


def crawl_box_office_maoyan(title_short):
    searh_url ='http://maoyan.com/query?'
    maoyan_url = 'http://maoyan.com'
    param = {'kw': title_short}
    r = requests.get(searh_url, params=param, headers={'User-Agent': 'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)'})
    r.encoding = 'utf-8'
    bs = BeautifulSoup(r.text, 'html.parser')
    lis = bs.find('div', {'class': 'search-result-box'})
    if not lis:
        print('dl')
        return 'not found'
    lis = lis.find_all('dd')
    info_list = []
    for li in lis:
        movie_item = li.find('div', {'class': 'channel-detail movie-item-title'})
        name = movie_item['title']
        url = maoyan_url + movie_item.find('a')['href']
        print(url)
        distance = editdistance.eval(title_short.encode('utf-8'), name.encode('utf-8'))
        info_list.append((title_short, name, distance, url))
    if len(info_list) == 0:
        logger.info('not found for title_short=%s' % title_short)
        return 'not found'
    #found match movie by editdistance
    sort_list = sorted(info_list, key=lambda x: x[2])
    best_match = info_list[0]
    #如果能找到完美匹配的使用完美匹配，不能则直接获取第一个搜索结果
    if sort_list[0][2] == 0:
        best_match = sort_list[0]
    else:
        best_match = info_list[0]
    logger.info('best_match info:title_short=%s, name=%s, distance=%s, url=%s' % (best_match[0], best_match[1], best_match[2], best_match[3]))
    r = requests.get(best_match[3], headers={'User-Agent': 'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)'})
    bs = BeautifulSoup(r.text, 'html.parser')
    info = bs.find('div', {'class': 'movie-index-content box'}).find('span', {'class': 'stonefont'})
    if not info:
        logger.info('not found for title_short=%s' % title_short)
        return 'not found'
    box_office = info.text
    logger.info('best_match info:title_short=%s, name=%s, box_office=%s, distance=%s' % (best_match[0], best_match[1], box_office, best_match[2]))
    return box_office


def crawl_box_office_mtime(title_short):
    searh_api ='http://service.channel.mtime.com/Search.api?'
    movie_api ='http://service.library.mtime.com/Movie.api?'
    search_param = {'Ajax_CallBack': 'true',
                    'Ajax_CallBackType': 'Mtime.Channel.Services',
                    'Ajax_CallBackMethod': 'GetSearchResult',
                    'Ajax_CrossDomain': '1',
                    'Ajax_CallBackArgument0': title_short,
                    'Ajax_CallBackArgument1': '0',
                    'Ajax_CallBackArgument2': '290',
                    'Ajax_CallBackArgument3': '0',
                    'Ajax_CallBackArgument4': '1'}
    movie_param = {'Ajax_CallBack': 'true',
                   'Ajax_CallBackType': 'Mtime.Library.Services',
                   'Ajax_CallBackMethod': 'GetMovieOverviewRating',
                   'Ajax_CrossDomain': '1',
                   'Ajax_CallBackArgument0': None}
    #search movie by title_short
    r = requests.get(searh_api, params=search_param, headers={'User-Agent': 'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)'})
    result = r.text.replace('var getSearchResult = ', '')
    result = result[:-3]
    try:
        movie_dict = json.loads(result)
    except:
        return 'not found'
    movie_result = movie_dict['value']
    if 'movieResult' not in movie_result:
        return 'not found'
    movie_result = movie_result['movieResult']
    if 'totalCount' not in movie_result:
        return 'not found'
    total_count = movie_result['totalCount']
    if total_count == 0:
        return 'not found'
    more_movies = movie_result['moreMovies']
    movie = more_movies[0]
    movie_id = movie['movieId']
    movie_title = movie['movieTitle']
    movie_param['Ajax_CallBackArgument0'] = movie_id

    #search movie info by id
    r = requests.get(movie_api, params=movie_param)
    result = r.text.replace('var movieOverviewRatingResult = ', '')
    result = result[:-3]
    try:
        movie_dict = json.loads(result)
    except:
        return 'not found'
    movie_result = movie_dict['value']
    if 'boxOffice' not in movie_result:
        return 'not found'
    box_office = movie_result['boxOffice']
    if 'TotalBoxOffice' not in box_office:
        return 'not found'
    total_box_office = box_office['TotalBoxOffice']
    box_office_unit = box_office['TotalBoxOfficeUnit']
    return total_box_office + box_office_unit


def crawl_box_office_mojo(title):
    title_parts = title.split(' ')
    title_parts = title_parts[1:]
    english_title = ' '.join(title_parts)
    print(english_title)
    search_url = 'http://www.boxofficemojo.com/search/?'
    movie_page = 'http://www.boxofficemojo.com'
    param = {'q': english_title}
    r = requests.get(search_url, params=param)
    if r.status_code != 200:
        return 'not found'
    bs = BeautifulSoup(r.text, 'html.parser')
    tr = bs.find('tr', {'bgcolor': '#FFFF99'})
    if not tr:
        tr = bs.find('tr', {'bgcolor': '#FFFFFF'})
    if not tr:
        return 'not found'

    movie_url = tr.find('a')['href']
    domestic_tr = tr.find_all('td')[2]
    domestic_box_office = domestic_tr.text
    if '$' not in domestic_box_office:
        return 'not found'
    domestic_box_office = format_us_box_office(domestic_box_office)
    print('domestic_box_office=%s' % domestic_box_office)
    print(movie_page + movie_url)
    movie_url = movie_page + movie_url

    r = requests.get(movie_url)
    bs = BeautifulSoup(r.text, 'html.parser')
    box_content = bs.find('div', {'class': 'mp_box_content'})
    if not box_content:
        return domestic_box_office
    trs = box_content.find_all('tr')
    if not trs or len(trs) < 3:
        return domestic_box_office
    box_tr = trs[-1]
    box_office_td = box_tr.find_all('td')[1]
    box_office = box_office_td.text

    box_office = format_us_box_office(box_office)
    print('world_wide_box_office=%s' % box_office)
    return box_office


def format_us_box_office(box_office):
    box_office = box_office.replace('$', '').replace(',', '')
    box_office = str(int(box_office) / 10000)
    box_office = box_office + '万美元'
    return box_office


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    result = crawl_box_office_mojo('真实的谎言 True Lies')