import requests

from fake_useragent import UserAgent


def get(url):
    headers = {'User-Agent': UserAgent().random}
    return requests.get(url, headers=headers)
