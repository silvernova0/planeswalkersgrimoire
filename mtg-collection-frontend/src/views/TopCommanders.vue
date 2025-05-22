<!-- filepath: c:\Users\social\pg\mtg-collection-frontend\src\views\TopCommanders.vue -->
<template>
  <div>
    <h1>Top cEDH Commanders</h1>
    <div v-if="isLoading" class="loading-message">Loading top commanders...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="!isLoading && !error && commanders.length === 0" class="empty-message">
      No top commanders found. The database might be updating or empty.
    </div>
    <div v-if="!isLoading && !error && commanders.length > 0">
      <div v-for="commander in commanders" :key="commander.commander" class="commander-block">
        <h2>{{ commander.commander }} <span style="font-size:0.8em;color:gray;">({{ commander.count }} decks)</span></h2>
        <ul>
          <li v-for="deck in commander.decks" :key="deck.id">
            <a :href="deck.url" target="_blank">{{ deck.name }}</a>
            <span v-if="deck.placement"> - Placement: {{ deck.placement }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api'; // Adjust path if necessary

const commanders = ref([]);
const isLoading = ref(false);
const error = ref(null);

onMounted(async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await api.getTopCommanders();
    commanders.value = response.data;
  } catch (err) {
    console.error("Error fetching top commanders:", err);
    error.value = "Failed to load top commanders. Please try again later.";
    // Optionally, you could try to get more specific error messages
    // if (err.response && err.response.data && err.response.data.detail) {
    //   error.value = err.response.data.detail;
    // }
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.commander-block {
  margin-bottom: 2em;
  padding: 1em;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.loading-message, .error-message, .empty-message {
  text-align: center;
  padding: 20px;
  margin-top: 20px;
}
.error-message {
  color: red;
  background-color: #ffebee;
  border: 1px solid #ef9a9a;
  border-radius: 4px;
}
</style>