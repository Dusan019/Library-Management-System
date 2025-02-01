<template>
  <div class="loans">
    <h1>Your Loans</h1>

    <!-- Display a list of loans -->
    <div class="table-container">
      <table v-if="loans.length > 0">
        <thead>
          <tr>
            <th>Book Title</th>
            <th>Loan Date</th>
            <th>Date Returned</th>
            <th>Return</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="loan in loans" :key="loan.id">
            <td>{{ loan.title }}</td>
            <td>{{ formatDate(loan.loan_date) }}</td>
            <td>{{ formatDate(loan.date_returned) || 'Not Returned Yet' }}</td>
            <td>
              <button 
              :class="{'returned': loan.date_returned}"
              v-if="!loan.date_returned"
                @click="askConfirmation(loan)"
              >
                Return Book
              </button>
              <!-- Display 'Returned' button with gray styling if the book is returned -->
              <button
                v-else
                class="returned"
                disabled
              >
                Returned
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No loans found.</p>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showConfirmation" class="confirmation-overlay">
      <div class="confirmation-modal">
        <p>Are you sure you want to return this book?</p>
        <div class="buttons">
        <button class="yes-btn" @click="returnBook()"><b>Yes,Return</b></button>
        <button class="no-btn" @click="cancelReturn"><b>Cancel</b></button>
      </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        @click="changePage(currentPage - 1)" 
        :disabled="currentPage === 1"
      >
        Previous
      </button>
      <span class="pagination-text">Page {{ currentPage }} of {{ totalPages }}</span>
      <button 
        @click="changePage(currentPage + 1)" 
        :disabled="currentPage === totalPages"
      >
        Next
      </button>
      
    </div>
  </div>
</template>

<script>
import Toastify from 'toastify-js';  

import "toastify-js/src/toastify.css";
import axios from 'axios';

export default {
  data() {
    return {
      loans: [],
      userId: localStorage.getItem('userId'),
      currentPage: 1,
      totalPages: 1,
      loansPerPage: 5,
      showConfirmation: false, 
      loanToReturn: null, 
    };
  },
  methods: {
    getLoans() {
      axios
        .get(`http://127.0.0.1:5000/loans/user/${this.userId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          params: {
            page: this.currentPage,
            limit: this.loansPerPage,
          },
        })
        .then((response) => {
          this.loans = response.data.loans.sort((a, b) => {
            if (!a.date_returned && b.date_returned) return -1;
            if (a.date_returned && !b.date_returned) return 1;
            return new Date(b.loan_date) - new Date(a.loan_date);
          });
          this.totalPages = response.data.totalPages;
        })
        .catch((error) => {
          console.error('Error fetching loans:', error);
        });
    },

    formatDate(date) {
      return date ? new Date(date).toLocaleDateString() : '';
    },

    askConfirmation(loan) {
      this.showConfirmation = true;
      this.loanToReturn = loan;
    },

    returnBook() {
      axios
        .put(
          `http://127.0.0.1:5000/loans/return/${this.loanToReturn.id}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        )
        .then((response) => {
          const updatedLoan = response.data;
          const loanIndex = this.loans.findIndex((l) => l.id === updatedLoan.id);
          if (loanIndex !== -1) {
            this.loans[loanIndex] = updatedLoan;
          }
          this.loans.sort((a, b) => {
            if (!a.date_returned && b.date_returned) return -1;
            if (a.date_returned && !b.date_returned) return 1;
            return new Date(b.loan_date) - new Date(a.loan_date);
          });

        
        Toastify({
          text: "Book returned successfully!",
          duration: 3000, 
          backgroundColor: "#4CAF50", 
          close: true,
          position: "center",
        }).showToast();
          this.cancelReturn(); 
        })
        .catch((error) => {
          console.error('Error returning book:', error);
          Toastify({
          text: this.errorMessage,
          duration: 3000, 
          close: true,
          gravity: "top", 
          position: "center", 
          backgroundColor: "#ff4d4d", 
          stopOnFocus: true, 
        }).showToast();
          this.cancelReturn(); 
        });
    },

    cancelReturn() {
      this.showConfirmation = false;
      this.loanToReturn = null;
    },

    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      this.getLoans();
    },
  },
  mounted() {
    this.getLoans();
  },
};
</script>

<style scoped>

.loans {
  background: url("/images/loans-background.jpg") no-repeat center/cover;
  max-width: 100%;
  max-height: 100vh;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 2rem;

}
.pagination-text{
  color: white;
  font-weight: bold;
  
}
h1{
  text-align: center;
  background-color: rgba(87, 59, 138, 0.8);
  padding: 2rem;
  font-size: 2rem;
  color:white;
  font-weight: bold;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}
.confirmation-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(5px); 
}

.confirmation-modal {
  background-color: white;
  padding: 20px;
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  width: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.confirmation-modal p {
  margin-bottom: 20px;
}

.confirmation-modal button {
  padding: 10px 20px;
  margin: 10px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  color: white;
}

.confirmation-modal .yes-btn {
  background-color: #28a745; 
}

.confirmation-modal .yes-btn:hover {
  background-color: #218838; 
}

.confirmation-modal .no-btn {
  background-color: #dc3545; 
}

.confirmation-modal .no-btn:hover {
  background-color: #c82333; 
}
td button.returned {
  background-color: #6c757d; 
  color: white;
  cursor: not-allowed;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
}


button {
  padding: 5px 10px;
  background-color: #28a745;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.pagination button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
}

.pagination span {
  margin: 0 20px;
}

.table-container {
  overflow-x: auto;
  background-color: rgba(87, 59, 138, 0.8); 
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 5px 10px; 
}

th, td {
  padding: 12px 0px;
  text-align: center;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 8px;
  transition: background-color 0.3s;
}

th {
  background-color: #007bff; 
  color: white;
  font-weight: bold;
}

td {
  background-color: rgba(255, 255, 255, 0.8); 
  color: #333;
}

td button {
  padding: 6px 12px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

td button:hover {
  background-color: #218838;
}

td button:disabled {
  background-color: #ccc; 
  cursor: not-allowed;
}

td button.returned {
  background-color: #6c757d; 
  cursor: not-allowed;
}
</style>