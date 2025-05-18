<template>
  <div class="collection-page">
    <h1>My Collection</h1>

    <!-- Card Search and Add Section -->
    <CardSearch @card-selected="handleCardSelectedForAddition" />

    <!-- Modal/Form for adding card details -->
    <div v-if="cardToAdd" class="add-card-modal-overlay">
      <div class="add-card-modal">
        <h3>Add "{{ cardToAdd.name }}" to Collection</h3>
        <img v-if="cardToAdd.image_uris?.normal" :src="cardToAdd.image_uris.normal" :alt="cardToAdd.name" class="modal-card-image" />
        <form @submit.prevent="confirmAddCardToCollection" class="add-card-form">
          <div>
            <label for="quantity">Quantity:</label>
            <select id="quantity" v-model.number="addDetails.quantity">
              <option v-for="n in 10" :key="n" :value="n">{{ n }}</option> <!-- Changed range to 1-10 -->
            </select>
            <!-- <input type="number" id="quantity" v-model.number="addDetails.quantity" min="1" required /> -->
          </div>
          <div>
            <label for="condition">Condition:</label>
            <select id="condition" v-model="addDetails.condition">
              <option value="NM">Near Mint (NM)</option>
              <option value="LP">Lightly Played (LP)</option>
              <option value="MP">Moderately Played (MP)</option>
              <option value="HP">Heavily Played (HP)</option>
              <option value="DMG">Damaged (DMG)</option>
            </select>
          </div>
          <div>
            <label for="isFoil">Foil:</label>
            <input type="checkbox" id="isFoil" v-model="addDetails.isFoil" />
          </div>
          <!-- Add other fields like language, notes if needed -->
          <div class="modal-actions">
            <button type="submit" :disabled="isAddingCard">Confirm Add</button>
            <button type="button" @click="cancelAddCard" :disabled="isAddingCard">Cancel</button>
          </div>
          <p v-if="addCardError" class="error-message">{{ addCardError }}</p>
        </form>
      </div>
    </div>

    <!-- Display User's Collection -->
    <div v-if="isLoadingCollection" class="loading-message">Loading your collection...</div>
    <p v-else-if="!isLoadingCollection && userCollectionError" class="error-message">{{ userCollectionError }}</p>
    <div v-else-if="!isLoadingCollection && userCollection.length === 0 && !userCollectionError" class="empty-collection-message">
      <p>Your collection is empty. Use the search above to find and add cards!</p>
    </div>
    <div v-else-if="!isLoadingCollection && userCollection.length > 0 && !userCollectionError" class="collection-grid">
      <div v-for="item in userCollection" :key="item.id" class="collection-item">
        <!-- Display your collected card details here. Adjust 'item' properties based on your API response -->
        <img :src="getCardImageUrl(item.card_definition)" :alt="item.card_definition?.name || 'Card Image'" class="collection-card-image"/>
        <p class="card-name"><strong>{{ item.card_definition?.name || 'Unknown Card' }}</strong></p>
        <p class="card-detail" v-if="item.quantity_normal > 0">Quantity (Normal): {{ item.quantity_normal }}</p>
        <p class="card-detail" v-if="item.quantity_foil > 0">Quantity (Foil): {{ item.quantity_foil }}</p>
        <p class="card-detail">Condition: {{ item.condition }}</p>
        <!-- You might want a button to edit/remove items here in the future -->
      </div>
    </div>
  </div>
</template>

<script setup>
// Potentially some basic script
import { ref, onMounted } from 'vue';
import CardSearch from '../components/CardSearch.vue'; // Ensure path is correct
import api from '../services/api'; // Your API service
import authStore from '../store/auth'; // If needed for auth token implicitly by api service

const userCollection = ref([]);
const isLoadingCollection = ref(false);
const cardToAdd = ref(null); // Stores the card object selected from search
const addDetails = ref({
  quantity: 1,
  condition: 'NM',
  isFoil: false,
});
const addCardError = ref('');
const isAddingCard = ref(false);
const userCollectionError = ref(''); // For displaying errors when fetching collection
const defaultCardImage = 'https://via.placeholder.com/100x140.png?text=No+Image'; // Placeholder

const fetchUserCollection = async () => {
  isLoadingCollection.value = true;
  userCollectionError.value = ''; // Reset error before fetching
  try {
    // Ensure api.getUserCollection() is implemented and returns an array in response.data
    const response = await api.getUserCollection();
    userCollection.value = response.data; // Adjust based on your API response structure
  } catch (error) {
    console.error('Error fetching user collection:', error);
    userCollectionError.value = 'Failed to load your collection. Please try refreshing the page or try again later.';
  } finally {
    isLoadingCollection.value = false;
    };

// Helper to construct full image URL
const getCardImageUrl = (cardDefinition) => {
  if (!cardDefinition) return defaultCardImage;

  // Option 1: If your API provides a direct relative path for a locally served image
  // (e.g., in cardDefinition.local_image_url_small or even cardDefinition.image_uris.small if it's relative)
  const localRelativePath = cardDefinition.local_image_url_small || cardDefinition.image_uris?.small; // Adjust field based on your API structure

  if (localRelativePath) {
    if (localRelativePath.startsWith('http://') || localRelativePath.startsWith('https://')) {
      return localRelativePath; // It's already an absolute URL
    }
    // Construct full URL for relative path from your API
    const baseUrl = api.defaults.baseURL.replace(/\/$/, ''); // Remove any trailing slash from API base URL
    const path = localRelativePath.startsWith('/') ? localRelativePath : `/${localRelativePath}`; // Ensure leading slash for path
    return `${baseUrl}${path}`;
  }

  // Option 2: Fallback to a Scryfall direct image URL if available and no local path
  // This line might be redundant if image_uris.small was already checked above and was a Scryfall URL.
  // if (cardDefinition.image_uris?.small) return cardDefinition.image_uris.small;

  return defaultCardImage; // Default placeholder if no image found
  }
};

const handleCardSelectedForAddition = (card) => {
  cardToAdd.value = card;
  // Reset details for the new card
  addDetails.value = { quantity: 1, condition: 'NM', isFoil: false }; // Default quantity is 1
  addCardError.value = '';
};

const confirmAddCardToCollection = async () => {
  if (!cardToAdd.value) return;
  isAddingCard.value = true;
  addCardError.value = '';
  try {
    const payload = {
      card_definition_scryfall_id: cardToAdd.value.scryfall_id, // Send scryfall_id
      // Assuming addDetails.value.quantity is the total quantity for this condition/foil status
      quantity_normal: addDetails.value.isFoil ? 0 : addDetails.value.quantity,
      quantity_foil: addDetails.value.isFoil ? addDetails.value.quantity : 0,
      condition: addDetails.value.condition,
      // language: "en", // Uncomment and set if you have this field
      // notes: "", // Uncomment and set if you have this field
    };
    // You'll need to implement `addCardToCollection` in your api.js
    await api.addCardToCollection(payload);
    cardToAdd.value = null; // Close modal/form
    await fetchUserCollection(); // Refresh collection to show the new card
  } catch (error) {
    console.error('Error adding card to collection:', error);
    addCardError.value = error.response?.data?.detail || 'Failed to add card. Please try again.';
  } finally {
    isAddingCard.value = false;
  }
};

const cancelAddCard = () => {
  cardToAdd.value = null;
  addCardError.value = '';
};

onMounted(() => {
  // Fetch collection when component mounts, if user is authenticated
  if (authStore.token) { // Or however you check authentication status
    fetchUserCollection();
  }
});
</script>

<style scoped>
.collection-page { padding: 20px; max-width: 1200px; margin: auto; }
.loading-message, .empty-collection-message, .error-message { text-align: center; margin-top: 20px; padding: 10px; }
.error-message { color: red; background-color: #ffebee; border: 1px solid #ef9a9a; border-radius: 4px; }

.add-card-modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.add-card-modal { background-color: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); width: 90%; max-width: 500px; }
.add-card-modal h3 { margin-top: 0; margin-bottom: 15px; color: #333; /* Darker color for heading */ }
.modal-card-image { max-width: 150px; display: block; margin: 0 auto 15px auto; border-radius: 6px; }
.add-card-form div { margin-bottom: 12px; }
.add-card-form label { display: block; margin-bottom: 5px; font-weight: bold; color: #444; /* Slightly darker label color */ }
.add-card-form input[type="number"], .add-card-form select { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.add-card-form input[type="checkbox"] { margin-right: 5px; vertical-align: middle; }
.modal-actions { margin-top: 20px; display: flex; justify-content: flex-end; gap: 10px; }
.modal-actions button { padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
.modal-actions button[type="submit"] { background-color: #28a745; color: white; }
.modal-actions button[type="button"] { background-color: #6c757d; color: white; }

.collection-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
.collection-item { border: 1px solid #ddd; border-radius: 8px; padding: 15px; background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.collection-card-image { max-width: 100%; height: auto; border-radius: 6px; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto; }
.collection-item p { margin: 5px 0; font-size: 0.9em; }
.collection-item strong { font-size: 1em; }
.collection-item .card-name strong {
  color: #333333; /* Dark color for card name, ensuring visibility */
}
.collection-item .card-detail {
  color: #555555; /* Medium-dark color for details */
}
</style>