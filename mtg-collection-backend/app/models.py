# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, LargeBinary, Float, Date
from sqlalchemy.dialects.postgresql import ARRAY, JSONB # For PostgreSQL specific types
from sqlalchemy.sql import func # For server-side default timestamp
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)  # Keep for legacy, but always set = email
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())

    collection_entries = relationship("UserCollectionEntry", back_populates="owner")
    decks = relationship("Deck", back_populates="owner")

class CardDefinition(Base): # Renamed from Card
    __tablename__ = "card_definitions"

    id = Column(Integer, primary_key=True, index=True)
    scryfall_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    set_code = Column(String)
    collector_number = Column(String)
    lang = Column(String, default="en", nullable=True) # Language of the card print
    type_line = Column(String, index=True, nullable=True) # Added for searching by type
    mana_cost = Column(String, nullable=True)
    cmc = Column(Float, nullable=True)
    oracle_text = Column(String, nullable=True)
    flavor_text = Column(String, nullable=True)
    power = Column(String, nullable=True)
    toughness = Column(String, nullable=True)
    loyalty = Column(String, nullable=True)
    colors = Column(ARRAY(String), nullable=True) # Colors in the mana cost
    color_identity = Column(ARRAY(String), nullable=True) # e.g., ['W','U','B','R','G']
    keywords = Column(ARRAY(String), nullable=True) # e.g., ["Flying", "Trample"]
    rarity = Column(String, nullable=True) # e.g., "common", "uncommon", "rare", "mythic"
    artist = Column(String, nullable=True)
    released_at = Column(String, nullable=True) # Date string, e.g., "2023-10-30"
    set_name = Column(String, nullable=True) # Full name of the set
    layout = Column(String, nullable=True) # e.g., "normal", "split", "transform"
    frame = Column(String, nullable=True) # e.g., "2015", "1997"
    border_color = Column(String, nullable=True) # e.g., "black", "white"
    full_art = Column(Boolean, nullable=True)
    textless = Column(Boolean, nullable=True)
    reprint = Column(Boolean, nullable=True)
    promo = Column(Boolean, nullable=True)
    digital = Column(Boolean, nullable=True) # Is it a digital-only card (e.g., Arena)
    foil = Column(Boolean, nullable=True) # Does this specific printing exist in foil
    nonfoil = Column(Boolean, nullable=True) # Does this specific printing exist in nonfoil
    oversized = Column(Boolean, nullable=True)
    story_spotlight = Column(Boolean, nullable=True)
    edhrec_rank = Column(Integer, nullable=True)

    legalities = Column(JSONB, nullable=True) # To store format legalities e.g. {"standard": "legal", "commander": "legal"}
    prices = Column(JSONB, nullable=True) # e.g. {"usd": "0.10", "usd_foil": "0.50"}
    card_faces = Column(JSONB, nullable=True) # For multi-faced cards
    all_parts = Column(JSONB, nullable=True) # Related card objects (tokens, meld parts)
    purchase_uris = Column(JSONB, nullable=True) # Links to buy the card
    related_uris = Column(JSONB, nullable=True) # Links to Gatherer, TCGplayer, etc.

    image_uri_small = Column(String, nullable=True)
    image_uri_normal = Column(String, nullable=True)
    image_uri_large = Column(String, nullable=True)
    image_uri_art_crop = Column(String, nullable=True)
    image_uri_border_crop = Column(String, nullable=True)
    scryfall_uri = Column(String, nullable=True) # Link to the card on Scryfall
    rulings_uri = Column(String, nullable=True) # Link to Scryfall rulings API
    prints_search_uri = Column(String, nullable=True) # Link to Scryfall API for all prints of this card

    # Columns for storing raw image data (already present)
    image_data_small = Column(LargeBinary, nullable=True)
    image_data_normal = Column(LargeBinary, nullable=True)
    image_data_large = Column(LargeBinary, nullable=True)

    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    collection_entries = relationship("UserCollectionEntry", back_populates="card_definition")
    deck_entries = relationship("DeckEntry", back_populates="card_definition")

class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    format = Column(String, nullable=True) # e.g., "Commander", "Standard", "Modern"
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    owner = relationship("User", back_populates="decks")
    deck_entries = relationship("DeckEntry", back_populates="deck", cascade="all, delete-orphan")

class DeckEntry(Base):
    __tablename__ = "deck_entries"

    id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    card_definition_id = Column(Integer, ForeignKey("card_definitions.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    is_commander = Column(Boolean, default=False)
    is_sideboard = Column(Boolean, default=False)

    deck = relationship("Deck", back_populates="deck_entries")
    card_definition = relationship("CardDefinition", back_populates="deck_entries")

class UserCollectionEntry(Base):
    __tablename__ = "user_collection_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_definition_id = Column(Integer, ForeignKey("card_definitions.id"), nullable=False) # Or use scryfall_id as FK

    quantity_normal = Column(Integer, default=0, nullable=False)
    quantity_foil = Column(Integer, default=0, nullable=False)
    condition = Column(String, nullable=True) # e.g., "NM", "LP"
    language = Column(String, default="en", nullable=False) # e.g., "en", "ja"
    notes = Column(String, nullable=True)
    date_added_to_collection = Column(DateTime(timezone=True), server_default=func.now())
    date_updated_in_collection = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    owner = relationship("User", back_populates="collection_entries")
    card_definition = relationship("CardDefinition", back_populates="collection_entries")

class MetaTournament(Base):
    __tablename__ = "meta_tournaments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=True)
    url = Column(String, nullable=False)

    decks = relationship("MetaDeck", back_populates="tournament")

class MetaDeck(Base):
    __tablename__ = "meta_decks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    commander = Column(String, nullable=True)
    tournament_id = Column(Integer, ForeignKey("meta_tournaments.id"))
    placement = Column(String, nullable=True)
    url = Column(String, nullable=False)

    tournament = relationship("MetaTournament", back_populates="decks")
    cards = relationship("MetaDeckCard", back_populates="deck")

class MetaDeckCard(Base):
    __tablename__ = "meta_deck_cards"
    id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey("meta_decks.id"))
    card_name = Column(String, nullable=False)
    set_code = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    is_commander = Column(Boolean, default=False)

    deck = relationship("MetaDeck", back_populates="cards")

# app/routers/meta.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func, desc
from app.models import MetaDeckCard, MetaDeck
from app.database import get_db

router = APIRouter()

@router.get("/meta/top-commanders")
async def get_top_commanders(db: AsyncSession = Depends(get_db)):
    # Get top 3 commanders by count
    result = await db.execute(
        select(
            MetaDeckCard.card_name,
            func.count(MetaDeckCard.deck_id).label("count")
        )
        .where(MetaDeckCard.is_commander == True)
        .group_by(MetaDeckCard.card_name)
        .order_by(desc("count"))
        .limit(3)
    )
    commanders = result.all()
    # For each commander, get 3 example decks
    data = []
    for commander, count in commanders:
        decks_result = await db.execute(
            select(MetaDeck)
            .join(MetaDeckCard, MetaDeck.id == MetaDeckCard.deck_id)
            .where(MetaDeckCard.card_name == commander, MetaDeckCard.is_commander == True)
            .limit(3)
        )
        decks = decks_result.scalars().all()
        data.append({
            "commander": commander,
            "count": count,
            "decks": [
                {
                    "id": d.id,
                    "name": d.name,
                    "placement": d.placement,
                    "url": d.url
                } for d in decks
            ]
        })
    return data

# app/frontend/login.js
// When logging in, send { username: email, password }
formData.append('username', email.value); // Use email as username
formData.append('password', password.value);