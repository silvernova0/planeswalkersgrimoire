<script setup>
import Navbar from './components/Navbar.vue';
</script>

<template>
  <Navbar />
  <div class="container">
    <router-view></router-view>
  </div>
</template>

<style> /* Changed from 'scoped' to apply globally or to a root element */
body {
  margin: 0; /* Remove default body margin */
  font-family: sans-serif; /* Optional: A default font for the app */
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  /* Padding adjusted or removed to accommodate Tailwind CSS */
}
</style>
