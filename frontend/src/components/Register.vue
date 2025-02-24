<template>
  <div class="container">
    <div class="main">
      <div class="register">
        <h2>Register</h2>
        <form @submit.prevent="register">
          <div>
            <input type="text" v-model="username" id="username" placeholder="Username" required />
          </div>
          <div>
            <input type="password" v-model="password" id="password" placeholder="Password" required />
          </div>
          <div>
            <input type="email" v-model="email" id="email" placeholder="Email" required />
          </div>
          <div>
            <input type="text" v-model="name" id="name" placeholder="Name" required />
          </div>
          <div>
            <input type="text" v-model="last_name" id="last_name" placeholder="Last Name" required />
          </div>
          <button type="submit">Register</button>
        </form>
        <div class="login-redirect">
          <p>Already have an account? <router-link to="/login">Login here</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import axios from 'axios';
import Toastify from 'toastify-js';
import 'toastify-js/src/toastify.css';

export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      name: '',
      last_name: '',
      errorMessage: '', 
    };
  },
  methods: {
    showToast(type, message) {
      Toastify({
        text: message,
        duration: 3000,  // Duration in ms (3 seconds)
        close: true,  // Show close button
        gravity: "top",  // Position at the top
        position: "center",  // Centered on the screen
        backgroundColor: type === 'success' ? "#4CAF50" : "#ff4d4d",  // Green for success, red for error
      }).showToast();
    },  
    async register() {
      this.errorMessage = ''; // Clear previous errors before sending a new request

      try {
        // Send registration data to the backend
        const response = await axios.post('http://127.0.0.1:5000/auth/register', {
          username: this.username,
          password: this.password,
          email: this.email,
          name: this.name,
          last_name: this.last_name,
          role: 'member', // Set default role as 'member'
        });
        this.showToast('success', response.data.message);

        this.$router.push('/login'); // Redirect to login page after successful registration
      } catch (error) {
        const errorMessage = error.response && error.response.data ? error.response.data.message : 'An unexpected error occurred. Please try again.';
        this.showToast('error', errorMessage);
        this.errorMessage = errorMessage;
      }
    },
  },
};
</script>

<style scoped>
.container {
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  font-family: "Jost", sans-serif;
  background: url('/images/register-background.jpg') no-repeat center/cover;
}

.main {
  width: 350px;
  height: auto; 
  background: rgba(255, 255, 255, 0.9); 
  border-radius: 10px;
  box-shadow: 5px 20px 50px #000;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 20px;
}

.register {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center; 
}

form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center; 
  width: 100%;
}

label {
  color: #573b8a;
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  width: 100%;
  height: 35px;
  font-size: 16px;
  background: #e0dede;
  margin: 10px 0;
  padding: 10px;
  border: none;
  outline: none;
  border-radius: 5px;
}

button {
  width: 60%;
  height: 40px;
  margin: 20px 0;
  color: #fff;
  background: #573b8a;
  font-size: 1em;
  font-weight: bold;
  outline: none;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #6d44b8;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.login-redirect {
  margin-top: 20px;
  text-align: center;
}

.login-redirect a {
  color: #573b8a;
  text-decoration: none;
}

.login-redirect a:hover {
  text-decoration: underline;
}
</style>
