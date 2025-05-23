# edhrec_scraper/parsers.py
from bs4 import BeautifulSoup
import re

# --- Helper Utility Functions for Parsing ---

def _get_text_or_none(element, selector: str, strip: bool = True):
    """Safely gets text from a selected sub-element, returns None if element or sub-element not found."""
    if not element:
        return None
    found_el = element.select_one(selector)
    if found_el:
        return found_el.get_text(strip=strip)
    return None

def _get_attribute_or_none(element, selector: str, attribute: str):
    """Safely gets an attribute from a selected sub-element."""
    if not element:
        return None
    found_el = element.select_one(selector)
    if found_el:
        return found_el.get(attribute)
    return None

def _extract_percentage(text: str | None) -> float | None:
    """Extracts percentage like 'X%' or 'X.Y%' from text, returns as float (e.g., 0.XX)."""
    if not text:
        return None
    match = re.search(r'(\d+\.?\d*)%', text)
    return float(match.group(1)) / 100.0 if match else None

def _extract_number(text: str | None) -> int | None:
    """Extracts the first integer found in a string."""
    if not text:
        return None
    match = re.search(r'(\d+)', text.replace(',', '')) # Remove commas for numbers like 1,234
    return int(match.group(1)) if match else None

# --- Main Parsing Functions ---

def parse_commander_list_page(html_content: str) -> list[dict]:
    """
    Parses a page listing multiple commanders.
    (e.g., https://edhrec.com/commanders)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    commanders_found = []
    print("PARSER_INFO: Attempting to parse commander list page...")
    
    # ** YOU WILL NEED TO DEFINE THIS SELECTOR **
    # This selector should target the <a> tags that link to individual commander pages.
    # commander_link_elements = soup.select('YOUR_SELECTOR_FOR_COMMANDER_LINKS_HERE') 
    # Example (conceptual):
    # for link_el in commander_link_elements:
    #     name = link_el.get_text(strip=True)
    #     url_path = link_el.get('href')
    #     if name and url_path and url_path.startswith('/commanders/'):
    #         commanders_found.append({'name': name, 'url_path': url_path})

    if not commanders_found:
        print("PARSER_WARNING: No commander links found on list page. Check selector in `parse_commander_list_page`.")
    else:
        print(f"PARSER_INFO: Found {len(commanders_found)} potential commanders on list page.")
    return commanders_found

def parse_commander_page(html_content: str, commander_name: str) -> dict | None:
    """
    Parses an individual commander's page on EDHREC.
    (e.g., https://edhrec.com/commanders/atraxa-praetors-voice)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {'name': commander_name, 'stats': {}, 'related_cards': []}
    print(f"PARSER_INFO: Parsing EDHREC page for commander: {commander_name}")

    # --- Parse Commander Stats ---
    # ** YOU WILL NEED TO DEFINE THESE SELECTORS **
    # Example:
    # data['stats']['deck_count'] = _extract_number(_get_text_or_none(soup, 'SELECTOR_FOR_DECK_COUNT'))
    # data['stats']['deck_percentage'] = _extract_percentage(_get_text_or_none(soup, 'SELECTOR_FOR_DECK_PERCENTAGE'))

    # --- Parse Related Cards (High Synergy, Top Cards, by Type, etc.) ---
    # Example for one section (e.g., "High Synergy Cards"):
    # high_synergy_section = soup.select_one('SELECTOR_FOR_HIGH_SYNERGY_SECTION')
    # if high_synergy_section:
    #     source_list_name = "High Synergy Cards"
    #     card_items = high_synergy_section.select('SELECTOR_FOR_INDIVIDUAL_CARD_ITEMS_IN_SECTION')
    #     for item_el in card_items:
    #         card_name = _get_text_or_none(item_el, 'SELECTOR_FOR_CARD_NAME_IN_ITEM')
    #         inclusion_text = _get_text_or_none(item_el, 'SELECTOR_FOR_INCLUSION_IN_ITEM')
    #         synergy_text = _get_text_or_none(item_el, 'SELECTOR_FOR_SYNERGY_IN_ITEM')
    #         if card_name:
    #             data['related_cards'].append({
    #                 'card_name': card_name, 'source_list': source_list_name,
    #                 'inclusion_percentage': _extract_percentage(inclusion_text),
    #                 'synergy_score': _extract_percentage(synergy_text)
    #             })
    # ** REPEAT FOR OTHER SECTIONS (Top Cards, Creatures, etc.) **

    if not data['stats'] and not data['related_cards']:
         print(f"PARSER_WARNING: No stats or related cards found for commander '{commander_name}'. Check selectors.")
    else:
        print(f"PARSER_INFO: Parsed commander '{commander_name}'. Stats: {data['stats']}. Found {len(data['related_cards'])} related card entries.")
    return data

def parse_card_page(html_content: str, card_name: str) -> dict | None:
    """
    Parses an individual card's page on EDHREC.
    (e.g., https://edhrec.com/cards/sol-ring)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {'name': card_name, 'stats': {}, 'played_with': [], 'top_commanders': []}
    print(f"PARSER_INFO: Parsing EDHREC page for card: {card_name}")

    # --- Parse Card Stats ---
    # ** YOU WILL NEED TO DEFINE THESE SELECTORS **
    # data['stats']['overall_inclusion_percentage'] = _extract_percentage(_get_text_or_none(soup, 'SELECTOR_FOR_OVERALL_INCLUSION'))
    # salt_text = _get_text_or_none(soup, 'SELECTOR_FOR_SALT_SCORE')
    # if salt_text: try: data['stats']['salt_score'] = float(salt_text) ...

    # --- Parse "Played With" Cards ---
    # Similar to related_cards on commander page.
    # played_with_section = soup.select_one('SELECTOR_FOR_PLAYED_WITH_SECTION')
    # if played_with_section: ... (loop through items) ...

    # --- Parse "Top Commanders" using this card ---
    # top_commanders_section = soup.select_one('SELECTOR_FOR_TOP_COMMANDERS_SECTION')
    # if top_commanders_section: ... (loop through items) ...

    if not data['stats'] and not data['played_with'] and not data['top_commanders']:
        print(f"PARSER_WARNING: No data found for card '{card_name}'. Check selectors.")
    else:
        print(f"PARSER_INFO: Parsed card '{card_name}'. Stats: {data['stats']}. Found {len(data['played_with'])} played-with, {len(data['top_commanders'])} top commanders.")
    return data