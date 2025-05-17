<script setup>
import Navbar from './components/Navbar.vue';
</script>

<template>
  <Navbar />
  <div class="container">
    <router-view></router-view>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
