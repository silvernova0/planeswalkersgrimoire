<!-- filepath: c:\Users\social\pg\mtg-collection-frontend\src\views\TopCommanders.vue -->
<template>
  <div>
    <h1>Top cEDH Commanders</h1>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
const commanders = ref([])

onMounted(async () => {
  const resp = await fetch('/api/meta/top-commanders')
  commanders.value = await resp.json()
})
</script>

<style scoped>
.commander-block {
  margin-bottom: 2em;
  padding: 1em;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>