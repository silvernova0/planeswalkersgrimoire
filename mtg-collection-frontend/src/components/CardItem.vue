<template>
  <div class="card-item">
    <!-- ... other card details ... -->
    <img
      v-if="localImageUrl && !localImageLoadError"
      :src="localImageUrl"
      :alt="card.name"
      class="card-image"
      @error="handleLocalImageError"
    />
    <div v-else-if="card.image_uri_small" class="placeholder-image">
      <!-- Fallback or placeholder if local image isn't available but Scryfall URI is -->
      <img :src="card.image_uri_small" :alt="card.name + ' (Scryfall)'" class="card-image-fallback"/>
      <p class="text-xs">Using Scryfall image</p>
    </div>
    <div v-else class="no-image-available">
      No Image
    </div>
    <!-- ... -->
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import apiClient from '@/services/api'; // Adjust path as needed

const props = defineProps({
  card: {
    type: Object,
    required: true
  }
});

const localImageLoadError = ref(false);

// Choose which local image size to prefer (e.g., normal, then small)
const localImageUrl = computed(() => {
  // Ensure card prop is available
  if (!props.card) return null;

  const baseUrl = apiClient.defaults.baseURL;
  let chosenPath = null;

  // Define the order of preference for local image URLs
  const potentialPaths = [
    props.card.local_image_url_normal,
    props.card.local_image_url_small,
    // props.card.local_image_url_large, // Add this if you implement it
  ];

  for (const path of potentialPaths) {
    if (path && typeof path === 'string' && path.trim() !== '') {
      chosenPath = path;
      break; // Found the preferred path
    }
  }

  if (chosenPath) {
    localImageLoadError.value = false; // Reset error state when URL might change

    // Check if chosenPath is already an absolute URL
    if (chosenPath.startsWith('http://') || chosenPath.startsWith('https://')) {
      return chosenPath; // Use it directly
    } else {
      // It's a relative path, construct the full URL (original logic)
      const trimmedBaseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash from base
      const trimmedRelativePath = chosenPath.replace(/^\//, ''); // Remove leading slash from relative
      return `${trimmedBaseUrl}/${trimmedRelativePath}`;
    }
  }

  return null;
});

function handleLocalImageError() {
  console.warn(`Failed to load local image: ${localImageUrl.value}`);
  localImageLoadError.value = true; // This will hide the broken local image and allow fallbacks to kick in
}
</script>

<style scoped>
.card-item {
  background-color: #fff; /* Light mode background */
  border-radius: 12px;
  padding: 1rem; /* Or adjust as needed */
  box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* Softer than global .card for individual items unless it should match global .card */
  margin-bottom: 1rem; /* Example spacing */
}

@media (prefers-color-scheme: dark) {
  .card-item {
    background-color: #2f2f2f; /* Dark mode background, similar to global .card */
  }
}

.card-image, .card-image-fallback {
  max-width: 100%;
  height: auto;
  border-radius: 8px; /* Rounded images within the card item */
}
.no-image-available {
  width: 100px; /* Adjust as needed */
  height: 140px; /* Adjust as needed */
  background-color: #eee; /* Light mode placeholder background */
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777;
  border-radius: 8px;
}

@media (prefers-color-scheme: dark) {
  .no-image-available {
    background-color: #3a3a3a; /* Dark mode placeholder background */
    color: #aaa;
  }
}

.placeholder-image .text-xs {
  font-size: 0.75rem;
  text-align: center;
  color: #555; /* Light mode text */
}

@media (prefers-color-scheme: dark) {
  .placeholder-image .text-xs {
    color: #bbb; /* Dark mode text */
  }
}
</style>
