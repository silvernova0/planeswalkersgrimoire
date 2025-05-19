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
  /* If your image is in public/background.png */
  background-image: url('/background.png');
  /* If your image is in public/images/background.png */
  /* background-image: url('/images/background.png'); */

  background-size: 100% 100%; /* Stretch to cover entire page */
  background-position: center center; /* Center the image */
  background-repeat: no-repeat; /* Do not repeat the image */
  background-attachment: fixed; /* Keep the background fixed during scroll */
  margin: 0; /* Remove default body margin */
  font-family: sans-serif; /* Optional: A default font for the app */
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 20px 250px; /* Add left padding for sidebar */
  /* Optional: Add a semi-transparent background to the container if text is hard to read over the main background */
  /* background-color: rgba(255, 255, 255, 0.8); */
  /* border-radius: 8px; */
}
</style>
