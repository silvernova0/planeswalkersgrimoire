// c:\Users\social\Desktop\mtg-collection-frontend\src\router\index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';
import CollectionPage from '../views/CollectionPage.vue';
import authStore from '../store/auth';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
  },
  {
    path: '/collection',
    name: 'Collection',
    component: CollectionPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/',
    redirect: () => {
      if (!authStore.getToken()) {
        return { name: 'Login' };
      } else {
        return { name: 'Collection' };
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // import.meta.env.BASE_URL is good practice for Vite
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authStore.getToken()) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router; // This is the crucial default export
