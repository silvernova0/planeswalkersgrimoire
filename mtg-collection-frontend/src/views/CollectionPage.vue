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

    <!-- Filters Section -->
    <div class="collection-filters">
      <label>
        Set Code:
        <select v-model="filters.set">
          <option value="">All</option>
          <option v-for="set in uniqueSets" :key="set" :value="set">{{ set }}</option>
        </select>
      </label>
      <label>
        Card Type:
        <select v-model="filters.type">
          <option value="">All</option>
          <option v-for="type in uniqueTypes" :key="type" :value="type">{{ type }}</option>
        </select>
      </label>
      <label>
        Colors:
        <select v-model="filters.colors" multiple>
          <option v-for="color in colorOptions" :key="color" :value="color">{{ color }}</option>
        </select>
      </label>
      <label>
        Language:
        <select v-model="filters.language">
          <option value="">All</option>
          <option v-for="lang in languageOptions" :key="lang" :value="lang">{{ lang }}</option>
        </select>
      </label>
      <button @click="resetFilters">Reset Filters</button>
    </div>

    <!-- Display User's Collection -->
    <div v-if="isLoadingCollection" class="loading-message">Loading your collection...</div>
    <p v-else-if="!isLoadingCollection && userCollectionError" class="error-message">{{ userCollectionError }}</p>
    <div v-else-if="!isLoadingCollection && userCollection.length === 0 && !userCollectionError" class="empty-collection-message">
      <p>Your collection is empty. Use the search above to find and add cards!</p>
    </div>
    <div v-else-if="!isLoadingCollection && userCollection.length > 0 && !userCollectionError" class="collection-grid">
      <div v-for="item in paginatedCollection" :key="item.id" class="collection-item">
        <img
          :src="getCardImageUrl(item.card_definition)"
          :alt="item.card_definition?.name || 'Card Image'"
          class="collection-card-image"
          @error="event => event.target.src = defaultCardImage"
        />
        <p class="card-name"><strong>{{ item.card_definition?.name || 'Unknown Card' }}</strong></p>
        <p class="card-detail">
          Set: <strong>{{ item.card_definition.set?.toUpperCase() }}</strong>
          <span v-if="item.card_definition.set_name">({{ item.card_definition.set_name }})</span>
          <span v-if="item.card_definition.collector_number"> - #{{ item.card_definition.collector_number }}</span>
        </p>
        <p class="card-detail" v-if="item.quantity_normal > 0">Quantity (Normal): {{ item.quantity_normal }}</p>
        <p class="card-detail" v-if="item.quantity_foil > 0">Quantity (Foil): {{ item.quantity_foil }}</p>
        <p class="card-detail">Condition: {{ item.condition }}</p>
        <button @click="removeCardFromCollection(item)" style="margin-top:10px;color:red;">Remove</button>
      </div>
    </div>
    <!-- Pagination Controls -->
    <div v-if="totalPages > 1" class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<script setup>
// Potentially some basic script
import { ref, onMounted, computed } from 'vue';
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
const defaultCardImage = 'https://via.placeholder.com/150x210.png?text=No+Image';

const CARDS_PER_PAGE = 15;
const currentPage = ref(1);

const filters = ref({
  set: '',
  type: '',
  colors: [],
  language: '', // show all by default
});

const mainTypes = [
  'Sorcery', 'Land', 'Kindred', 'Planeswalker', 'Battle',
  'Instant', 'Creature', 'Enchantment', 'Artifact'
];

const uniqueTypes = computed(() => {
  const types = userCollection.value
    .map(item => {
      const typeLine = item.card_definition.type_line || '';
      return mainTypes.find(type => typeLine && typeLine.includes(type));
    })
    .filter(Boolean);
  return mainTypes.filter(type => types.includes(type));
});

const uniqueSets = computed(() => [...new Set(userCollection.value.map(item => item.card_definition.set?.toUpperCase()).filter(Boolean))]);
const languageOptions = computed(() => [...new Set(userCollection.value.map(item => item.card_definition.lang || 'en'))]);
const colorOptions = ['W', 'U', 'B', 'R', 'G', 'C', 'M']; // White, Blue, Black, Red, Green, Colorless, Multicolor

function resetFilters() {
  filters.value = { set: '', type: '', colors: [], language: 'en' };
}

// Filtered collection
const filteredCollection = computed(() => {
  return userCollection.value.filter(item => {
    const def = item.card_definition;
    // Set filter
    if (filters.value.set && def.set?.toUpperCase() !== filters.value.set) return false;
    // Type filter
    if (filters.value.type && !def.type_line?.includes(filters.value.type)) return false;
    // Language filter
    if (filters.value.language && def.lang !== filters.value.language) return false;
    // Colors filter (multi-select, must match all selected)
    if (filters.value.colors.length > 0) {
      const cardColors = def.color_identity || [];
      if (!filters.value.colors.every(c => cardColors.includes(c))) return false;
    }
    return true;
  });
});

// Use filteredCollection for pagination
const paginatedCollection = computed(() => {
  const start = (currentPage.value - 1) * CARDS_PER_PAGE;
  return filteredCollection.value.slice(start, start + CARDS_PER_PAGE);
});
const totalPages = computed(() =>
  Math.ceil(filteredCollection.value.length / CARDS_PER_PAGE)
);

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
  }
};

// Helper to construct full image URL
const getCardImageUrl = (cardDefinition) => {
  if (!cardDefinition) return defaultCardImage;
  // Try local image first
  const localRelativePath = cardDefinition.local_image_url_small || cardDefinition.image_uris?.small;
  if (localRelativePath) {
    if (localRelativePath.startsWith('http://') || localRelativePath.startsWith('https://')) {
      return localRelativePath;
    }
    // If it's a relative path, prepend your API base URL
    const baseUrl = api.defaults.baseURL?.replace(/\/$/, '') || '';
    const path = localRelativePath.startsWith('/') ? localRelativePath : `/${localRelativePath}`;
    return `${baseUrl}${path}`;
  }
  // Fallback to placeholder
  return defaultCardImage;
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

async function removeCardFromCollection(item) {
  if (!confirm(`Remove ${item.card_definition?.name || 'this card'} from your collection?`)) return;
  try {
    await api.removeCardFromCollection(item.id); // Implement this in your api.js
    await fetchUserCollection();
  } catch (error) {
    alert('Failed to remove card.');
  }
}

onMounted(() => {
  fetchUserCollection();
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

.collection-filters {
  display: flex;
  gap: 1em;
  margin-bottom: 1em;
  flex-wrap: wrap;
}
.collection-filters label {
  display: flex;
  flex-direction: column;
  font-size: 0.95em;
}
.collection-filters select[multiple] {
  min-width: 80px;
  min-height: 60px;
}

.collection-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-auto-rows: 1fr;
  gap: 20px;
  margin-top: 20px;
}
.collection-item { border: 1px solid #ddd; border-radius: 8px; padding: 15px; background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05); position: relative; }
.collection-card-image { max-width: 100%; height: auto; border-radius: 6px; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto; }
.collection-item p { margin: 5px 0; font-size: 0.9em; }
.collection-item strong { font-size: 1em; }
.collection-item .card-name strong {
  color: #333333; /* Dark color for card name, ensuring visibility */
}
.collection-item .card-detail {
  color: #555555; /* Medium-dark color for details */
}
.hover-image-container {
  position: relative;
}
.hover-image {
  display: none;
  position: absolute;
  top: 10px;
  left: 110%;
  z-index: 10;
  background: white;
  border: 1px solid #ccc;
  padding: 5px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.hover-image-container:hover .hover-image {
  display: block;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1em;
  margin-top: 20px;
}
.pagination-controls button {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
}
.pagination-controls button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
.pagination-controls span {
  font-size: 1em;
  color: #333;
}
</style>