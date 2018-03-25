# coding=utf-8
# author=XingLong Pan
# date=2016-12-04

# 豆瓣电影的登录入口页面
DOUBAN_MOVIE_LOGIN_URL = 'https://accounts.douban.com/login'

# 搜索引擎（SEO爬虫）的请求头
USER_AGENT = [
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
        'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
        'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)'
    ]
AGENT_SIZE = 7

# 延时设置
DELAY_MIN_SECOND = 1
DELAY_MAX_SECOND = 2

# 豆瓣电影的url前缀
URL_PREFIX = 'https://movie.douban.com/subject/'
URL_MOVIE_TYPE = 'https://movie.douban.com/j/new_search_subjects'
ALL_FORMS = ['电影', '电视剧', '综艺', '动画', '纪录片', '短片']
ALL_TYPES = ['剧情', '爱情', '喜剧', '科幻', '动作', '悬疑', '犯罪', '恐怖', '青春', '励志', '战争', '文艺', '黑色幽默', '传记', '情色', '暴力', '音乐', '家庭']
ALL_AREAS = ['大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国','意大利', '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']

"""
这里用到了阿布云代理动态版。使用影梭或者其他代理，甚至不用代理也可以
"""
# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HT1LX50X8R4P0I8D"
proxyPass = "1133BD889583B72A"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
