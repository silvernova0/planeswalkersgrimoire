# edhrec_scraper/db_manager.py
import psycopg2
from psycopg2 import extras # For extras.execute_values
# MODIFIED: Import specific variables from .config
from .config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from datetime import datetime

# REMOVED: The direct DB_CONFIG dictionary is no longer here.

def get_db_connection():
    """Establishes and returns a PostgreSQL database connection."""
    # MODIFIED: Uses imported config variables
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def get_card_id_by_name(cursor, card_name: str) -> int | None:
    """Fetches a card's ID from the 'cards' table by its name."""
    try:
        cursor.execute("SELECT id FROM cards WHERE name = %s", (card_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except psycopg2.Error as e:
        print(f"DB_MANAGER_ERROR: Error fetching card ID for '{card_name}': {e}")
        return None

# --- Functions to save EDHREC data ---

def update_card_edhrec_stats(conn, card_id: int, salt_score: float | None, overall_inclusion: float | None, edhrec_rank: int | None):
    """
    Updates EDHREC-specific stats in the 'cards' table.
    Assumes 'edhrec_salt_score', 'edhrec_overall_inclusion_percentage', 'edhrec_rank', 'last_edhrec_update' columns exist in 'cards' table.
    """
    sql = """
        UPDATE cards
        SET edhrec_salt_score = %s,
            edhrec_overall_inclusion_percentage = %s,
            edhrec_rank = %s,
            last_edhrec_update = %s
        WHERE id = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (salt_score, overall_inclusion, edhrec_rank, datetime.now(), card_id))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"DB_MANAGER_ERROR: Error updating EDHREC stats for card_id {card_id}: {e}")

def save_edhrec_commander_stats(conn, commander_card_id: int, deck_count: int | None, deck_percentage: float | None):
    """
    Saves or updates a commander's EDHREC stats in 'edhrec_commander_stats'.
    """
    sql = """
        INSERT INTO edhrec_commander_stats (card_id, edhrec_deck_count, edhrec_deck_percentage, last_scraped)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (card_id) DO UPDATE SET
            edhrec_deck_count = EXCLUDED.edhrec_deck_count,
            edhrec_deck_percentage = EXCLUDED.edhrec_deck_percentage,
            last_scraped = EXCLUDED.last_scraped;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (commander_card_id, deck_count, deck_percentage, datetime.now()))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"DB_MANAGER_ERROR: Error saving EDHREC commander stats for card_id {commander_card_id}: {e}")


def save_commander_card_synergies(conn, commander_card_id: int, synergy_data_list: list[dict]):
    """
    Bulk saves commander-card synergy data.
    synergy_data_list is a list of dicts:
    [{'card_name': str, 'source_list': str, 'inclusion_percentage': float, 'synergy_score': float}, ...]
    """
    if not synergy_data_list:
        return

    values_to_insert = []
    # Create a new cursor for this operation to avoid issues if passed cursor is in a transaction
    with conn.cursor() as cur_synergy: # Use a distinct cursor
        for item in synergy_data_list:
            # Ensure 'card_name' exists and is not None
            item_card_name = item.get('card_name')
            if not item_card_name:
                print(f"DB_MANAGER_WARNING: Missing 'card_name' in synergy item for commander_id {commander_card_id}. Skipping item: {item}")
                continue

            recommended_card_id = get_card_id_by_name(cur_synergy, item_card_name)
            if recommended_card_id:
                values_to_insert.append((
                    commander_card_id,
                    recommended_card_id,
                    item.get('source_list'),
                    item.get('inclusion_percentage'),
                    item.get('synergy_score')
                ))
            else:
                print(f"DB_MANAGER_WARNING: Could not find card_id for '{item_card_name}' while saving synergy for commander_id {commander_card_id}. Skipping.")

    if not values_to_insert:
        # print(f"DB_MANAGER_INFO: No valid card IDs found for synergy data for commander_id {commander_card_id}.")
        return

    sql = """
        INSERT INTO edhrec_commander_card_synergy
            (commander_card_id, recommended_card_id, source_list, inclusion_percentage, synergy_score)
        VALUES %s
        ON CONFLICT (commander_card_id, recommended_card_id, source_list) DO UPDATE SET
            inclusion_percentage = EXCLUDED.inclusion_percentage,
            synergy_score = EXCLUDED.synergy_score;
    """
    try:
        with conn.cursor() as cur_exec: # Use another distinct cursor for execution
            extras.execute_values(cur_exec, sql, values_to_insert)
        conn.commit()
        # print(f"DB_MANAGER_INFO: Saved/Updated {len(values_to_insert)} synergy entries for commander_id {commander_card_id}.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"DB_MANAGER_ERROR: Error bulk saving commander card synergies for commander_id {commander_card_id}: {e}")

def save_card_card_synergies(conn, primary_card_id: int, synergy_data_list: list[dict]):
    """
    Bulk saves card-card synergy data (for 'played with' section).
    """
    if not synergy_data_list:
        return

    values_to_insert = []
    with conn.cursor() as cur_synergy_cc: # Distinct cursor
        for item in synergy_data_list:
            item_card_name = item.get('card_name')
            if not item_card_name:
                print(f"DB_MANAGER_WARNING: Missing 'card_name' in card-card synergy item for primary_card_id {primary_card_id}. Skipping item: {item}")
                continue

            associated_card_id = get_card_id_by_name(cur_synergy_cc, item_card_name)
            if associated_card_id:
                values_to_insert.append((
                    primary_card_id,
                    associated_card_id,
                    item.get('source_list'),
                    item.get('inclusion_percentage'),
                    item.get('synergy_score')
                ))
            else:
                print(f"DB_MANAGER_WARNING: Could not find card_id for '{item_card_name}' while saving card-card synergy for primary_card_id {primary_card_id}. Skipping.")

    if not values_to_insert:
        # print(f"DB_MANAGER_INFO: No valid card IDs found for card-card synergy data for primary_card_id {primary_card_id}.")
        return

    sql = """
        INSERT INTO edhrec_card_card_synergy
            (primary_card_id, associated_card_id, source_list, inclusion_percentage, synergy_score)
        VALUES %s
        ON CONFLICT (primary_card_id, associated_card_id, source_list) DO UPDATE SET
            inclusion_percentage = EXCLUDED.inclusion_percentage,
            synergy_score = EXCLUDED.synergy_score;
    """
    try:
        with conn.cursor() as cur_exec_cc: # Distinct cursor
            extras.execute_values(cur_exec_cc, sql, values_to_insert)
        conn.commit()
        # print(f"DB_MANAGER_INFO: Saved/Updated {len(values_to_insert)} card-card synergy entries for primary_card_id {primary_card_id}.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"DB_MANAGER_ERROR: Error bulk saving card card synergies for primary_card_id {primary_card_id}: {e}")
