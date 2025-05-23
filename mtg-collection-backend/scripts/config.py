# edhrec_scraper/config.py

# --- URLs ---
BASE_URL_EDHREC = "https://edhrec.com"
COMMANDERS_URL = f"{BASE_URL_EDHREC}/commanders"  # Entry point for all commanders
CARDS_URL_TEMPLATE = f"{BASE_URL_EDHREC}/cards/{{card_slug}}" # Use .format(card_slug="your-card-slug")

# --- Scraping Behavior ---
REQUEST_DELAY_SECONDS = 2  # Time to wait between requests (IMPORTANT for respectful scraping)
REQUEST_TIMEOUT_SECONDS = 20 # How long to wait for a response before giving up
USER_AGENT = "PlaneswalkersGrimoireScraper/1.0 (Contact: silvernova0@gmail.com; GitHub: https://github.com/silvernova0/planeswalkersgrimoire)" # Be a good internet citizen! Please update email.

# --- Optional: Limits and Refresh Intervals (Uncomment and adjust if you implement this logic) ---
# COMMANDER_SCRAPE_LIMIT = 0 # 0 means no limit. Set to a positive number to limit commanders scraped (for testing).
# CARD_SCRAPE_LIMIT = 0      # 0 means no limit. Set to a positive number to limit cards scraped (for testing).
# REFRESH_INTERVAL_DAYS_COMMANDER = 7 # Re-scrape commander EDHREC data if older than this many days.
# REFRESH_INTERVAL_DAYS_CARD_STATS = 30 # Re-scrape EDHREC card stats (in 'cards' table) if older.
# REFRESH_INTERVAL_DAYS_CARD_SYNERGY = 14 # Re-scrape card-card synergy data if older.

# --- Database Connection ---
# It's best practice to use environment variables for sensitive data like passwords.
# For simplicity in this setup, we're defining them here.
# Ensure this file is in your .gitignore if you commit actual credentials.

DB_NAME = "your_mtg_db"  # Replace with your actual DB name from your setup
DB_USER = "postgres"            # Replace with your actual PostgreSQL username
DB_PASSWORD = "B0r3dd00"      # Replace with your actual PostgreSQL password
DB_HOST = "localhost"                     # Replace if your DB is hosted elsewhere (e.g., a Docker container IP)
DB_PORT = "5432"                          # Standard 