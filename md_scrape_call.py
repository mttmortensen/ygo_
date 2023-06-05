import requests
from bs4 import BeautifulSoup
import re

def get_deck_links(start_url):
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    deck_links = []
    for link in soup.find_all('a', attrs={'href': re.compile("^/deck/")}):  
        relative_link = link.get('href')
        deck_links.append(relative_link)

    return deck_links

def get_deck_list(deck_url):
    try:
        response = requests.get(deck_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        deck_list = []
        # The card names are in 'td' tags with class 'card'
        card_names = soup.find_all('td', class_='card')

        for card in card_names:
            deck_list.append(card.text)

    except requests.exceptions.RequestException as e:
        print(f"Error getting deck list from {deck_url}: {e}")

    return deck_list

deck_links = get_deck_links('https://yugiohtopdecks.com/decklists')

with open("output.txt", "a", encoding="utf-8") as f:
    f.write("Deck links: " + str(deck_links) + "\n")

    for link in deck_links:
        deck_list = get_deck_list('https://yugiohtopdecks.com' + link)
        f.write("Getting deck list for: " + link + "\n")
        f.write("Deck list: " + str(deck_list) + "\n")
