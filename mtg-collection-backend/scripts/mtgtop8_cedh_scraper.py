import asyncio
import requests
from bs4 import BeautifulSoup
import sys
import os
import sqlalchemy as sa
import re

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.database import AsyncSessionLocal
from app.models import MetaTournament, MetaDeck, MetaDeckCard

BASE_URL = "https://www.mtgtop8.com"

def get_cedh_event_links():
    url = f"{BASE_URL}/format?f=cEDH"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    event_links = []
    # Each event is in a table row with a link like <a href="event?e=XXXXX&f=cEDH">
    for a in soup.select('a[href^="event?e="]'):
        event_links.append(BASE_URL + "/" + a['href'])
    return list(set(event_links))  # Remove duplicates

def get_cedh_deck_links():
    url = f"{BASE_URL}/format?f=cEDH"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Find deck links (you'll need to inspect the HTML structure)
    deck_links = []
    for a in soup.select('a[href^="event?e="]'):
        deck_links.append(BASE_URL + "/" + a['href'])
    return deck_links

def get_commander_archetype_links():
    url = f"{BASE_URL}/archetype?a=1158&meta=240&f=cEDH&color_id=&show=pop"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    # Left sidebar: <a href="archetype?a=1781&meta=240&f=cEDH&color_id=&show=alpha">
    for a in soup.select('div#archetypes_list a[href^="archetype?a="]'):
        links.append(BASE_URL + "/" + a['href'])
    return links

def get_deck_links_from_archetype(archetype_url):
    # Always use show=all to get all decks for the commander
    if "show=all" not in archetype_url:
        if "show=" in archetype_url:
            archetype_url = re.sub(r"show=\w+", "show=all", archetype_url)
        else:
            archetype_url += "&show=all"
    resp = requests.get(archetype_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    for a in soup.select('a[href^="event?e="][href*="&d="]'):
        links.append(BASE_URL + "/" + a['href'])
    return links

def parse_event(event_url):
    resp = requests.get(event_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Try alternative selectors if <h1> is missing
    h1 = soup.find('h1')
    if h1:
        event_name = h1.get_text(strip=True)
    else:
        # Fallback: get event name from <title>
        title = soup.find('title')
        if title and "@" in title.text:
            # Example: "cEDH event - CEDH Tournament @ Spacity Cards (Hot Springs, AR) @ mtgtop8.com"
            event_name = title.text.split("@")[0].replace("cEDH event -", "").strip()
        elif title:
            event_name = title.text.strip()
        else:
            print(f"Warning: No event name found for {event_url}")
            print(soup.prettify()[:1000])
            return None
    # Date is often in a <div> or <td> near the top, you may need to inspect the HTML
    event_date = None  # Parse as needed

    deck_links = set()
    # Add the current page (the #1 deck) itself
    deck_links.add(event_url)
    # Find all links to other decks in this event
    for a in soup.select('a[href^="event?e="]'):
        href = a['href']
        # Only include links with both e= and d= (i.e., specific decks)
        if "&d=" in href:
            deck_links.add(BASE_URL + "/" + href)
    return {
        "name": event_name,
        "date": event_date,
        "url": event_url,
        "deck_links": list(deck_links)
    }

import re # Ensure re is imported

def parse_deck(deck_url):
    resp = requests.get(deck_url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # --- New Deck Name Logic ---
    deck_name = deck_url # Default to URL
    try:
        deck_name_element_container = soup.find('div', class_='w_title')
        if deck_name_element_container:
            event_title_divs = deck_name_element_container.find_all('div', class_='event_title', recursive=False)
            if len(event_title_divs) > 1 and event_title_divs[1]:
                # Try to get text before " - " which usually precedes player name
                raw_name_text = event_title_divs[1].get_text(separator=' ', strip=True)
                # Split at " - " which often separates archetype from player
                parts = raw_name_text.split(" - ", 1)
                potential_name = parts[0]
                # Clean up ranking like "#1 ", "3-4. " etc.
                cleaned_name = re.sub(r'^#?\d+(?:-\d+)?\s*[\.\-]?\s*', '', potential_name).strip()
                if cleaned_name:
                    deck_name = cleaned_name
                else:
                    print(f"Warning: Deck name parsing (cleaned) resulted in empty string for {deck_url}. Defaulting to URL.")
            else:
                print(f"Warning: Could not find specific deck name structure (second event_title) for {deck_url}. Defaulting to URL.")
        else:
            print(f"Warning: Could not find w_title container for deck name for {deck_url}. Defaulting to URL.")
    except Exception as e:
        print(f"Error parsing deck name for {deck_url}: {e}. Defaulting to URL.")


    # --- New Commander Names Logic ---
    commander_names = []
    try:
        card_list_columns = soup.find_all('div', style=lambda x: x and 'flex:1' in x and 'margin:3px' in x)
        if not card_list_columns:
            card_list_columns = [soup] # Fallback: search the whole document

        for column in card_list_columns:
            o14_headers = column.find_all('div', class_='O14')
            for header_div in o14_headers:
                if header_div.get_text(strip=True).upper() == "COMMANDER":
                    current_element = header_div.find_next_sibling()
                    while current_element:
                        if current_element.name == 'div' and 'O14' in current_element.get('class', []):
                            break # Next section
                        if current_element.name == 'div' and 'deck_line' in current_element.get('class', []):
                            card_name_span = current_element.find('span', class_='L14')
                            card_name_text = card_name_span.get_text(strip=True) if card_name_span else ''
                            
                            # Get quantity - usually the text node before the span or first text node
                            quantity_str = ''
                            if current_element.contents:
                                first_content = str(current_element.contents[0]).strip()
                                if first_content.isdigit(): # Check if the first part is a number
                                    quantity_str = first_content
                            
                            if quantity_str == "1" and card_name_text:
                                commander_names.append(card_name_text)
                        current_element = current_element.find_next_sibling()
                    if commander_names: break # Found in this column
            if commander_names: break # Found in one of the columns
        if not commander_names:
            print(f"Warning: No commanders found for {deck_url} using new parsing method.")
    except Exception as e:
        print(f"Error parsing commanders for {deck_url}: {e}")

    # --- New All Cards Logic ---
    cards = []
    try:
        all_deck_lines = soup.find_all('div', class_='deck_line')
        for line_div in all_deck_lines:
            card_name_span = line_div.find('span', class_='L14')
            card_name_text = card_name_span.get_text(strip=True) if card_name_span else ''
            
            quantity_str = ''
            # Iterate through contents to find quantity more reliably
            for content_node in line_div.contents:
                if isinstance(content_node, str): # NavigableString
                    potential_qty = content_node.strip()
                    if potential_qty.isdigit():
                        quantity_str = potential_qty
                        break # Found quantity

            if card_name_text and quantity_str.isdigit():
                cards.append({"name": card_name_text, "quantity": int(quantity_str)})
            elif card_name_text: # If quantity parsing failed but name exists, assume 1 (or log warning)
                 cards.append({"name": card_name_text, "quantity": 1}) # Default quantity or handle error
                 print(f"Warning: Quantity not found for card '{card_name_text}' in {deck_url}, defaulting to 1.")


        if not cards:
            print(f"Warning: No cards parsed for {deck_url} using new method.")
    except Exception as e:
        print(f"Error parsing all cards for {deck_url}: {e}")
        
    # Fallback to old text-based parsing if new method yields no cards,
    # but this is less likely to be useful if HTML structure changed significantly.
    # Consider removing old decklist_text logic entirely if new one is meant to be comprehensive.
    # For now, the new 'all_deck_lines' logic above should be the primary source for 'cards'.

    print(f"Deck: {deck_name} | Commanders: {commander_names}") # Keep this for logging
    return {
        "name": deck_name,
        "commanders": commander_names,
        "cards": cards, # Populated by new 'all_deck_lines' logic
        "placement": None, # This was never parsed, remains None
        "url": deck_url
    }

async def save_deck_to_db(event_data, deck_data):
    async with AsyncSessionLocal() as session:
        # Insert or get tournament
        result = await session.execute(
            sa.select(MetaTournament).where(
                MetaTournament.name == event_data['name'],
                MetaTournament.date == event_data['date']
            )
        )
        tournament = result.scalars().first()
        if not tournament:
            tournament = MetaTournament(name=event_data['name'], date=event_data['date'], url=event_data['url'])
            session.add(tournament)
            await session.commit()
            await session.refresh(tournament)
        # Insert deck
        deck = MetaDeck(
            name=deck_data['name'],
            commander=", ".join(deck_data['commanders']),  # Updated to handle multiple commanders
            tournament_id=tournament.id,
            placement=deck_data['placement'],
            url=deck_data['url']
        )
        session.add(deck)
        await session.commit()
        await session.refresh(deck)
        # Insert cards
        for card in deck_data['cards']:
            deck_card = MetaDeckCard(
                deck_id=deck.id,
                card_name=card['name'],
                quantity=card['quantity'],
                is_commander=(card['name'] in deck_data['commanders'])
            )
            session.add(deck_card)
        await session.commit()

async def main():
    # Define generic tournament details for archetype decks
    generic_tournament_details = {
        "name": "cEDH Archetype Data",
        "date": None,  # MetaTournament.date is nullable
        "url": "N/A"   # Or a relevant placeholder URL
    }

    # Get or create the generic tournament entry for archetype decks
    archetype_event_tournament_orm = None
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            sa.select(MetaTournament).where(
                MetaTournament.name == generic_tournament_details['name'],
                MetaTournament.date == generic_tournament_details['date'] # Comparing None with None works
            )
        )
        archetype_event_tournament_orm = result.scalars().first()

        if not archetype_event_tournament_orm:
            print(f"Creating generic tournament: {generic_tournament_details['name']}")
            archetype_event_tournament_orm = MetaTournament(
                name=generic_tournament_details['name'],
                date=generic_tournament_details['date'],
                url=generic_tournament_details['url']
            )
            session.add(archetype_event_tournament_orm)
            await session.commit()
            await session.refresh(archetype_event_tournament_orm)
        else:
            print(f"Found existing generic tournament: {archetype_event_tournament_orm.name}")

    # Prepare event_data structure for save_deck_to_db using the generic details
    event_data_for_archetypes = generic_tournament_details

    event_links = get_cedh_event_links()
    for event_url in event_links:
        event_data = parse_event(event_url)
        if not event_data:
            continue
        for deck_url in event_data['deck_links']:
            deck_data = parse_deck(deck_url)
            if not deck_data:
                continue
            await save_deck_to_db(event_data, deck_data)
            print(f"Saved deck: {deck_data['name']} from event {event_data['name']}")

    commander_links = get_commander_archetype_links()
    for commander_url in commander_links:
        print(f"Commander archetype: {commander_url}")
        deck_links = get_deck_links_from_archetype(commander_url)
        for deck_url in deck_links:
            deck_data = parse_deck(deck_url)
            if not deck_data:
                continue
            await save_deck_to_db(event_data_for_archetypes, deck_data)
            print(f"Saving deck from archetype {commander_url}: {deck_data['name']} | Commanders: {deck_data['commanders']}")

if __name__ == "__main__":
    asyncio.run(main())