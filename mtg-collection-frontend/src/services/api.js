import axios from 'axios';
import authStore from '../store/auth';
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000', // Your FastAPI backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add the auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = authStore.getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor to handle 401 errors (e.g., token expired)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token is invalid or expired
      authStore.clearAuth();
      // Redirect to login page
      // You might need to access the router instance here or emit an event
      // For simplicity, we'll just log and let the route guards handle redirection
      console.error("Unauthorized or token expired. Logging out.");
      // router.push('/login'); // If router is accessible here
      window.location.href = '/login'; // Fallback redirect
    }
    return Promise.reject(error);
  }
);

export default {
  login(credentials) {
    // FastAPI's OAuth2PasswordRequestForm expects form data
    return apiClient.post('/auth/token', credentials, { headers: {'Content-Type': 'application/x-www-form-urlencoded'} });
  },

  async searchCards(query) {
    // The actual endpoint might be /api/cards/search, /api/v1/cards/search or similar,
    // ensure this matches your backend route for searching cards from the main database.
    // Example: GET /api/cards/search?name=:cardName
    return apiClient.get(`/cards/search?name=${encodeURIComponent(query)}`);
  },

  async getUserCollection() {
    // Endpoint to get the logged-in user's collection.
    // Example: GET /api/users/me/collection
  return apiClient.get('/collection/cards/'); // Matches backend route
  },

  async addCardToCollection(payload) {
    // Endpoint to add a card to the user's collection
    // payload: { card_id (e.g. scryfall_id), quantity, condition, is_foil, ... }
    // Example: POST /api/users/me/collection
  return apiClient.post('/collection/cards/', payload); // Matches backend route
  },

  // --- Deck Management ---
  async createDeck(deckData) {
    // deckData: { name: string, description?: string, format?: string }
    return apiClient.post('/decks/', deckData);
  },

  async getUserDecks() {
    return apiClient.get('/decks/');
  },

  async getDeckDetails(deckId) {
    return apiClient.get(`/decks/${deckId}/`);
  },

  async addCardToDeck(deckId, cardData) {
    // cardData: { card_definition_scryfall_id: string, quantity: int, is_commander?: bool, is_sideboard?: bool }
    return apiClient.post(`/decks/${deckId}/cards/`, cardData);
  },

  async register(userData) {
    // userData: { username, email, password }
    return apiClient.post('/users/', userData);
  }
  // You can add other API calls here (e.g., register, updateCollectionItem, deleteCollectionItem)
};
