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
.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem auto; /* Centering with some top/bottom margin */
  padding: 2rem;
  background-color: #fff; /* Light mode background */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  max-width: 400px; /* Or appropriate width */
}

@media (prefers-color-scheme: dark) {
  .login-page {
    background-color: #2d3748; /* A common dark background, adjust as needed */
    /* Text colors for inputs and labels should ideally be handled by global styles or inherit correctly.
       If not, they might need specific overrides here for dark mode. */
  }
  .login-page h2 { /* Example if h2 needs color adjustment for dark mode */
    color: rgba(255, 255, 255, 0.87);
  }
   .login-page label { /* Example if labels need color adjustment for dark mode */
    color: rgba(255, 255, 255, 0.7);
  }
  .login-page .error-message {
    color: #f9a9a9; /* Lighter red for dark mode */
  }
  .login-page a {
    color: #8cb4ff; /* Lighter blue for links in dark mode */
  }
  .login-page a:hover {
    color: #a7c7ff;
  }
}

.login-form div { margin-bottom: 10px; width: 100%; } /* Ensure form elements take width */
.login-form label { margin-right: 5px; display: block; margin-bottom: 0.3em; text-align: left; } /* Align labels left */
.error-message { color: red; margin-top: 10px; }
/* Buttons and inputs should pick up global styles */
button { margin-top: 10px; padding: 8px 15px; width: 100%;} /* Make button full width */
input[type="text"], input[type="password"] { width: 100%; box-sizing: border-box; } /* Make inputs full width */
</style>