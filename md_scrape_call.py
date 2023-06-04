import requests
from bs4 import BeautifulSoup

def scrape_site(start_url, max_pages):
    url = start_url
    for _ in range(max_pages):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Here, you would scrape the data you're interested in. For example:
        # articles = soup.find_all('div', class_='article')
        # for article in articles:
        #     print(article.text)

        # Try to find a link to the next page
        next_link = soup.find('a', rel='next')

        if next_link is None:
            break  # Couldn't find a link to the next page
        
        url = next_link.get('href')  # Get the URL for the next page

scrape_site('http://example.com/articles', max_pages=10)
