import requests


def yu_requests(url, cookie = None):
    '''
    入力
    第一引数 URL 第二引数 cookie 
    出力
    URLを投げるとBeautifulSoupに入れるテキストを第一引数
    別のページに飛ばされていないかをbool型(True=飛ばされていない)第二引数
    cookieを第三引数
    '''
    header = user_agent()
    res  = requests.get(url,cookies=cookie,headers=header)
    text = res.text
    urlcheck = url_check(res ,url)
    new_cookie = res.cookies.get_dict()
    if res.status_code != 200:
        raise YubraryError("ステータスコードが200じゃないよ")
    return text, urlcheck, new_cookie


def user_agent():
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    header = {'User-Agent': ua}
    return header


def url_check(res, url):
    if res.url != url:
        return False
    return True


class YubraryError(Exception):
    pass
