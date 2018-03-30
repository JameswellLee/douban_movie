import requests
import constants
import random
import string


class MovieFetcher:
    def __init__(self):

        self.session = requests.Session()
        self.session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
        self.clear_session()
        return

    def clear_session(self):
        self.session.headers.clear()
        self.session.cookies.clear()
        self.session.headers = {
            'User-Agent': random.choice(constants.USER_AGENT),
            "Host": "movie.douban.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
            "Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
        }
        return

    def url_fetch(self, url):
        resp = self.session.get(url, allow_redirects=False, verify=False, timeout=5)
        if resp.status_code == 200:
            return resp.text
        print("Fetcher change cookie: %s", resp.status_code)
        self.clear_session()
        resp.raise_for_status()
        return resp.text


if __name__ == '__main__':
    session = requests.Session()
    session.get('https://movie.douban.com/subject/26602933/')
    # fetcher = MovieFetcher()
    # fetcher.url_fetch('https://movie.douban.com/subject/26602933/')
