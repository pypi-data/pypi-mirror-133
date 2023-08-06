import requests

from fake_useragent import UserAgent


def ajax(cookie=None, proxies=None):
    headers = {'User-Agent': UserAgent().random}

    if cookie:
        headers['cookie'] = cookie

    if proxies:
        proxies = {
            'http': 'http://' + proxies,
            'https': 'https://' + proxies,
        }

    return headers, proxies


def get(url, params=None, cookie=None, proxies=None):
    headers, proxies = ajax(cookie, proxies)
    return requests.get(url, params=params, headers=headers, proxies=proxies)


def post(url, data=None, cookie=None, proxies=None):
    headers, proxies = ajax(cookie, proxies)
    return requests.post(url, data=data, headers=headers, proxies=proxies)
