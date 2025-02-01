<template>
  <div class="update-user">
    <h1>Update Your Information</h1>
    <!-- Flex container for both forms -->
    <div class="form-container">
      <!-- Form to update user information -->
      <form @submit.prevent="openUpdateConfirmation" class="form-left">
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

        <button type="submit">Update Information</button>
      </div>
      </form>

      <!-- Form to change password -->
      <form @submit.prevent="openPasswordChangeConfirmation" class="form-right">
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
    <!-- Confirmation Modals -->
    <!-- Update Info Modal -->
    <div v-if="showUpdateModal" class="modal">
      <div class="modal-content">
        <h3>Are you sure you want to change your information?</h3>
        <div class="modal-footer">
          <button @click="updateUserInfo" class="yes-btn">Yes,Change</button>
          <button @click="closeUpdateModal" class="no-btn">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Confirmation modal for password change -->
    <div v-if="showPasswordModal" class="modal">
      <div class="modal-content">
        <h3>Are you sure you want to change your password?</h3>
        
        <div class="modal-footer">
          <button @click="changePassword" class="yes-btn">Yes,Change</button>
          <button @click="closePasswordModal" class="no-btn">Cancel</button>
        </div>
      </div>
    </div>


    <p v-if="message">{{ message }}</p>
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
      email: '',
      name: '',
      last_name: '',
      newPassword: '',
      confirmPassword: '',
      currentPassword: '',
      message: '',
      userId: localStorage.getItem('userId'), 
      showUpdateModal: false, // for showing the update confirmation modal
      showPasswordModal: false,
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
          this.showToast("error","Error fetching user data!");
        });
    },
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
    openUpdateConfirmation() {
      this.showUpdateModal = true; // Show the confirmation modal
    },

    closeUpdateModal() {
      this.showUpdateModal = false; // Close the confirmation modal
    },

    openPasswordChangeConfirmation() {
      this.showPasswordModal = true; // Show the confirmation modal
    },

    closePasswordModal() {
      this.showPasswordModal = false; // Close the confirmation modal
    },

    updateUserInfo() {
      if (this.newPassword && this.newPassword !== this.confirmPassword) {
        this.showToast("error","Passwords do not match!");
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
          this.showToast("success",response.data.message);
        this.closeUpdateModal();
        })
        .catch((error) => {
          this.showToast("error","Error updating user information!");
        });
    },

    changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.showToast("error",'Passwords do not match!');
        return;
      }

      if (!this.currentPassword) {
        this.showToast("error",'Current password is required!');
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
          this.showToast("success",response.data.message);
        this.closePasswordModal();
        })
        .catch((error) => {
          this.showToast("error","Error changing password!");
        });
    },
  },
  mounted() {
    this.fetchUserData();
  },
};
</script>

<style scoped>
.modal-footer {
  display: flex;
  justify-content: space-evenly; 
  gap: 10px; 
}
.modal-footer .yes-btn {
  background-color: #28a745; 
}

.modal-footer .yes-btn:hover {
  background-color: #218838; }

.modal-footer .no-btn {
  background-color: #dc3545; 
}

.modal-footer .no-btn:hover {
  background-color: #c82333; 
}

.modal-footer button {
  width: auto; 
  padding: 10px 20px; 
  cursor: pointer;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}

.modal-content button {
  margin: 10px;
}
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
  background: rgba(255, 255, 255, 0.9); 
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
  width: 81%; 
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
