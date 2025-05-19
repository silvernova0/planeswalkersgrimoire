import asyncio
import requests
from bs4 import BeautifulSoup
import sys
import os
import sqlalchemy as sa

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

    deck_links = []
    # Deck links look like <a href="event?e=XXXXX&d=YYYYY&f=cEDH">
    for a in soup.select('a[href*="&d="]'):
        deck_links.append(BASE_URL + "/" + a['href'])
    return {
        "name": event_name,
        "date": event_date,
        "url": event_url,
        "deck_links": list(set(deck_links))
    }

def parse_deck(deck_url):
    resp = requests.get(deck_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Deck name
    h1 = soup.find('h1')
    if h1:
        deck_name = h1.get_text(strip=True)
    else:
        title = soup.find('title')
        if title:
            deck_name = title.text.strip().split('@')[0].replace('Decklist:', '').strip()
        else:
            print(f"Warning: No deck name found for {deck_url}")
            print(soup.prettify()[:1000])
            return None
    placement = None  # Parse as needed

    # Find commander: look for a row with "Commander" or similar
    commander = None
    for row in soup.select('table.Stable tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            label = cols[1].get_text(strip=True)
            if "commander" in label.lower():
                # Sometimes the label is "Commander: Card Name"
                parts = label.split(":")
                if len(parts) > 1:
                    commander = parts[1].strip()
                else:
                    commander = label.strip()
                break
    # Fallback: use the first card in the first table
    if not commander:
        first_table = soup.find('table', class_='Stable')
        if first_table:
            first_row = first_table.find('tr')
            if first_row:
                cols = first_row.find_all('td')
                if len(cols) == 2:
                    commander = cols[1].get_text(strip=True)

    cards = []
    for row in soup.select('table.Stable tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            qty = cols[0].get_text(strip=True)
            card_name = cols[1].get_text(strip=True)
            if qty.isdigit():
                cards.append({"name": card_name, "quantity": int(qty)})
    return {
        "name": deck_name,
        "commander": commander,
        "cards": cards,
        "placement": placement,
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
            commander=deck_data['commander'],
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
                is_commander=(card['name'] == deck_data['commander'])
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

if __name__ == "__main__":
    asyncio.run(main())