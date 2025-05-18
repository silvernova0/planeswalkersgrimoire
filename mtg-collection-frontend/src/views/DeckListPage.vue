<template>
  <div>
    <h1>My Decks</h1>
    <form @submit.prevent="createDeck">
      <input v-model="newDeckName" placeholder="New deck name" required />
      <select v-model="newDeckCategory" required>
        <option disabled value="">Select format</option>
        <option>Standard</option>
        <option>Modern</option>
        <option>Pauper</option>
        <option>Commander</option>
      </select>
      <button type="submit">Create Deck</button>
    </form>
    <div v-if="decks.length === 0" style="margin-top: 1em;">No decks yet.</div>
    <ul>
      <li v-for="deck in decks" :key="deck.id" style="margin-bottom: 1em;">
        <strong>{{ deck.name }}</strong> <em>({{ deck.category }})</em>
        <span v-if="deck.category === 'Commander' && deck.commander">
          — Commander: <strong>{{ deck.commander.name }}</strong>
        </span>
        <button @click="selectDeck(deck)">Edit</button>
        <button @click="viewDeck(deck)">View</button>
      </li>
    </ul>

    <!-- Read-only Deck View -->
    <div v-if="viewedDeck" class="deck-view-modal">
      <div class="deck-view-content">
        <h2>View Deck: {{ viewedDeck.name }}</h2>
        <p><strong>Format:</strong> {{ viewedDeck.category }}</p>
        <div v-if="viewedDeck.category === 'Commander' && viewedDeck.commander">
          <p><strong>Commander:</strong> {{ viewedDeck.commander.name }} ({{ viewedDeck.commander.color_identity?.join(',') }})</p>
        </div>
        <ul>
          <li v-for="(card, idx) in viewedDeck.cards" :key="idx">
            {{ card.name }}
            <span v-if="card.color_identity && card.color_identity.length">
              ({{ card.color_identity.join(',') }})
            </span>
          </li>
        </ul>
        <button @click="closeViewDeck">Close</button>
      </div>
    </div>

    <div v-if="selectedDeck">
      <h2>Edit Deck: {{ selectedDeck.name }}</h2>
      <div v-if="showCommanderPrompt">
        <p><strong>Select your commander:</strong></p>
        <CardSearch @card-selected="handleCardSelected" />
        <button @click="addCardToDeck" :disabled="!selectedCard">Set Commander</button>
      </div>
      <div v-else>
        <CardSearch @card-selected="handleCardSelected" />
        <button @click="addCardToDeck" :disabled="!selectedCard">Add Card</button>
      </div>
      <div v-if="selectedDeck.category === 'Commander' && selectedDeck.commander">
        <p><strong>Commander:</strong> {{ selectedDeck.commander.name }} ({{ selectedDeck.commander.color_identity?.join(',') }})</p>
      </div>
      <ul>
        <li v-for="(card, idx) in selectedDeck.cards" :key="idx">
          {{ card.name }}
          <span v-if="card.color_identity && card.color_identity.length">
            ({{ card.color_identity.join(',') }})
          </span>
        </li>
      </ul>
      <button @click="selectedDeck = null">Done</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '../services/api';
import CardSearch from '../components/CardSearch.vue';

const decks = ref([]);
const newDeckName = ref('');
const newDeckCategory = ref('');
const selectedDeck = ref(null);
const viewedDeck = ref(null);

const selectedCard = ref(null);

function createDeck() {
  const deck = {
    id: Date.now(),
    name: newDeckName.value,
    category: newDeckCategory.value,
    cards: [],
    commander: null // Only used for Commander decks
  };
  decks.value.push(deck);
  newDeckName.value = '';
  newDeckCategory.value = '';
  selectDeck(deck);
}

function selectDeck(deck) {
  selectedDeck.value = deck;
  selectedCard.value = null;
}

function viewDeck(deck) {
  viewedDeck.value = deck;
}

function closeViewDeck() {
  viewedDeck.value = null;
}

function handleCardSelected(card) {
  selectedCard.value = card;
}

function addCardToDeck() {
  if (!selectedDeck.value || !selectedCard.value) return;

  if (selectedDeck.value.category === 'Commander' && !selectedDeck.value.commander) {
    // First card is the commander
    selectedDeck.value.commander = selectedCard.value;
    selectedCard.value = null;
    return;
  }

  // For Commander, enforce color identity
  if (selectedDeck.value.category === 'Commander' && selectedDeck.value.commander) {
    const commanderColors = selectedDeck.value.commander.color_identity || [];
    const cardColors = selectedCard.value.color_identity || [];
    // Only allow if every color in the card is in the commander (subset)
    const isSubset = cardColors.every(c => commanderColors.includes(c));
    // Also, block if the card has a color not in the commander
    if (cardColors.length > 0 && !isSubset) {
      alert('This card does not match your commander\'s color identity.');
      return;
    }
  }

  selectedDeck.value.cards.push(selectedCard.value);
  selectedCard.value = null;
}

const showCommanderPrompt = computed(() =>
  selectedDeck.value &&
  selectedDeck.value.category === 'Commander' &&
  !selectedDeck.value.commander
);
</script>

<style scoped>
form {
  margin-bottom: 1em;
}
input, select {
  margin-right: 0.5em;
}
.deck-view-modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
}
.deck-view-content {
  background: #fff;
  padding: 2em;
  border-radius: 8px;
  min-width: 300px;
  max-width: 90vw;
  box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}
.search-results {
  background: #fff;
  border: 1px solid #ccc;
  max-height: 150px;
  overflow-y: auto;
  position: absolute;
  z-index: 10;
  width: 200px;
  list-style: none;
  padding: 0;
  margin: 0.2em 0 0 0;
}
.search-results li {
  padding: 0.3em 0.5em;
}
.search-results li:hover {
  background: #eee;
}
</style>
