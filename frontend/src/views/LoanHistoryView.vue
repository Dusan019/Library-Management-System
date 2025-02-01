<template>
    <div class="loan-history">
      <h1>Loan History</h1>
  
      <Button 
      buttonText="Add New Loan" 
      color="blue" 
      @click="showAddModal = true" 
    />
      <table>
        <thead>
          <tr>
            <th>Book Title</th>
            <th>Member Id</th>
            <th>Loan Date</th>
            <th>Return Date</th>
            <th>Date Returned</th> <!-- Added column -->
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="loan in paginatedLoans" :key="loan.id">
            <td>{{ loan.title }}</td>
            <td>{{ loan.user_id }}</td>
            <td>{{ loan.loan_date }}</td>
            <td>{{ loan.return_date }}</td>
            <td>{{ loan.date_returned || 'Not Returned' }}</td> <!-- Display Date Returned -->
            <td>
              <button @click="editLoan(loan)">✏️</button>
              <button @click="confirmDelete(loan.id)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="previousPage">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="nextPage">Next</button>
      </div>
  
      <!-- Add Loan Modal -->
      <div v-if="showAddModal" class="modal">
        <div class="modal-content">
          <h2>Add New Loan</h2>
          <form @submit.prevent="addLoan">
            <label for="book_id">Book:</label>
            <select v-model="newLoan.book_id" id="book_id" @change="updateBookTitle">
            <option disabled value="">Select a Book</option>
            <option v-for="book in books" :key="book.id" :value="book.id">{{ book.title }}</option>
            </select>

            <label for="user_id">User:</label>
            <select v-model="newLoan.user_id" id="user_id" required>
            <option disabled value="">Select a User</option>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.name }}</option>
            </select>
            <label for="loan_date">Loan Date:</label>
            <input type="date" v-model="newLoan.loan_date" required />
  
            <label for="return_date">Return Date:</label>
            <input type="date" v-model="newLoan.return_date" required />
  
            <label for="date_returned">Date Returned:</label>
            <input type="date" v-model="newLoan.date_returned" />
  
            <button type="submit">Add Loan</button>
            <button @click="closeAddModal" type="button">Close</button>
          </form>
        </div>
      </div>
  
      <!-- Edit Loan Modal -->
      <div v-if="showEditModal" class="modal">
        <div class="modal-content">
          <h2>Edit Loan</h2>
          <form @submit.prevent="updateLoan">
            <div class="select">
            <label for="book_title">Book Title:</label>
            <select v-model="editForm.book_id" required>
              <option v-for="book in books" :key="book.id" :value="book.id">{{ book.title }}</option>
            </select>
  
            <label for="member_name">Member Name:</label>
            <select v-model="editForm.user_id" required>
              <option v-for="user in users" :key="user.id" :value="user.id">{{ user.name }}</option>
            </select>
          </div>
            <label for="loan_date">Loan Date:</label>
            <input type="date" v-model="editForm.loan_date" required />
  
            <label for="return_date">Return Date:</label>
            <input type="date" v-model="editForm.return_date" required />
  
            <label for="date_returned">Date Returned:</label>
            <input type="date" v-model="editForm.date_returned" />
  
            <button type="submit">Update Loan</button>
            <button @click="closeEditModal" type="button">Close</button>
          </form>
        </div>
      </div>
      <div v-if="showConfirmDeleteModal" class="modal">
      <div class="modal-content">
        <h2>Confirm Deletion</h2>
        <p>Are you sure you want to delete this loan?</p>
        <div class="modal-footer">
        <button @click="deleteLoan(loanToDelete)">Yes, Delete</button>
        <button @click="closeConfirmDeleteModal">Cancel</button>
      </div>
      </div>
    </div>
    <div v-if="showConfirmDeleteModal" class="modal">
      <div class="modal-content">
        <h2>Confirm Deletion</h2>
        <p>Are you sure you want to delete this loan?</p>
        <button @click="deleteLoan(loanToDelete)" class="yes-btn">Yes, Delete</button>
        <button @click="closeConfirmDeleteModal" class="no-btn">Cancel</button>
      </div>
    </div>
      
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
        loans: [],
        books: [],
        users: [],
        showAddModal: false,
        showEditModal: false,
        showConfirmDeleteModal: false, // New state for confirmation modal
      loanToDelete: null, 
        newLoan: {
          book_id: '',
          user_id: '',
          loan_date: '',
          return_date: '',
          date_returned: '', // Added date_returned field
        },
        successMessage: '',
        currentPage: 1,
        loansPerPage: 5,
        editForm: {},
      };
    },
    created() {
      this.fetchLoans();
      this.fetchUsers();
      this.fetchBooks();
    },
    computed: {
      totalPages() {
        return Math.ceil(this.loans.length / this.loansPerPage);
      },
      paginatedLoans() {
        const start = (this.currentPage - 1) * this.loansPerPage;
        const end = start + this.loansPerPage;
        return this.loans.slice(start, end);
      }
    },
    methods: {
      confirmDelete(loanId) {
      this.loanToDelete = loanId;
      this.showConfirmDeleteModal = true;
    },
    closeConfirmDeleteModal() {
      this.showConfirmDeleteModal = false;
      this.loanToDelete = null;
    },
      updateBookTitle() {
    const selectedBook = this.books.find(book => book.id === this.newLoan.book_id);
    this.newLoan.title = selectedBook ? selectedBook.title : '';
  },
      async addLoan() {
    try {
      console.log(this.newLoan); 
      if (!this.newLoan.book_id || !this.newLoan.user_id || !this.newLoan.loan_date || !this.newLoan.return_date) {
        this.showToast("error","All fields are required except 'Date Returned'.");
        return;
      }

      // Post the new loan to the backend
      const response = await axios.post('http://127.0.0.1:5000/loans/add', this.newLoan);

      if (response.data.message === 'Loan added successfully') {
        // Add the new loan to the loans list
        this.loans.push({
          ...response.data.loan,
          title: this.books.find(book => book.id === this.newLoan.book_id)?.title || '',
        });

        this.showToast("success","Loan added successfully!");
        this.closeAddModal();

        // Reset the newLoan form
        this.newLoan = {
          book_id: '',
          user_id: '',
          loan_date: '',
          return_date: '',
          date_returned: '',
          title: ''
        };

        setTimeout(() => (this.successMessage = ''), 3000);
      }
    } catch (error) {
      console.error('Error adding loan:', error);
    }
  },

      async fetchLoans() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/loans');
          this.loans = response.data;
          console.log('Fetched loans:', this.loans);
        } catch (error) {
          console.error('Error fetching loans:', error);
        }
      },
  
      async fetchUsers() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/users');
          this.users = response.data;
          console.log('Fetched users:', this.users);
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      },
  
      async fetchBooks() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/books');
          this.books = response.data;
          console.log('Fetched books:', this.books);
        } catch (error) {
          console.error('Error fetching books:', error);
        }
      },
  
      editLoan(loan) {
  console.log('Editing loan:', loan);
  this.editForm = { ...loan };

  // Set the loan title based on the selected book
  const selectedBook = this.books.find(book => book.id === loan.book_id);
  this.editForm.book_id = loan.book_id;
  this.editForm.title = selectedBook ? selectedBook.title : '';
  const selectedUser = this.users.find(user => user.id === loan.user_id);
  this.editForm.user_id = loan.user_id;
  this.editForm.user_name = selectedUser ? selectedUser.name : '';

  this.showEditModal = true; // Display modal after ensuring `editForm` is fully updated
},


      closeAddModal() {
        this.showAddModal = false;
      },
  
      closeEditModal() {
        this.showEditModal = false;
      },
      async updateLoan() {
  try {
    const updatedLoan = {
      book_id: this.editForm.book_id,
      user_id: this.editForm.user_id,
      loan_date: this.editForm.loan_date,
      return_date: this.editForm.return_date,
      date_returned: this.editForm.date_returned || null,
      title: this.editForm.title 
    };

    const response = await axios.put(`http://127.0.0.1:5000/loans/${this.editForm.id}`, updatedLoan);

    if (response.data.message === 'Loan updated successfully') {
      const index = this.loans.findIndex(loan => loan.id === this.editForm.id);
      if (index !== -1) {
        const updatedBook = this.books.find(book => book.id === this.editForm.book_id);
        this.loans[index] = {
          ...this.editForm,
          title: updatedBook ? updatedBook.title : this.editForm.title,
        };
      }

      this.showToast("success",'Loan updated successfully!');
      this.closeEditModal();
      setTimeout(() => (this.successMessage = ''), 3000);
    }
  } catch (error) {
    console.error('Error updating loan:', error);
  }
},


async updateBookAvailability(bookId) {
  try {
    const response = await axios.put(`http://127.0.0.1:5000/books/${bookId}/update-availability`, { available: true });
    console.log('Update book availability response:', response);
  } catch (error) {
    console.error('Error updating book availability:', error);
  }
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

  
      async deleteLoan(loanId) {
        try {
          const response = await axios.delete(`http://127.0.0.1:5000/loans/${loanId}`);
          console.log('Delete loan response:', response);
  
          if (response.data.message === 'Loan deleted successfully') {
            this.loans = this.loans.filter(loan => loan.id !== loanId);
            this.showToast("success","Loan deleted successfully!");
            this.closeConfirmDeleteModal();
            setTimeout(() => {
              this.successMessage = '';
            }, 3000);
          }
        } catch (error) {
          console.error('Error deleting loan:', error);
        }
      },
  
      previousPage() {
        if (this.currentPage > 1) {
          this.currentPage--;
        }
      },
  
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.currentPage++;
        }
      }
    }
  };
  </script>
  <style scoped>
  .select{
    display:flex;
    flex-wrap: wrap;
    flex-direction: column;
  }
  .loan-history {
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
background-color: #007bff;
color: white;
font-weight: bold;
text-transform: uppercase;
}

td {
background-color: #f9f9f9;
color: #333;
}
  .modal {
    text-align: center;
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
  .modal-content .yes-btn {
  background-color: #28a745; 
}

.modal-content .yes-btn:hover {
  background-color: #218838; 
}

.modal-content .no-btn {
  background-color: #dc3545; 
}

.modal-content .no-btn:hover {
  background-color: #c82333; 
}

.modal-content button {
  width: auto; 
  padding: 10px 20px; 
  cursor: pointer;
}
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 400px;
  }
  
  input {
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
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
  
  .pagination button {
    padding: 10px;
    background-color: #007bff;
    color: white;
    border-radius: 4px;
  }
  
  .pagination button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  