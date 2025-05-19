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
    resp = requests.get(archetype_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    # Right side: <a href="event?e=60726&d=656453&f=cEDH">
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

def parse_deck(deck_url):
    resp = requests.get(deck_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    h1 = soup.find('h1')
    deck_name = h1.get_text(strip=True) if h1 else deck_url

    # Find the decklist text block
    # Try to find the <pre> or <div class="deck_line"> or similar
    decklist_text = ""
    pre = soup.find('pre')
    if pre:
        decklist_text = pre.get_text()
    else:
        # Fallback: try to find the decklist in a <div class="deck_line"> or similar
        deck_div = soup.find('div', class_='deck_line')
        if deck_div:
            decklist_text = deck_div.get_text("\n")
        else:
            # Fallback: try to extract from the table as text
            table = soup.find('table', class_='Stable')
            if table:
                decklist_text = "\n".join(row.get_text(" ", strip=True) for row in table.find_all('tr'))

    # Now parse the decklist text
    commander_names = []
    cards = []
    in_commander_section = False

    for line in decklist_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r'^COMMANDER', line, re.IGNORECASE):
            in_commander_section = True
            continue
        elif in_commander_section and re.match(r'^[A-Z ]+$', line) and not line.startswith("COMMANDER"):
            # Section header, end of commander section
            in_commander_section = False
        if in_commander_section:
            m = re.match(r'^(\d+)\s+(.+)$', line)
            if m and m.group(1) == "1":
                commander_names.append(m.group(2))
        # Always parse cards
        m = re.match(r'^(\d+)\s+(.+)$', line)
        if m:
            cards.append({"name": m.group(2), "quantity": int(m.group(1))})

    print(f"Deck: {deck_name} | Commanders: {commander_names}")
    return {
        "name": deck_name,
        "commanders": commander_names,
        "cards": cards,
        "placement": None,
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
            parse_deck(deck_url)

if __name__ == "__main__":
    asyncio.run(main())