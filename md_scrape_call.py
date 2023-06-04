import requests
from bs4 import BeautifulSoup

def get_deck_links(start_url, num_decks):
    # try:
        # response = requests.get(start_url)
        # response.raise_for_status()
    # except requests.exceptions.HTTPError as err:
        # print(f"HTTP error occurred: {err}")
        # return []
           
    response = requests.get(start_url)
     
    # Replace unsupported characters with '?'
    html_content = response.text.encode('utf-8', errors='replace').decode()
    print(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')

    deck_links = []

    # The deck names are in 'h3' tags with class 'decktype'
    deck_names = soup.find_all('h3', class_='decktype')

    for deck in deck_names[:num_decks]:  # Limit the number of decks
        link = deck.find('a').get('href')
        deck_links.append(link)

    return deck_links

def get_deck_list(deck_url):
    try:
        response = requests.get(deck_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    deck_list = []

    # The card names are in 'td' tags with class 'card'
    card_names = soup.find_all('td', class_='card')

    for card in card_names:
        deck_list.append(card.text)

    return deck_list

deck_links = get_deck_links('https://yugiohtopdecks.com/', 5)
print("Deck links:", deck_links)

for link in deck_links:
    print("Getting deck list for", link)
    deck_list = get_deck_list('https://yugiohtopdecks.com' + link)
    print("Deck list:", deck_list)