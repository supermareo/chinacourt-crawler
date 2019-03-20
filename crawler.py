# coding=utf-8
import requests
from bs4 import BeautifulSoup
from file_util import append_lines, read_lines
from time import sleep
import os

DOMAIN = 'https://www.chinacourt.org'
BASE_URL = DOMAIN + '/article/index/id/MzAwNDAwNTBIApMEAAA%3D/page/{page_no}.shtml'


# 获取总页数
def get_total_pages():
    soup = open_page()
    page_control = soup.find(attrs={'class': 'paginationControl'})
    last_page = page_control.find_all('a')[-2]
    last_page_url = last_page['href']
    return int(last_page_url.split('/')[-1].split('.')[0])


# 打开问题列表第 page_no 页，转换为soup返回
def open_page(page_no=1):
    url = BASE_URL.format(page_no=page_no)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


# 提取问题列表页
def extract_problems(soup):
    result = []
    article_list = soup.find(id='articleList').find('ul').find_all('li')
    for article in article_list:
        a = article.find('a')
        title = a['title']
        href = a['href']
        question = {
            'question': title.strip(),
            'url': DOMAIN + href
        }
        result.append(question)
    return result


# 打开问题详情页，提取出详情
def extract_problem_detail(url):
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        detail = soup.find(attrs={'class': 'detail_txt'})
        return detail.text
    except:
        return None


# 再处理一遍失败的
def process_fail():
    lines = read_lines('error.txt')
    os.remove('error.txt')
    q = ''
    u = ''
    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            q = line[2:]
        elif line.startswith('U:'):
            u = line[2:]
        if u != '':
            problem_detail = extract_problem_detail(u)
            if problem_detail is not None:
                append_lines('question_list.txt', ['Q:' + q + '\n', 'A:' + problem_detail + '\n'])
                print('end process', q)
            else:
                print('----------------error process', q)
                append_lines('error.txt', ['Q:' + q + '\n', 'U:' + u + '\n'])
            q = ''
            u = ''


if __name__ == '__main__':
    total_pages = get_total_pages()
    print('start, total', total_pages, 'pages')
    for i in range(1, total_pages + 1):
        print('> start process page', i)
        soup = open_page(i)
        problems = extract_problems(soup)
        for problem in problems:
            sleep(0.3)
            question = problem['question']
            print('start process', question)
            url = problem['url']
            problem_detail = extract_problem_detail(url)
            if problem_detail is not None:
                append_lines('question_list.txt', ['Q:' + question + '\n', 'A:' + problem_detail + '\n'])
                print('end process', question)
            else:
                print('----------------error process', question)
                append_lines('error.txt', ['Q:' + question + '\n', 'U:' + url + '\n'])
        print('> end process page', i)
    # 再把失败的重新跑一次
    process_fail()
    print('complete')
