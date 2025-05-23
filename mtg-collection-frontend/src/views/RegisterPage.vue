<template>
  <div class="register-page-container">
    <h2>Register</h2>
    <form @submit.prevent="register" class="register-form">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Register</button>
      <div v-if="error" style="color:red">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function register() {
  error.value = ''
  try {
    const res = await fetch('http://127.0.0.1:8000/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    })
    if (!res.ok) {
      const data = await res.json()
      error.value = data.detail || 'Registration failed'
      return
    }
    // Optionally, redirect to login after registration
    router.push({ name: 'Login' })
  } catch (e) {
    error.value = 'Network error'
  }
}
</script>

<style scoped>
.register-page-container {
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
  .register-page-container {
    background-color: #2d3748; /* A common dark background, adjust as needed */
  }
  .register-page-container h2 {
    color: rgba(255, 255, 255, 0.87);
  }
  .register-page-container .error { /* Assuming error messages have a .error class or similar */
    color: #f9a9a9; /* Lighter red for dark mode */
  }
}

.register-form { /* Specific styling for the form if needed */
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.register-form input {
  margin-bottom: 10px; /* Spacing between inputs */
  width: 100%; /* Make inputs take full width of form */
  box-sizing: border-box; /* Include padding and border in the element's total width and height */
}

.register-form button {
  width: 100%; /* Make button take full width of form */
  margin-top: 10px; /* Space above the button */
}

.error { /* Style for the error message div */
  color: red; /* Standard red for light mode */
  margin-top: 10px;
}
</style>