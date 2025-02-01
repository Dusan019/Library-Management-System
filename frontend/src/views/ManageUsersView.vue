<template>
  <div class="manage-members">
    <h1>Manage Members</h1>
    
    <!-- Button to open modal for adding new member -->
    <Button 
      buttonText="Add New Member" 
      color="blue" 
      @click="showAddModal = true" 
    />
    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Name</th>
          <th>Role</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="member in paginatedMembers" :key="member.id">
          <td>{{ member.username }}</td>
          <td>{{ member.email }}</td>
          <td>{{ member.name }} {{ member.last_name }}</td>
          <td>{{ member.role }}</td>
          <td>
            <button @click="editMember(member)">✏️</button>
            <button @click="showDeleteConfirmation(member)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
  <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
  <span>Page {{ currentPage }}</span>
  <button @click="nextPage" :disabled="currentPage * membersPerPage >= members.length">Next</button>
  <div v-if="showDeleteModal" class="modal">
      <div class="modal-content">
        <h3>Are you sure you want to delete this member?</h3>
        <div class="modal-footer">
        <button @click="deleteMember(selectedMember.id)" class="yes-btn">Yes,Delete</button>
        <button @click="closeDeleteModal" class="no-btn">Cancel</button>
      </div>
      </div>
    </div>
</div>

    <!-- Modal for adding new member -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h2>Add New Member</h2>
        <form @submit.prevent="addMember">
          <label for="username">Username:</label>
          <input type="text" v-model="newMember.username" required />
          
          <label for="email">Email:</label>
          <input type="email" v-model="newMember.email" required />

          <label for="name">Name:</label>
          <input type="text" v-model="newMember.name" required />

          <label for="last_name">Last Name:</label>
          <input type="text" v-model="newMember.last_name" required />

          <label for="role">Role:</label>
          <select v-model="newMember.role" required>
            <option value="member">Member</option>
            <option value="librarian">Librarian</option>
          </select>

          <!-- New Password Field -->
          <label for="password">Password:</label>
          <input type="password" v-model="newMember.password" required />

          <button type="submit">Add Member</button>
          <button @click="closeAddModal" type="button">Close</button>
        </form>
      </div>
    </div>

    <!-- Modal for editing member -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h2>Edit Member</h2>
        <form @submit.prevent="updateMember">
          <label for="username">Username:</label>
          <input type="text" v-model="editForm.username" required />
          
          <label for="email">Email:</label>
          <input type="email" v-model="editForm.email" required />

          <label for="name">Name:</label>
          <input type="text" v-model="editForm.name" required />

          <label for="last_name">Last Name:</label>
          <input type="text" v-model="editForm.last_name" required />

          <label for="role">Role:</label>
          <select v-model="editForm.role" required>
            <option value="member">Member</option>
            <option value="librarian">Librarian</option>
          </select>

          <button type="submit">Update</button>
          <button @click="closeEditModal" type="button">Close</button>
        </form>
      </div>
    </div>

    <!-- Success message -->
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import Button from '@/components/Button.vue';
import Toastify from 'toastify-js';
import 'toastify-js/src/toastify.css'; 

export default {
  components: {
    Button, // Register the Button component
  },
  data() {
    return {
      members: [], 
      showAddModal: false, 
      showEditModal: false,
      showDeleteModal: false, 
      selectedMember: null, 
      newMember: {
        username: '',
        email: '',
        name: '',
        last_name: '',
        role: 'member',
        password: '', 
      },
      editForm: {
        id: null,
        username: '',
        email: '',
        name: '',
        last_name: '',
        role: 'member',
      },
      successMessage: '',
      currentPage: 1, // Current page number
    membersPerPage: 5,  
    };
    
  },
  computed: {
  paginatedMembers() {
    const startIndex = (this.currentPage - 1) * this.membersPerPage;
    const endIndex = startIndex + this.membersPerPage;
    return this.members.slice(startIndex, endIndex);
  },
},
  
  created() {
    this.fetchMembers(); // Fetch members when the page loads
  },
  methods: {
    closeDeleteModal() {
      this.showDeleteModal = false;
    },
    showDeleteConfirmation(member) {
      this.selectedMember = member;
      this.showDeleteModal = true;
    },
    // Fetch all members from the backend (GET /users)
    async fetchMembers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/users');
        this.members = response.data;
        this.resetPage();
        console.log('Fetched members:', this.members); 
      } catch (error) {
        console.error('Error fetching members:', error);
      }
    },
    

    // Open the edit modal and populate the form with the member's details
    editMember(member) {
      console.log('Editing member:', member); 
      this.editForm = { ...member }; // Copy the member's details into the form
      this.showEditModal = true; // Show the edit modal
    },

    // Close the edit modal
    closeEditModal() {
      this.showEditModal = false;
    },

    // Open the add modal
    closeAddModal() {
      this.showAddModal = false;
    },
        nextPage() {
    if (this.currentPage * this.membersPerPage < this.members.length) {
      this.currentPage++;
    }
  },
  
  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  },

  // Reset to first page when books are added/updated
  resetPage() {
    this.currentPage = 1;
  },

    // Add a new member (POST /users/add)
    async addMember() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/users/add', this.newMember);
        console.log('Add member response:', response); 
        
        // If the member was added successfully
        if (response.data.message === 'User added successfully') {
          this.members.push(response.data.user); // Add the new member to the list
          this.showToast("success",'Member added successfully!');
    
          this.closeAddModal(); // Close the modal
          
          // Reset the form after adding the new member
          this.newMember = { 
            username: '', 
            email: '', 
            name: '', 
            last_name: '', 
            role: 'member', 
            password: '' 
          };

          // Clear the success message after a few seconds
          setTimeout(() => {
            this.successMessage = '';
          }, 3000);
        }
      } catch (error) {
        console.error('Error adding member:', error);
      }
    },
    showToast(type, message) {
      Toastify({
        text: message,
        duration: 3000,  // Duration in ms (3 seconds)
        close: true,  // Show close button
        gravity: "top",  // Position at the top
        position: "center",  // Centered on the screen
        backgroundColor: type === 'success' ? "#4CAF50" : "#ff4d4d",  
      }).showToast();
    },  
    async updateMember() {
      try {
        console.log('Updating member:', this.editForm); 
        const response = await axios.put(`http://127.0.0.1:5000/users/${this.editForm.id}/update`, this.editForm);
        console.log('Update member response:', response); 
        if (response.data.message === 'User updated successfully') {
          this.fetchMembers(); 
          this.closeEditModal(); 
        }
      } catch (error) {
        console.error('Error updating member:', error);
      }
    },
    async deleteMember(memberId) {
  try {
    const response = await axios.delete(`http://127.0.0.1:5000/users/${memberId}/delete`);
    console.log('Delete member response:', response.data);
    if (response.data.message === 'User and related loans deleted successfully') {
      
      this.showToast("success","User and related loans deleted succesfully");
  
      await this.fetchMembers();
    } else {

      if(response.data.message){
        this.showToast("success",response.data.message);
      }
      else
      {
        this.showToast("error","User not cannot be deleted!");
     
      }
      // Manually reload members or reset the state
      await this.fetchMembers(); // Ensures the members list is always refreshed after any deletion attempt
    }
    this.closeDeleteModal();
  } catch (error) {
    console.error('Error deleting member:', error);
    this.showToast("error","An error occurred while deleting the user.");


    // Manually reload members on error
    await this.fetchMembers();
    this.closeDeleteModal(); 
  }
}


  },
};
</script>

<style scoped>

.modal-footer{
  display: flex;
  justify-content: space-evenly; 
  gap: 10px;
}
.modal-footer button {
  width: auto; 
  padding: 10px 20px; 
  cursor: pointer;
}
.modal-footer .yes-btn {
  background-color: #28a745; 
}

.modal-footer .yes-btn:hover {
  background-color: #218838; 
}

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
.manage-members {
  margin: 0px;
  max-width: 100%;
  max-height: 100%;
  height: 100%;
  width:100%;
  padding: 2rem;
  background-color: #007bff;
  font-family: 'Arial', sans-serif;
  background: url('/images/register-background.jpg');
}
h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color:white;
  text-align: center;
  margin-bottom: 20px;
}

button {
  padding: 5px 10px;
  margin-right: 5px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
}

button:hover {
  background-color: #007bff;;
}

button:focus {
  outline: none;
}

table { 
  width: 100%;
  border-collapse: separate;
  border-spacing: 10px 10px;
  text-align: center;
  background-color: rgba(87, 59, 138, 0.8);
  border-radius: 10px; 
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}


th, td {

padding: 12px;
text-align: center;
border-radius: 10px;
border-bottom: 1px solid #ddd;
}

th {
background-color:  #007bff;;
color: white;
font-weight: bold;
text-transform: uppercase;
}

td {
background-color: #f9f9f9;
color: #333;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}

input, select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  background-color: #28a745;
}

button[type="submit"]:hover {
  background-color: #218838;
}

button[type="button"] {
  background-color: #dc3545;
}

button[type="button"]:hover {
  background-color: #c82333;
}

.success-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}
</style>
