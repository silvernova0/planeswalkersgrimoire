<template>
  <div class="login-page">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
    <router-link to="/register">Register</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import authStore from '../store/auth';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

const handleLogin = async () => {
  errorMessage.value = '';
  try {
    // FastAPI's OAuth2PasswordRequestForm expects URL-encoded form data
    const formData = new URLSearchParams();
    formData.append('username', username.value);
    formData.append('password', password.value);

    const response = await api.login(formData);
    authStore.setToken(response.data.access_token);
    // You might want to fetch user details here and store them
    router.push('/collection'); // Redirect to collection page after login
  } catch (error) {
    console.error('Login failed:', error.response?.data || error.message);
    errorMessage.value = error.response?.data?.detail || 'Login failed. Please check your credentials.';
  }
};
</script>

<style scoped>
.login-page { display: flex; flex-direction: column; align-items: center; margin-top: 50px; }
.login-form div { margin-bottom: 10px; }
.login-form label { margin-right: 5px; }
.error-message { color: red; margin-top: 10px; }
button { margin-top: 10px; padding: 8px 15px; }
</style>