<template>
  <div class="update-user">
    <h1>Update Your Information</h1>
    <!-- Flex container for both forms -->
    <div class="form-container">
      <!-- Form to update user information -->
      <form @submit.prevent="updateUserInfo" class="form-left">
        <div class="center">
        <div>
          <label for="username">Username:</label>
          <input type="text" v-model="username" id="username" required placeholder="Username"/>
        </div>

        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="email" id="email" required placeholder="Email" />
        </div>

        <div>
          <label for="name">Name:</label>
          <input type="text" v-model="name" id="name" required placeholder="Name" />
        </div>

        <div>
          <label for="last_name">Last Name:</label>
          <input type="text" v-model="last_name" id="last_name" required placeholder="Last Name"/>
        </div>

        <button type="submit">Update Info</button>
      </div>
      </form>

      <!-- Form to change password -->
      <form @submit.prevent="changePassword" class="form-right">
        <div class="center">
        <div>
          <label for="current_password">Current Password:</label>
          <input type="password" v-model="currentPassword" id="current_password" required placeholder="Current password"/>
        </div>

        <div>
          <label for="new_password">New Password:</label>
          <input type="password" v-model="newPassword" id="new_password" required placeholder="New password"/>
        </div>

        <div>
          <label for="confirm_password">Confirm Password:</label>
          <input type="password" v-model="confirmPassword" id="confirm_password" required placeholder="Confirm new password"/>
        </div>

        <button type="submit">Change Password</button>
        </div>
      </form>
    </div>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import Toastify from 'toastify-js';
import 'toastify-js/src/toastify.css'; // Import CSS for Toastify

export default {
  data() {
    return {
      username: '', 
      email: '',
      name: '',
      last_name: '',
      newPassword: '',
      confirmPassword: '',
      currentPassword: '',
      message: '',
      userId: localStorage.getItem('userId'), 
    };
  },
  methods: {
    fetchUserData() {
      axios
        .get(`http://127.0.0.1:5000/users/${this.userId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .then((response) => {
          this.username = response.data.username;
          this.email = response.data.email;
          this.name = response.data.name;
          this.last_name = response.data.last_name;
        })
        .catch((error) => {
          console.error('Error fetching user data:', error);
          Toastify({
          text: "Error fetching the user data!",
          duration: 3000, // Toast duration in ms
          close: true,
          gravity: "top", // Position of the toast (top/bottom)
          position: "center", // Position on screen (left, center, right)
          backgroundColor: "#ff4d4d", // Red background for errors
          stopOnFocus: true, // Stop animation when the toast is focused
        }).showToast();
        });
    },

    updateUserInfo() {
      if (this.newPassword && this.newPassword !== this.confirmPassword) {
        Toastify({
          text: this.message,
          duration: 3000, // Toast duration in ms
          close: true,
          gravity: "top", // Position of the toast (top/bottom)
          position: "center", // Position on screen (left, center, right)
          backgroundColor: "#ff4d4d", // Red background for errors
          stopOnFocus: true, // Stop animation when the toast is focused
        }).showToast();
        return;
      }

      const data = {
        username: this.username,
        email: this.email,
        name: this.name,
        last_name: this.last_name,
      };

      axios
        .put(`http://127.0.0.1:5000/users/${this.userId}/update`, data, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .then((response) => {
          Toastify({
          text: response.data.message,
          duration: 3000, // 3 seconds
          backgroundColor: "#4CAF50", // Green color for success
          close: true,
          position: "center",
        }).showToast();
        })
        .catch((error) => {
          Toastify({
          text: this.message,
          duration: 3000, // Toast duration in ms
          close: true,
          gravity: "top", // Position of the toast (top/bottom)
          position: "center", // Position on screen (left, center, right)
          backgroundColor: "#ff4d4d", // Red background for errors
          stopOnFocus: true, // Stop animation when the toast is focused
        }).showToast();
        });
    },

    changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.message = 'Passwords do not match!';
        Toastify({
          text: this.errorMessage,
          duration: 3000, // Toast duration in ms
          close: true,
          gravity: "top", // Position of the toast (top/bottom)
          position: "center", // Position on screen (left, center, right)
          backgroundColor: "#ff4d4d", // Red background for errors
          stopOnFocus: true, // Stop animation when the toast is focused
        }).showToast();
        return;
      }

      if (!this.currentPassword) {
        this.message = 'Current password is required!';
        Toastify({
          text: this.errorMessage,
          duration: 3000, // Toast duration in ms
          close: true,
          gravity: "top", // Position of the toast (top/bottom)
          position: "center", // Position on screen (left, center, right)
          backgroundColor: "#ff4d4d", // Red background for errors
          stopOnFocus: true, // Stop animation when the toast is focused
        }).showToast();
        return;
      }

      const data = {
        current_password: this.currentPassword,
        new_password: this.newPassword,
      };

      axios
        .put(`http://127.0.0.1:5000/users/${this.userId}/change-password`, data, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .then((response) => {
          Toastify({
          text: response.data.message,
          duration: 3000, // 3 seconds
          backgroundColor: "#4CAF50", // Green color for success
          close: true,
          position: "center",
        }).showToast();
        })
        .catch((error) => {
          Toastify({
          text: this.errorMessage,
          duration: 3000, // Toast duration in ms
          close: true,
          gravity: "top", // Position of the toast (top/bottom)
          position: "center", // Position on screen (left, center, right)
          backgroundColor: "#ff4d4d", // Red background for errors
          stopOnFocus: true, // Stop animation when the toast is focused
        }).showToast();
        });
    },
  },
  mounted() {
    this.fetchUserData();
  },
};
</script>

<style scoped>
.update-user {
  padding: 20px;
  max-height: 80vh;
  overflow-y: auto;
  max-width: 100%;
  max-height: 100%;
  width:100%;
  height: 100%;
  background-image: url("images/login-background.jpg");
}
h1{
  color:white;
  text-align: center;
}
.form-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding-top: 3rem;
}

form {
  width: 30%;
  background: rgba(255, 255, 255, 0.9); /* Add slight transparency to make the form stand out */
  border-radius: 10px;
  box-shadow: 5px 20px 50px #000;
  margin-right: 1rem;
  padding: 2rem;
  display: flex;
  justify-content: right;
  border-radius: 10px;
}
.form-right{
  padding-top:3.7rem;
  padding-right: 3.5rem;
}
.form-left{
  padding-right: 3.5rem;
}
form div {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 81%; /* Decrease width of inputs */
  height: 35px;
  font-size: 16px;
  background: #e0dede;
  justify-content: center;
  display: flex;
  margin: 5px;
  padding: 10px;
  border: none;
  outline: none;
  border-radius: 5px;
}

button {
  width: 60%;
  height: 40px;
  justify-content: center;
  display: block;
  color: #fff;
  background: #573b8a;
  font-size: 1em;
  font-weight: bold;
  margin-top: 20px;
  margin-left: 1.9rem;
  outline: none;
  border: none;
  border-radius: 5px;
  transition: 0.2s ease-in;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}

p {
  color: red;
}
</style>
