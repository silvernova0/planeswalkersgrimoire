<template>
  <nav class="sidebar-navbar">
    <div class="navbar-title">Planeswalkers Grimoire</div>
    <router-link to="/" class="nav-link">Home</router-link>
    <router-link to="/collection" class="nav-link">My Collection</router-link>
    <router-link to="/decks" class="nav-link">My Decks</router-link>
    <router-link to="/credits" class="nav-link">Credits</router-link>
    <router-link to="/top-commanders" class="nav-link">Top Commanders</router-link>
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
.sidebar-navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 220px;
  height: 100vh;
  background: #23272f;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 2rem 1rem 1rem 1rem;
  box-shadow: 2px 0 8px rgba(0,0,0,0.08);
  z-index: 100;
}
.navbar-title {
  font-size: 1.3em;
  font-weight: bold;
  margin-bottom: 2em;
  color: #ffd700;
  letter-spacing: 1px;
}
.nav-link {
  color: #fff;
  margin-bottom: 1.2rem;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.08em;
  transition: color 0.2s;
  width: 100%;
  padding: 0.5em 0.8em;
  border-radius: 6px;
}
.nav-link:hover, .router-link-exact-active {
  background: #ffd700;
  color: #23272f !important;
  text-decoration: none;
}
.logout-button {
  margin-top: auto;
  background-color: #555;
  color: white;
  border: none;
  padding: 0.7rem 1.2rem;
  cursor: pointer;
  font-weight: bold;
  border-radius: 4px;
  width: 100%;
  transition: background 0.2s;
}
.logout-button:hover {
  background-color: #888;
}
</style>