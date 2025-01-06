<template>
  <div class="container">
  <div class="main">
    <input type="checkbox" id="chk" />
    <div class="signup">
      <form @submit.prevent="login">
        <label for="chk">Login</label>
        <input
          type="text"
          v-model="username"
          id="username"
          placeholder="Username"
          required
        />
        <input
          type="password"
          v-model="password"
          id="password"
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
        <div class="register-redirect">
          <p>
            Don't have an account?
            <router-link to="/register">Register here</router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</div>
</template>


<script>
import axios from 'axios';
import Toastify from 'toastify-js';  // Import Toastify

import "toastify-js/src/toastify.css";  // Import Toastify styles

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '', // To store any error messages from the backend
    };
  },
  methods: {
    async login() {
      this.errorMessage = ''; // Clear previous errors before sending a new request

      try {
        // Send login credentials to the backend
        const response = await axios.post('http://127.0.0.1:5000/auth/login', {
          username: this.username,
          password: this.password,
        });

        // Handle success (store token in localStorage or redirect)
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('username', response.data.username);
        localStorage.setItem('userId',response.data.user_id);
        console.log(response.data.token); // Store JWT token
        this.$router.push('/home'); // Redirect to the dashboard or protected route
      } catch (error) {
        // Handle error (invalid credentials or server error)
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = 'An unexpected error occurred. Please try again.';
        }
          // Show error message using Toastify
          Toastify({
          text: this.errorMessage,
          duration: 3000, // Toast duration in ms
          close: true,
          gravity: "top", // Position of the toast (top/bottom)
          position: "center", // Position on screen (left, center, right)
          backgroundColor: "#ff4d4d", // Red background for errors
          stopOnFocus: true, // Stop animation when the toast is focused
        }).showToast();
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
  background: url('/images/login-background.jpg') no-repeat center/cover;
   /* Use this if the image is stored in src/assets/images */
  /* If stored in public/images, use: background: url('/images/login-background.jpg') no-repeat center/cover; */
}

.main {
  width: 350px;
  height: 500px;
  background: rgba(255, 255, 255, 0.9); /* Add slight transparency to make the form stand out */
  border-radius: 10px;
  box-shadow: 5px 20px 50px #000;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 20px;
}

#chk {
  display: none;
}

.signup,
.login {
  position: relative;
  width: 100%;
  height: 100%;
}

label {
  color: #573b8a;
  font-size: 2.3em;
  justify-content: center;
  display: flex;
  margin: 60px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.5s ease-in-out;
}

input {
  width: 70%; /* Increase width */
  height: 35px;
  font-size: 16px; 
  background: #e0dede;
  justify-content: center;
  display: flex;
  margin: 20px auto;
  padding: 10px;
  border: none;
  outline: none;
  border-radius: 5px;
}

button {
  width: 60%;
  height: 40px;
  margin: 10px auto;
  justify-content: center;
  display: block;
  color: #fff;
  background: #573b8a;
  font-size: 1em;
  font-weight: bold;
  margin-top: 20px;
  outline: none;
  border: none;
  border-radius: 5px;
  transition: 0.2s ease-in;
  cursor: pointer;
}

button:hover {
  background: #6d44b8;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.register-redirect {
  margin-top: 20px;
  text-align: center;
}

.register-redirect a {
  color: #573b8a;
  text-decoration: none;
}

.register-redirect a:hover {
  text-decoration: underline;
}

.login {
  height: 460px;
  background: #eee;
  border-radius: 60% / 10%;
  transform: translateY(-180px);
  transition: 0.8s ease-in-out;
}

.login label {
  color: #573b8a;
  transform: scale(0.6);
}

#chk:checked ~ .login {
  transform: translateY(-500px);
}

#chk:checked ~ .login label {
  transform: scale(1);
}

#chk:checked ~ .signup label {
  transform: scale(0.6);
}
</style>
