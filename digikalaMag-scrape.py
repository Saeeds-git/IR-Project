import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from newspaper import Article
import pandas as panda


def article_crawler():
    page = 58
    scraped_data = []

    while True:
        page += 1
        main_page_url = f"https://www.digikala.com/mag/tag/%d9%86%da%a9%d8%aa%d9%87-%d9%88-%d8%aa%d8%b1%d9%81%d9%86%d8%af/page/{page}/"
        
        html = requests.get(main_page_url).text  # Download html of the page
        B_soup = BeautifulSoup(html, features='lxml')
        links = B_soup.find_all('div' , {"class": "masonry-gallery__item"})

        # to get out of the loop when we get to end of posts
        if len(links) == 0 : break

        for link in tqdm(links):
            a_tag = link.find_all("a")[0]
            page_url = a_tag["href"]
            try:
                article = Article(page_url)
                article.download()
                article.parse()
                scraped_data.append({'url': page_url, 'title': article.title, 'text': article.text})
            except:
                print(f"Failed to process page: {page_url}")

    df = panda.DataFrame(scraped_data)
    df.to_csv(f'D:\IR\digikalaMagTricks&Points.csv')


if __name__ == '__main__':
    article_crawler()

