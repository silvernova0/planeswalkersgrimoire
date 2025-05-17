<template>
  <div>
    <h1>Deck Details</h1>
    <p>Details for deck ID: {{ deckId }} will go here.</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  deckId: {
    type: [String, Number],
    required: true,
  },
});
// Add script logic later
</script>

<style scoped>
/* Add styles later */
</style>
