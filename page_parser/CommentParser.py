# coding=utf-8
# author=Alan Lee
# data=2018/3/25

from bs4 import BeautifulSoup
import Entity
import constants
import re
class CommentParser:
    """
    负责从html文档中解析视频实体信息

    当然了，你也可以使用Xpath表达式来提取。这里只是为了方便。
    """
    __soup = ''
    __NOT_FOUND = u'页面不存在'
    __html_doc = ''

    def __set_bs_soup(self):

        self.__soup = BeautifulSoup(self.__html_doc, 'html.parser')

    def __is_404_page(self):

        if self.__html_doc.find(self.__NOT_FOUND) != -1:
            return True

        if len(self.__html_doc) < 500:
            return True

        return False

    def set_html_doc(self, html_doc):

        self.__html_doc = html_doc

    def get_comments(self):
        comments = []
        try:
            infos = self.__soup.find_all('div', {'class': 'comment'})
            for info in infos:
                comment = Entity.comment.copy()
                vote_node = info.find('span', {'class': 'votes'})
                if vote_node:
                    comment['votes'] = int(vote_node.text)
                else:
                    comment['votes'] = 0
                comment['description'] = info.find('p').text
                comment_info = info.find('span', {'class', 'comment-info'}).contents
                for c_info in comment_info:
                    if len(str(c_info)) < 10:
                        continue
                    if str(c_info).find('allstar') != -1:
                        comment['rating'] = constants.COMMENT_RATING_DICT[c_info.attrs['title']]
                comments.append(comment)
        except:
            pass
        return comments

    def extract_page_str(self):
        """
        :return:所有评论连接起来的字符串
        """
        if self.__html_doc is None:
            return None

        if self.__is_404_page():
            return None
        rating_list = []
        self.__set_bs_soup()
        comments = self.get_comments()
        for comment in comments:
            rating_list.append(comment['description'])
        return 'amp&;'.join(rating_list)

    def extract_page_entity(self):
        """
        如果为404或其他出错页面，返回None。
        :return: None|dict
        """
        if self.__html_doc is None:
            return None

        if self.__is_404_page():
            return None
        self.__set_bs_soup()
        return self.get_comments()

