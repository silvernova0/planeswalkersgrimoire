<template>
  <nav class="navbar">
    <router-link to="/collection" class="nav-link">My Collection</router-link>
    <router-link to="/decks" class="nav-link">My Decks</router-link> <!-- Added Decks link -->
    <button v-if="isLoggedIn" @click="logout" class="logout-button">Logout</button>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import authStore from '../store/auth';

const router = useRouter();
const isLoggedIn = computed(() => !!authStore.getToken());

const logout = () => {
  authStore.clearAuth();
  router.push('/login');
};
</script>

<style scoped>
.navbar {
  background-color: #333;
  padding: 1rem;
  display: flex; /* Using flex for layout */
  justify-content: flex-start; /* Align links to the start */
  align-items: center;
}
.nav-link {
  color: white;
  margin-right: 1rem;
  text-decoration: none;
}
.nav-link:hover {
  text-decoration: underline;
}
.logout-button {
  margin-left: auto; /* Pushes logout button to the right */
  background-color: #555;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
.logout-button:hover {
  background-color: #777;
}
</style>