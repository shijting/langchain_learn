import json
import re

import requests
from bs4 import BeautifulSoup


def __get_text(html):
    html_str = BeautifulSoup(html, 'html.parser')
    return html_str.text  # 过滤掉html标签，只保留文本内容


def __get_keyvalue(data):
    # 匹配【】中的内容及后面的内容
    pattern = r'【(.*?)】(.*)'
    match = re.search(pattern, data)
    if match:
        return {"key": match.group(1), "value": match.group(2)}
    return None


def get_cls_data(keyword: str, page: int = 1, size: int = 5, type: str = "telegram"):
    url = 'https://www.cls.cn/api/sw?app=CailianpressWeb&os=web'
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    json_body = {
        "type": type,
        "keyword": keyword,
        "page": page,
        "rn": size,
        "os": "web",
        "sv": "7.7.5",
        "app": "CailianpressWeb"
    }
    resp = requests.post(url, headers=headers, data=json.dumps(json_body))

    data = json.loads(resp.text).get('data').get('telegram').get('data')
    ret = []
    for item in data:
        kv = __get_keyvalue(__get_text(item.get('descr')))
        if kv:
            ret.append(kv)
    return ret
