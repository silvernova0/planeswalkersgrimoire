# scripts/populate_cards.py
import asyncio
import json
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import httpx # Moved import to top level

from sqlalchemy.ext.asyncio import AsyncSession
# Removed Column, String, Integer, Boolean, JSON, Float, JSONB, ARRAY as local model is removed


# You'll need to set up access to your database session and CRUD operations
# This might involve importing from your main app's modules
# For simplicity, assuming you can get a db session and access CRUD
from app.database import AsyncSessionLocal, Base, engine # Adjust imports as needed
from app.models import CardDefinition as CardDefinitionModel
from app.crud import get_card_definition_by_scryfall_id # Import the CRUD function


# URL for a Scryfall bulk data file (e.g., Oracle Cards or All Cards)
# Get the latest download URI from https://api.scryfall.com/bulk-data
# Example: SCRYFALL_BULK_DATA_URL = "https://data.scryfall.io/oracle-cards/oracle-cards-20231030090509.json" 
# It's best to fetch the bulk data list first to get the current download_uri

async def get_latest_bulk_data_uri(bulk_type: str = "oracle_cards"): # or "all_cards"
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.scryfall.com/bulk-data")
        response.raise_for_status()
        bulk_data_list = response.json()["data"]
        for item in bulk_data_list:
            if item["type"] == bulk_type:
                return item["download_uri"]
    return None

async def process_card_data(db: AsyncSession, card_data: dict, image_client: httpx.AsyncClient):
    scryfall_id = card_data.get("id")
    if not scryfall_id:
        print(f"Skipping card with missing Scryfall ID: {card_data.get('name')}")
        return

    card_name_from_bulk = card_data.get("name")
    if not card_name_from_bulk:
        print(f"Skipping card {scryfall_id} due to missing name in bulk data.")
        return

    card_to_process: CardDefinitionModel | None = await get_card_definition_by_scryfall_id(db, scryfall_id)
    is_new_card = False

    image_uris = card_data.get("image_uris", {})

    if card_to_process:
        print(f"Card {scryfall_id} ({card_name_from_bulk}) already exists. Checking for updates...")
        # Update existing card's attributes - make this comprehensive
        card_to_process.name = card_name_from_bulk
        card_to_process.set_code = card_data.get("set")
        card_to_process.collector_number = card_data.get("collector_number")
        card_to_process.legalities = card_data.get("legalities")
        card_to_process.type_line = card_data.get("type_line")
        card_to_process.mana_cost = card_data.get("mana_cost")
        card_to_process.color_identity = card_data.get("color_identity")
        card_to_process.lang = card_data.get("lang", "en")
        card_to_process.type_line = card_data.get("type_line")
        card_to_process.mana_cost = card_data.get("mana_cost")
        card_to_process.cmc = card_data.get("cmc")
        card_to_process.keywords = card_data.get("keywords")
        card_to_process.rarity = card_data.get("rarity")
        card_to_process.artist = card_data.get("artist")
        card_to_process.released_at = card_data.get("released_at")
        card_to_process.set_name = card_data.get("set_name")
        card_to_process.layout = card_data.get("layout")
        card_to_process.frame = card_data.get("frame")
        card_to_process.border_color = card_data.get("border_color")
        card_to_process.full_art = card_data.get("full_art")
        card_to_process.textless = card_data.get("textless")
        card_to_process.reprint = card_data.get("reprint")
        card_to_process.promo = card_data.get("promo")
        card_to_process.digital = card_data.get("digital")
        card_to_process.foil = card_data.get("foil")
        card_to_process.nonfoil = card_data.get("nonfoil")
        card_to_process.oversized = card_data.get("oversized")
        card_to_process.story_spotlight = card_data.get("story_spotlight")
        card_to_process.edhrec_rank = card_data.get("edhrec_rank")
        card_to_process.prices = card_data.get("prices")
        card_to_process.card_faces = card_data.get("card_faces")
        card_to_process.all_parts = card_data.get("all_parts")
        card_to_process.purchase_uris = card_data.get("purchase_uris")
        card_to_process.related_uris = card_data.get("related_uris")
        card_to_process.scryfall_uri = card_data.get("scryfall_uri")
        card_to_process.rulings_uri = card_data.get("rulings_uri")
        card_to_process.prints_search_uri = card_data.get("prints_search_uri")
        card_to_process.oracle_text = card_data.get("oracle_text")
        card_to_process.flavor_text = card_data.get("flavor_text")
        card_to_process.power = card_data.get("power")
        card_to_process.toughness = card_data.get("toughness")
        card_to_process.loyalty = card_data.get("loyalty")
        card_to_process.colors = card_data.get("colors")
        card_to_process.image_uri_small = image_uris.get("small")
        card_to_process.image_uri_normal = image_uris.get("normal")
        card_to_process.image_uri_large = image_uris.get("large")
        card_to_process.image_uri_art_crop = image_uris.get("art_crop")
        card_to_process.image_uri_border_crop = image_uris.get("border_crop")
        # SQLAlchemy's onupdate mechanism should handle 'date_updated'

    else: # Card does not exist, create a new one
        print(f"Card {scryfall_id} ({card_name_from_bulk}) not found. Creating new record...")
        is_new_card = True
        
        card_model_data_for_new = {
            "scryfall_id": scryfall_id,
            "name": card_name_from_bulk,
            "set_code": card_data.get("set"),
            "lang": card_data.get("lang", "en"), # Default to 'en' if not present
            "collector_number": card_data.get("collector_number"),
            "type_line": card_data.get("type_line"),
            "mana_cost": card_data.get("mana_cost"),
            "cmc": card_data.get("cmc"),
            "oracle_text": card_data.get("oracle_text"),
            "flavor_text": card_data.get("flavor_text"),
            "power": card_data.get("power"),
            "toughness": card_data.get("toughness"),
            "loyalty": card_data.get("loyalty"),
            "colors": card_data.get("colors"),
            "color_identity": card_data.get("color_identity"),
            "keywords": card_data.get("keywords"),
            "rarity": card_data.get("rarity"),
            "artist": card_data.get("artist"),
            "released_at": card_data.get("released_at"),
            "set_name": card_data.get("set_name"),
            "layout": card_data.get("layout"),
            "frame": card_data.get("frame"),
            "border_color": card_data.get("border_color"),
            "full_art": card_data.get("full_art"),
            "textless": card_data.get("textless"),
            "reprint": card_data.get("reprint"),
            "promo": card_data.get("promo"),
            "digital": card_data.get("digital"),
            "foil": card_data.get("foil"), # Scryfall field indicates if foil version exists
            "nonfoil": card_data.get("nonfoil"), # Scryfall field indicates if nonfoil version exists
            "oversized": card_data.get("oversized"),
            "story_spotlight": card_data.get("story_spotlight"),
            "edhrec_rank": card_data.get("edhrec_rank"),
            "legalities": card_data.get("legalities"),
            "prices": card_data.get("prices"),
            "card_faces": card_data.get("card_faces"),
            "all_parts": card_data.get("all_parts"),
            "purchase_uris": card_data.get("purchase_uris"),
            "related_uris": card_data.get("related_uris"),
            "image_uri_small": image_uris.get("small"),
            "image_uri_normal": image_uris.get("normal"),
            "image_uri_large": image_uris.get("large"),
            "image_uri_art_crop": image_uris.get("art_crop"),
            "image_uri_border_crop": image_uris.get("border_crop"),
            "scryfall_uri": card_data.get("scryfall_uri"),
            "card_faces": card_data.get("card_faces"),
            "rulings_uri": card_data.get("rulings_uri"),
            "prints_search_uri": card_data.get("prints_search_uri"),
        }
        try:
            card_to_process = CardDefinitionModel(**card_model_data_for_new)
        except Exception as e:
            print(f"Error instantiating CardDefinitionModel for new card {scryfall_id} ({card_name_from_bulk}): {e}")
            return

    # Download image data if URI exists and corresponding image_data field is None
    if card_to_process.image_uri_small and not card_to_process.image_data_small:
        try:
            print(f"Attempting to download small image for {card_to_process.name} from {card_to_process.image_uri_small}")
            response = await image_client.get(card_to_process.image_uri_small)
            response.raise_for_status()
            card_to_process.image_data_small = response.content
            print(f"Successfully downloaded small image for {card_to_process.name} ({len(response.content)} bytes)")
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error downloading small image for {scryfall_id} ({card_to_process.name}): {e.response.status_code} - {e.request.url}")
            card_to_process.image_uri_small = None
            card_to_process.image_data_small = None
        except Exception as e:
            print(f"Generic Error downloading small image for {scryfall_id} ({card_to_process.name}): {e}")
            card_to_process.image_uri_small = None
            card_to_process.image_data_small = None

    if card_to_process.image_uri_normal and not card_to_process.image_data_normal:
        try:
            print(f"Attempting to download normal image for {card_to_process.name} from {card_to_process.image_uri_normal}")
            response = await image_client.get(card_to_process.image_uri_normal)
            response.raise_for_status()
            card_to_process.image_data_normal = response.content
            print(f"Successfully downloaded normal image for {card_to_process.name} ({len(response.content)} bytes)")
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error downloading normal image for {scryfall_id} ({card_to_process.name}): {e.response.status_code} - {e.request.url}")
            card_to_process.image_uri_normal = None
            card_to_process.image_data_normal = None
        except Exception as e:
            print(f"Generic Error downloading normal image for {scryfall_id} ({card_to_process.name}): {e}")
            card_to_process.image_uri_normal = None
            card_to_process.image_data_normal = None

    if card_to_process.image_uri_large and not card_to_process.image_data_large:
        try:
            print(f"Attempting to download large image for {card_to_process.name} from {card_to_process.image_uri_large}")
            response = await image_client.get(card_to_process.image_uri_large)
            response.raise_for_status()
            card_to_process.image_data_large = response.content
            print(f"Successfully downloaded large image for {card_to_process.name} ({len(response.content)} bytes)")
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error downloading large image for {scryfall_id} ({card_to_process.name}): {e.response.status_code} - {e.request.url}")
            card_to_process.image_uri_large = None
            card_to_process.image_data_large = None
        except Exception as e:
            print(f"Generic Error downloading large image for {scryfall_id} ({card_to_process.name}): {e}")
            card_to_process.image_uri_large = None
            card_to_process.image_data_large = None

    if is_new_card and card_to_process:
        try:
            db.add(card_to_process)
        except Exception as e:
            print(f"Error adding new card {card_to_process.name} ({scryfall_id}) to session: {e}")

async def main_populate():
    # Initialize DB (if needed for a standalone script, or ensure tables exist)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    bulk_data_uri = await get_latest_bulk_data_uri(bulk_type="all_cards") # or "oracle_cards"
    if not bulk_data_uri:
        print("Could not retrieve bulk data URI.")
        return

    print(f"Downloading bulk data from: {bulk_data_uri}")
    async with httpx.AsyncClient(timeout=None) as client: # Set longer timeout for large files
        response = await client.get(bulk_data_uri)
        response.raise_for_status()
        all_cards_data = response.json() # This will be a list of card objects

    print(f"Downloaded {len(all_cards_data)} card objects.")

    # Ensure database tables are created if not already (idempotent)
    async with engine.begin() as conn:
        # await conn.run_sync(CardDefinitionModel.__table__.drop, checkfirst=True) # CAUTION: Drops the table! - Commented out
        await conn.run_sync(Base.metadata.create_all)
        # No explicit commit needed here as engine.begin() handles transaction
    print("Database tables ensured.")

    async with AsyncSessionLocal() as session:
        # Create one httpx client for all image downloads within this session
        async with httpx.AsyncClient(timeout=30) as image_download_client: # Timeout for individual image downloads
            try:
                concurrency_factor = 20  # Reduced concurrency due to image downloads
                commit_batch_size = 200 # Commit more frequently due to larger data
                
                processed_count_since_last_commit = 0

                for i in range(0, len(all_cards_data), concurrency_factor):
                    current_batch_all_cards = all_cards_data[i:i + concurrency_factor]
                    
                    # --- IMPORTANT: "Lightning Bolt" Filter ---
                    # The following lines filter to ONLY process "Lightning Bolt".
                    # If you want to process ALL cards, remove or comment out this filter
                    # and use `current_batch_all_cards` directly in the tasks.
                    #
                    # Example: To process all cards, change:
                    #   `lightning_bolt_batch = [...]`
                    #   `if not lightning_bolt_batch: continue`
                    #   `tasks = [process_card_data(session, card_data, image_download_client) for card_data in lightning_bolt_batch]`
                    #   `processed_count_in_batch = len(lightning_bolt_batch)`
                    # TO:
                    #   `batch_to_process = current_batch_all_cards`
                    #   `if not batch_to_process: continue`
                    #   `tasks = [process_card_data(session, card_data, image_download_client) for card_data in batch_to_process]`
                    #   `processed_count_in_batch = len(batch_to_process)`
                    # And adjust print statements accordingly.
                    # For now, keeping the "Lightning Bolt" filter as it was in your original script.

                    batch_to_process = current_batch_all_cards # Default to all cards in batch
                    # batch_to_process = [ # Uncomment this block to filter for "Lightning Bolt"
                    #     card_data for card_data in current_batch_all_cards
                    #     if card_data.get("name") == "Lightning Bolt"
                    # ]

                    total_scanned_so_far = i + len(current_batch_all_cards)

                    if not batch_to_process: # If filtering resulted in an empty batch
                        print(f"Scanned batch up to card {total_scanned_so_far}/{len(all_cards_data)}. No cards to process in this segment (check filters).")
                        continue # Move to the next segment of the bulk data

                    print(f"Processing {len(batch_to_process)} card(s) in current batch segment...")
                    tasks = [process_card_data(session, card_data, image_download_client) for card_data in batch_to_process]
                                        
                    # Process a batch of cards concurrently
                    await asyncio.gather(*tasks)
                    
                    processed_count_in_batch = len(batch_to_process)
                    processed_count_since_last_commit += processed_count_in_batch
                    print(f"Processed {processed_count_in_batch} card(s). Total cards scanned from bulk: {total_scanned_so_far}/{len(all_cards_data)}")

                    if processed_count_since_last_commit >= commit_batch_size:
                        print(f"Committing {processed_count_since_last_commit} records...")
                        await session.commit()
                        print("Batch committed.")
                        processed_count_since_last_commit = 0
                    
                # This final commit block was correctly placed after the loop,
                # but the 'finally' block for session.close() is not strictly needed
                # due to the 'async with AsyncSessionLocal() as session:' context manager.
                if processed_count_since_last_commit > 0: # Commit any remaining cards
                    print(f"Committing final {processed_count_since_last_commit} records...")
                    await session.commit()
                    print("Final commit complete.")
            except Exception as e:
                print(f"An error occurred during bulk processing: {e}")
                await session.rollback()
            # 'finally: await session.close()' is not needed here as the context manager handles it.


    print("Card population process finished.")

if __name__ == "__main__":
    asyncio.run(main_populate())
# This script will download the latest Scryfall bulk data and populate your database with card definitions.