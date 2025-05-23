# edhrec_scraper/edhrec_client.py
import requests
import time
from .config import REQUEST_DELAY_SECONDS, USER_AGENT, REQUEST_TIMEOUT_SECONDS

# Initialize a session object
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

def get_html(url: str) -> requests.Response | None:
    """
    Fetches HTML content from a given URL using the configured session,
    with rate limiting and error handling.
    """
    print(f"CLIENT: Attempting to fetch URL: {url}")
    try:
        print(f"CLIENT: Waiting for {REQUEST_DELAY_SECONDS} seconds (rate limiting)...")
        time.sleep(REQUEST_DELAY_SECONDS)
        
        response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status() # Raise HTTPError for bad responses (4XX or 5XX)
        
        print(f"CLIENT: Successfully fetched URL: {url} (Status: {response.status_code})")
        return response
        
    except requests.exceptions.HTTPError as http_err:
        print(f"CLIENT_ERROR: HTTP error occurred while fetching {url}: {http_err} (Status: {http_err.response.status_code if http_err.response else 'N/A'})")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"CLIENT_ERROR: Connection error occurred while fetching {url}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"CLIENT_ERROR: Timeout occurred while fetching {url}: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"CLIENT_ERROR: An unexpected error occurred while fetching {url}: {req_err}")
    
    return None