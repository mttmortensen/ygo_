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

    # Convert to set and back to list to remove duplicates
    deck_links = list(set(deck_links))

    return deck_links

def get_deck_list(deck_url):
    try:
        response = requests.get(deck_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        deck_parts = ['Main Deck', 'Extra Deck', 'Side Deck']
        deck_list = {part: [] for part in deck_parts}
        deck_parts_elements = soup.find_all('h4')

        for element in deck_parts_elements:
            if element.b:  # Add this check to ensure element.b is not None
                part_name = element.b.text
                if part_name in deck_parts:
                    ul_element = element.find_next_sibling('ul')
                    if ul_element:
                        card_elements = ul_element.find_all('li')
                        for card in card_elements:
                            deck_list[part_name].append(card.a.text.strip())  # Update here to get card names

    except requests.exceptions.RequestException as e:
        print(f"Error getting deck list from {deck_url}: {e}")

    return deck_list



deck_links = get_deck_links('https://yugiohtopdecks.com/decklists')

with open("output.txt", "w", encoding="utf-8") as f:  # Open file in write mode
    f.write("Deck links: " + str(deck_links) + "\n")

    for link in deck_links:
        deck_list = get_deck_list('https://yugiohtopdecks.com' + link)  
        f.write("Getting deck list for: " + link + "\n")
        f.write("Deck list: " + str(deck_list) + "\n")

