import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // Import the router instance


const app = createApp(App)
// If you're using vue-router, you'd import and use it here:
// import router from './router' // Assuming you have router setup in src/router/index.js
// app.use(router)
app.use(router) // Tell Vue to use the router
app.mount('#app')
