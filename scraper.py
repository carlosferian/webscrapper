import requests
from bs4 import BeautifulSoup
import os


def search_link_articles(url, article_type):
    page_content = requests.get(url)
    if page_content.status_code == 200:
        soup = BeautifulSoup(page_content.content, 'html.parser')
        all_news = soup.find_all(string=article_type)
        links = []
        for new in all_news:
            links.append('https://www.nature.com' + new.find_parent('article').find('a').get('href'))
        return links
    return None


def clean_name(in_str):
    in_str = in_str.strip()
    in_str = in_str.replace(' ', '_')
    for i in r"!#$%&'()*+,-./:;<=>?@[\]^`´{|}~':":
        in_str = in_str.replace(i, '')
    return in_str + '.txt'


def get_content_article(url):
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.content, 'html.parser')
    article = soup.find('div', class_='article__body')
    if article:
        return article.text.strip()
    else:
        article = soup.find('div', class_='article-item__body')
        return article.text.strip()


def get_name_file(url):
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.content, 'html.parser')
    article_name = clean_name(soup.find('h1', class_='article-item__title').text)
    return article_name


def save_articles_to_txt(article_type, n, url):
    os.mkdir(f'Page_{n}')

    path = f'{os.getcwd()}/Page_{n}/'
    article_links = search_link_articles(url, article_type)
    if article_links:
        for link in article_links:
            article_name = get_name_file(link)
            article_content = get_content_article(link)
            with open(path + article_name, 'wb') as file:
                file.write(article_content.encode('utf-8'))


def get_pages(n):
    pages = {}
    for i in range(n):
        pages[str(i + 1)] = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={i + 1}'
    return pages


page_number = int(input())
article_type = input()

pages = get_pages(page_number)

for k, v in pages.items():
    save_articles_to_txt(article_type, k, v)
