# edhrec_scraper/main_scraper.py

# These imports will work once we create edhrec_client.py and parsers.py
from . import edhrec_client
from . import parsers
from . import db_manager
from .config import BASE_URL_EDHREC, COMMANDERS_URL, CARDS_URL_TEMPLATE
# from .config import REFRESH_INTERVAL_DAYS_COMMANDER, REFRESH_INTERVAL_DAYS_CARD_STATS # If using refresh logic
from datetime import datetime, timedelta # If using refresh logic
import re

def slugify_card_name(card_name: str) -> str:
    """
    Converts a card name to a URL slug for EDHREC.
    Example: "Sol Ring" -> "sol-ring"
    Example: "Fire // Ice" -> "fire-ice" (common EDHREC pattern for splits)
    Needs to be robust based on EDHREC's actual slug patterns.
    """
    if not card_name: # Handle None or empty string
        return ""
    s = card_name.lower()
    s = s.replace(' // ', '-') # Handle split cards as EDHREC often does
    s = re.sub(r'[^\w\s-]', '', s) # Remove non-alphanumeric (except spaces and hyphens)
    s = re.sub(r'\s+', '-', s) # Replace spaces with hyphens
    s = re.sub(r'--+', '-', s) # Replace multiple hyphens with single
    s = s.strip('-')
    return s

def scrape_commanders(conn):
    """
    Scrapes commander list and individual commander pages.
    Returns a set of unique card names found for further scraping.
    """
    print("MAIN: Starting commander scraping phase.")

    entry_page_html_response = edhrec_client.get_html(COMMANDERS_URL)
    if not entry_page_html_response:
        print("MAIN_ERROR: Failed to fetch main commander listing from EDHREC. Aborting commander scrape.")
        return set()

    commander_infos = parsers.parse_commander_list_page(entry_page_html_response.text)
    if not commander_infos:
        print("MAIN_WARNING: No commanders found from the main list page. Check `parsers.parse_commander_list_page` and EDHREC site structure.")
        return set()

    discovered_cards_from_commanders = set()
    processed_count = 0
    skipped_due_to_db_missing = 0
    skipped_due_to_recent_scrape = 0

    with conn.cursor() as cur: # Obtain cursor once for multiple lookups
        for i, info in enumerate(commander_infos):
            commander_name = info.get('name')
            commander_url_path = info.get('url_path')

            if not commander_name or not commander_url_path:
                print(f"MAIN_WARNING: Invalid commander info found: {info}. Skipping.")
                continue

            print(f"MAIN_PROGRESS: Processing commander {i+1}/{len(commander_infos)}: {commander_name}")

            commander_card_id = db_manager.get_card_id_by_name(cur, commander_name)
            if not commander_card_id:
                print(f"MAIN_INFO: Commander '{commander_name}' not found in local 'cards' table. Skipping. (Consider running Scryfall import)")
                skipped_due_to_db_missing += 1
                continue

            full_commander_url = f"{BASE_URL_EDHREC}{commander_url_path}"
            cmd_page_html_response = edhrec_client.get_html(full_commander_url)

            if cmd_page_html_response:
                parsed_cmd_data = parsers.parse_commander_page(cmd_page_html_response.text, commander_name)
                if parsed_cmd_data:
                    cmd_stats = parsed_cmd_data.get('stats', {})
                    db_manager.save_edhrec_commander_stats(conn, commander_card_id,
                                                           cmd_stats.get('deck_count'),
                                                           cmd_stats.get('deck_percentage'))

                    related_cards = parsed_cmd_data.get('related_cards', [])
                    if related_cards:
                        db_manager.save_commander_card_synergies(conn, commander_card_id, related_cards)
                        for r_card in related_cards:
                            if r_card.get('card_name'): # Ensure card_name is not None
                                discovered_cards_from_commanders.add(r_card['card_name'])
                    processed_count += 1
                    print(f"MAIN_SUCCESS: Successfully processed and stored data for commander '{commander_name}'.")
                else:
                    print(f"MAIN_WARNING: Failed to parse data for commander '{commander_name}' from {full_commander_url}.")
            else:
                print(f"MAIN_WARNING: Failed to fetch HTML for commander '{commander_name}' from {full_commander_url}.")

    print(f"MAIN: Finished commander scraping. Processed: {processed_count}, Skipped (not in DB): {skipped_due_to_db_missing}, Skipped (recent): {skipped_due_to_recent_scrape}.")
    return discovered_cards_from_commanders

def scrape_cards(conn, card_names_to_scrape: set[str]):
    """Scrapes individual card pages and stores their EDHREC specific data."""
    if not card_names_to_scrape:
        print("MAIN_INFO: No new unique cards provided to scrape from EDHREC card pages.")
        return

    print(f"MAIN: Starting EDHREC card page scraping phase for {len(card_names_to_scrape)} cards.")
    processed_count = 0
    skipped_due_to_db_missing = 0
    skipped_due_to_recent_scrape = 0

    card_list_for_scraping = list(card_names_to_scrape)

    with conn.cursor() as cur: # Obtain cursor once
        for i, card_name in enumerate(card_list_for_scraping):
            print(f"MAIN_PROGRESS: Processing card {i+1}/{len(card_list_for_scraping)}: {card_name}")

            card_id = db_manager.get_card_id_by_name(cur, card_name)
            if not card_id:
                print(f"MAIN_INFO: Card '{card_name}' not found in local 'cards' table. Skipping EDHREC card page. (Consider running Scryfall import)")
                skipped_due_to_db_missing += 1
                continue

            card_slug = slugify_card_name(card_name)
            if not card_slug: # If slugify returns empty (e.g. for an empty card_name)
                print(f"MAIN_WARNING: Could not generate slug for card name '{card_name}'. Skipping.")
                continue

            full_card_url = CARDS_URL_TEMPLATE.format(card_slug=card_slug)
            card_page_html_response = edhrec_client.get_html(full_card_url)

            if card_page_html_response:
                parsed_card_data = parsers.parse_card_page(card_page_html_response.text, card_name)
                if parsed_card_data:
                    card_stats = parsed_card_data.get('stats', {})
                    db_manager.update_card_edhrec_stats(conn, card_id,
                                                        card_stats.get('salt_score'),
                                                        card_stats.get('overall_inclusion_percentage'),
                                                        card_stats.get('rank'))

                    played_with_list = parsed_card_data.get('played_with', [])
                    if played_with_list:
                        db_manager.save_card_card_synergies(conn, card_id, played_with_list)

                    processed_count +=1
                    print(f"MAIN_SUCCESS: Successfully processed and stored EDHREC data for card '{card_name}'.")
                else:
                    print(f"MAIN_WARNING: Failed to parse data for card '{card_name}' from {full_card_url}.")
            else:
                print(f"MAIN_WARNING: Failed to fetch HTML for card '{card_name}' from {full_card_url}.")

    print(f"MAIN: Finished EDHREC card page scraping. Processed: {processed_count}, Skipped (not in DB): {skipped_due_to_db_missing}, Skipped (recent): {skipped_due_to_recent_scrape}.")

def run_scraper():
    """Main function to orchestrate the EDHREC scraping."""
    print("MAIN: EDHREC Scraper Started.")
    db_conn = None
    try:
        db_conn = db_manager.get_db_connection()
        if not db_conn:
            print("MAIN_CRITICAL: Failed to establish database connection. Aborting.")
            return

        print("MAIN_INFO: Database connection successful.")

        discovered_cards = scrape_commanders(db_conn)

        if discovered_cards:
            scrape_cards(db_conn, discovered_cards)
        else:
            print("MAIN_INFO: No new cards were discovered from commander pages, or commander scraping was aborted. Card scraping phase skipped.")

        print("MAIN: EDHREC Scraping process nominally complete.")

    except psycopg2.Error as db_err: # Specific psycopg2 error
        print(f"MAIN_CRITICAL: A database error occurred: {db_err}")
    except ImportError as import_err:
        print(f"MAIN_CRITICAL: Failed to import a required module. Ensure all scraper files (client, parsers) are in place. Error: {import_err}")
    except Exception as e:
        print(f"MAIN_CRITICAL: An unexpected error occurred: {e}")
    finally:
        if db_conn:
            db_conn.close()
            print("MAIN_INFO: Database connection closed.")

if __name__ == "__main__":
    run_scraper()