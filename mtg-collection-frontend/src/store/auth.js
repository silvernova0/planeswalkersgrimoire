import { reactive, readonly } from 'vue';

const state = reactive({
  token: localStorage.getItem('authToken') || null,
  user: null, // You can store user details here after login if needed
});

const mutations = {
  setToken(token) {
    state.token = token;
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  },
  // setUser(user) { state.user = user; },
  clearAuth() {
    this.setToken(null);
    // this.setUser(null);
  },
};

export default {
  state: readonly(state), // Expose state as readonly
  setToken: mutations.setToken,
  clearAuth: mutations.clearAuth,
  getToken: () => state.token,
};