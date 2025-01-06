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
            <button @click="deleteMember(member.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
  <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
  <span>Page {{ currentPage }}</span>
  <button @click="nextPage" :disabled="currentPage * membersPerPage >= members.length">Next</button>
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
export default {
  components: {
    Button, // Register the Button component
  },
  data() {
    return {
      members: [], // Store list of members
      showAddModal: false, // Control visibility of add modal
      showEditModal: false, // Control visibility of edit modal
      newMember: {
        username: '',
        email: '',
        name: '',
        last_name: '',
        role: 'member',
        password: '', // Add the password field here
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
    membersPerPage: 5,  // Add success message variable
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
    // Fetch all members from the backend (GET /users)
    async fetchMembers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/users');
        this.members = response.data;
        this.resetPage();
        console.log('Fetched members:', this.members); // Debug log
      } catch (error) {
        console.error('Error fetching members:', error);
      }
    },
    

    // Open the edit modal and populate the form with the member's details
    editMember(member) {
      console.log('Editing member:', member); // Debug log
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
        console.log('Add member response:', response); // Debug log
        
        // If the member was added successfully
        if (response.data.message === 'User added successfully') {
          this.members.push(response.data.user); // Add the new member to the list
          this.successMessage = 'Member added successfully!';  // Set success message
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

    // Update the member information (PUT /users/:id/update)
    async updateMember() {
      try {
        console.log('Updating member:', this.editForm); // Debug log
        const response = await axios.put(`http://127.0.0.1:5000/users/${this.editForm.id}/update`, this.editForm);
        console.log('Update member response:', response); // Debug log
        if (response.data.message === 'User updated successfully') {
          this.fetchMembers(); // Reload members after successful update
          this.closeEditModal(); // Close the modal
        }
      } catch (error) {
        console.error('Error updating member:', error);
      }
    },

    // Delete a member (DELETE /users/:id/delete)
    async deleteMember(memberId) {
  try {
    const response = await axios.delete(`http://127.0.0.1:5000/users/${memberId}/delete`);
    console.log('Delete member response:', response.data); // Debug log

    if (response.data.message === 'User and related loans deleted successfully') {
      // Reload the members list after successful deletion
      await this.fetchMembers();
    } else {
      // If deletion is not allowed, handle it appropriately
      alert(response.data.message || 'User cannot be deleted.');
      
      // Manually reload members or reset the state
      await this.fetchMembers(); // Ensures the members list is always refreshed after any deletion attempt
    }
  } catch (error) {
    console.error('Error deleting member:', error);
    alert('An error occurred while deleting the user.');

    // Manually reload members on error
    await this.fetchMembers(); // Ensure the members list is updated even on error
  }
}


  },
};
</script>

<style scoped>
/* Styles go here */
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
  background-color: #0056b3;
}

button:focus {
  outline: none;
}

table { 
  width: 100%;
  border-collapse: separate;
  border-spacing: 10px 10px;
  text-align: center;
  background-color:rgba(167, 199, 231, 0.7);
  border-radius: 10px; /* Add gap between rows */

}


th, td {

padding: 12px;
text-align: center;
border-radius: 10px;
border-bottom: 1px solid #ddd;
}

th {
background-color: #28a745;
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
