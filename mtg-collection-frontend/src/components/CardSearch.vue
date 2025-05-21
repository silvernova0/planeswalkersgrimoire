<template>
  <div class="card-search">
    <input v-model="searchQuery" @keyup.enter="performSearch" placeholder="Search available cards..." />
    <button @click="performSearch" :disabled="isLoading">Search</button>
    <div v-if="isLoading" class="loading-message">Searching...</div>
    <ul v-if="searchResults.length > 0" class="search-results">
      <li v-for="card in searchResults" :key="card.id" class="search-result-item">
        <!-- Prioritize local images if available, then Scryfall, then default -->
        <img
          :src="card.local_image_url_small || card.local_image_url_normal || card.image_uris?.small || defaultCardImage"
          :alt="card.name"
          class="card-image-small"
        />
        <div class="card-info">
          <strong>{{ card.name }}</strong>
          <div class="card-set-details">
            <span v-if="card.set_name">{{ card.set_name }}</span>
            <span v-if="card.set_name && card.set_code"> &ndash; </span>
            <span v-if="card.set_code">[{{ card.set_code.toUpperCase() }}]</span>
          </div>
        </div>
        <button @click="selectCardForAddition(card)">Add to Collection</button>
      </li>
    </ul>
    <p v-if="!isLoading && searchAttempted && searchResults.length === 0" class="no-results-message">No cards found matching your query.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../services/api'; // Assuming your API service is in src/services/api.js

const searchQuery = ref('');
const searchResults = ref([]);
const isLoading = ref(false);
const searchAttempted = ref(false);
// Replace with a path to a real default image or handle missing images more gracefully
const defaultCardImage = 'https://via.placeholder.com/50x70.png?text=No+Image';

const emit = defineEmits(['card-selected']);

const performSearch = async () => {
  if (!searchQuery.value.trim()) return;
  isLoading.value = true;
  searchAttempted.value = true;
  searchResults.value = [];
  try {
    // You'll need to implement `searchCards` in your api.js service
    const response = await api.searchCards(searchQuery.value);
    searchResults.value = response.data; // Adjust based on your API response structure
  } catch (error) {
    console.error('Error searching cards:', error);
    // You might want to show an error message to the user here
  } finally {
    isLoading.value = false;
  }
};

const selectCardForAddition = (card) => {
  emit('card-selected', card);
};
</script>

<style scoped>
.card-search { margin-bottom: 20px; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #f9f9f9; }
.card-search input[type="text"] { padding: 8px; margin-right: 10px; border: 1px solid #ccc; border-radius: 4px; }
.card-search button { padding: 8px 15px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
.card-search button:disabled { background-color: #ccc; }
.loading-message, .no-results-message { margin-top: 10px; color: #555; }
.search-results { list-style: none; padding: 0; margin-top: 15px; }
.search-result-item { display: flex; align-items: center; margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; background-color: white; }
.card-image-small { width: 40px; height: auto; margin-right: 10px; border-radius: 3px; }
.card-info {
  flex-grow: 1;
}
.card-info strong {
  display: block; margin-bottom: 2px; color: #000000; /* Explicitly set card name color to black */
}
.card-set-details {
  font-size: 0.85em;
  color: #555;
}
.search-result-item button { margin-left: auto; padding: 5px 10px; background-color: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>