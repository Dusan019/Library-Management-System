import './assets/main.css';

import { createApp } from 'vue';
import App from './App.vue';
import Toast from 'vue-toastification';
import router from './router';
import axios from 'axios'; // Import Axios directly
import { startPeriodicTokenCheck,isTokenExpired } from '@/utils/authUtils';

const app = createApp(App);

// Periodic token check
startPeriodicTokenCheck(() => {
  router.push({ name: 'login' }); // Redirect to login if token expires
});

// Axios global configuration
axios.defaults.baseURL = 'http://127.0.0.1:5000'; // Set your backend's base URL

// Request interceptor to attach Authorization header
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      if (isTokenExpired(token)) {
        // If the token is expired, remove it and redirect to login
        localStorage.removeItem('token');
        router.push({ name: 'login' });
        return Promise.reject('Token expired');
      }
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle 401 errors and expired token
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || (error.response?.data?.message && error.response.data.message === 'Token expired')) {
      // Remove the token if expired
      localStorage.removeItem('token');
      router.push({ name: 'login' }); // Redirect to login
    }
    return Promise.reject(error);
  }
);

app.use(router);
app.use(Toast);
app.mount('#app');
