import requests
import time
import json
from requests.exceptions import RequestException
import re

def get_one_page(url):
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<div class="list_num.*?">(.*?)\..*?class="name"><a .*?>(.*?)<.*?class="tuijian">(.*?)</span>.*?<a .*?>(.*?)</a>.*?<span>(.*?)</span>.*?<a .*?>(.*?)</a>.*?class="price_n">(.*?)</span>.*?class="price_r">(.*?)</span>.*?class="price_s">(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
        '排名': item[0],
        '书名': item[1],
        '作者': item[3],
        '出版社': item[5],
        '出版日期': item[4],
        '推荐度': item[2],
        '原价': item[7],
        '现价': item[6],
        '打折力度': item[8]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as file:
        file.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://bang.dangdang.com/books/bestsellers/01.54.00.00.00.00-year-2018-0-1-' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(1, 26):
        main(offset=i)
        time.sleep(5)
