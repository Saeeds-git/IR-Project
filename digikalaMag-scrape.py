
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd


def article_crawler(year: int):
    page = 58
    scraped_data = []
    url_list = []

    while True:
        page += 1

        main_page_url = f"https://www.digikala.com/mag/tag/%d9%86%da%a9%d8%aa%d9%87-%d9%88-%d8%aa%d8%b1%d9%81%d9%86%d8%af/page/{page}/"

        html = requests.get(main_page_url).text  # Download html of the page

        soup = BeautifulSoup(html, features='lxml')

        links = soup.find_all('div' , {"class": "masonry-gallery__item"})

        # to get out of the loop when we get to end of posts
        if len(links) == 0 : break

        for link in tqdm(links):
            
            link2 = link.find_all("a")[0]
            page_url = link2["href"]
            url_list.append(page_url)
            try:
                article = Article(page_url)
                article.download()
                article.parse()
                scraped_data.append({'url': page_url, 'text': article.text, 'title': article.title})
            except:
                print(f"Failed to process page: {page_url}")

    df = pd.DataFrame(scraped_data)
    df.to_csv(f'D:\IR\digikalaMagTricks&Points.csv')


if __name__ == '__main__':
    article_crawler(1400)

