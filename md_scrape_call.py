import requests
from bs4 import BeautifulSoup
import re

def get_deck_links(start_url):
    print("Starting to scrape deck links...")
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    deck_links = []
    for link in soup.find_all('a', attrs={'href': re.compile("^/deck/")}):  
        relative_link = link.get('href')
        deck_links.append(relative_link)

    # Convert to set and back to list to remove duplicates
    deck_links = list(set(deck_links))
    print("Finished scraping deck links.")
    return deck_links

def get_deck_list(deck_url):
    print(f"Getting deck list for: {deck_url}")
    try:
        response = requests.get(deck_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        deck_parts = ['Main Deck', 'Extra Deck', 'Side Deck']
        deck_list = {part: [] for part in deck_parts}
        deck_parts_elements = soup.find_all('h4')

        for element in deck_parts_elements:
            if element.b:
                part_name = element.b.text
                if part_name in deck_parts:
                    ul_element = element.find_next_sibling('ul')
                    if ul_element:
                        card_elements = ul_element.find_all('li')
                        for card in card_elements:
                            card_name = card.a.text.strip()  # Card's name
                            card_quantity = card.b.text.strip()  # Card's quantity
                            deck_list[part_name].append((card_quantity, card_name))  # Add as tuple

    except requests.exceptions.RequestException as e:
        print(f"Error getting deck list from {deck_url}: {e}")

    print(f"Finished getting deck list for: {deck_url}")
    return deck_list