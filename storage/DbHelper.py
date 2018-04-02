#!/usr/bin/env python3
# coding=utf-8
# author=XingLong Pan
# date=2016-12-06

import pymysql.cursors
import configparser


class DbHelper:

    __connection = None

    def __init__(self):
        self.__connect_database()

    def __connect_database(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.__connection = pymysql.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            db=config['mysql']['db_name'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def insert_movie(self, movie):
        try:
            with self.__connection.cursor() as cursor:
                sql = "INSERT IGNORE INTO `movie` (`douban_id`, `title`, `directors`, " \
                      "`scriptwriters`, `actors`, `types`,`release_region`," \
                      "`release_date`,`alias`,`languages`,`duration`,`score`," \
                      "`description`,`tags`, `recommendations`, `comments`, `title_short`,`box_office`) VALUES (%s," \
                      "%s, %s, %s, %s, %s, %s, %s," \
                      "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (
                    movie['douban_id'],
                    movie['title'],
                    movie['directors'],
                    movie['scriptwriters'],
                    movie['actors'],
                    movie['types'],
                    movie['release_region'],
                    movie['release_date'],
                    movie['alias'],
                    movie['languages'],
                    movie['duration'],
                    movie['score'],
                    movie['description'],
                    movie['tags'],
                    movie['recommendations'],
                    movie['comments'],
                    movie['title_short'],
                    movie['box_office']
                ))
                self.__connection.commit()
        finally:
            self.__connection.close()
            pass

    def is_contains_movie(self, douban_id):
        with self.__connection.cursor() as cursor:
            sql = "SELECT `douban_id` from movie where `douban_id`=%s"
            cursor.execute(sql, (douban_id, ))
            result = cursor.fetchone()
            if not result:
                return False
            else:
                return True
        self.__connection.commit()
        self.close_db


    # 'douban_id': 0,
    # 'title': '',
    # 'directors': '',
    # 'scriptwriters': '',
    # 'actors': '',
    # 'types': '',
    # 'release_region': '',
    # 'release_date': '',
    # 'alias': '',
    # 'languages': '',
    # 'duration': 0,
    # 'score': 0.0,
    # 'description': '',
    # 'tags': '',
    # 'link': '',
    # 'posters': '',
    # 'recommendations': '',
    # 'comments': '',
    # 'want_to_watch': 0
    def data_clean(self):
        self.update_title()

    def close_db(self):
        self.__connection.close()

    def update_title_short(self):
        with self.__connection.cursor() as cursor:
            sql = "select * from movie where 1=1;"
            cursor.execute(sql)
            row_dict_list = cursor.fetchall()
            for row_dict in row_dict_list:
                title = row_dict['title']
                douban_id = row_dict['douban_id']
                print(douban_id)
                title_short = title.split(' ')[0]
                row_dict['title_short'] = title_short
                print(title_short)
                sql = "update movie set `title_short`=%s where `douban_id`=%s"
                cursor.execute(sql, (title_short, douban_id))
        self.__connection.commit()

    def get_id_title_dicts(self):
        row_dict_list = None
        with self.__connection.cursor() as cursor:
            sql = "select douban_id, title_short from movie where 1=1;"
            cursor.execute(sql)
            row_dict_list = cursor.fetchall()
        self.__connection.commit()
        return row_dict_list

    def update_box_office_by_id(self, douban_id, box_office):
        with self.__connection.cursor() as cursor:
            sql = "update movie set `box_office`=%s where `douban_id`=%s"
            cursor.execute(sql, (box_office, douban_id))
        self.__connection.commit()


if __name__ == '__main__':
    db_helper = DbHelper()
    db_helper.data_clean()
