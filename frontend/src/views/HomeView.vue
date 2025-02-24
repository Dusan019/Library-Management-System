<template>
  <div class="home-view">
    <!-- Menu Bar -->
    <header>
      <nav>
        <ul>
          <li><router-link to="/books">Browse All Books</router-link></li>
          <li><router-link to="/loans">My Loans</router-link></li>
          <li><router-link to="/change-account-details">Change Account Details</router-link></li>
          <li v-if="isLibrarian"><router-link to="/manage-books">Manage Books</router-link></li>
          <li v-if="isLibrarian"><router-link to="/manage-users">All Members</router-link></li>
          <li v-if="isLibrarian"><router-link to="/loans-history">Loan History</router-link></li>
        </ul>
        <div class="user-greeting">
          <p>Hello, {{ username }} 
            <button @click="logout" class="logout-button">Logout</button>
          </p>
        </div>
      </nav>
    </header>

    <!-- Search Bar Section -->
    <section class="search-section">
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          @input="searchBooks" 
          placeholder="Search for a book..." 
          class="search-bar"
        />
      </div>

      <!-- Search Results Section -->
      <div v-if="searchedBooks.length > 0" class="search-results">
        <div v-for="book in searchedBooks" :key="book.id" class="book-card">
          <img :src="book.image_url" alt="Book Image" class="book-image"  />
          <div class="book-info">
            <h3>{{ book.title }}</h3>
            <p class="availability" :class="{ available: book.available, notAvailable: !book.available }">
              {{ book.available ? 'Available' : 'Not Available' }}
            </p>
          </div>
          <div class="action-btn">
            <button 
              v-if="book.available" 
              @click="loanBook(book)" 
              class="loan-button"
            >
              Borrow
            </button>
            <button 
              v-else 
              disabled 
              class="loan-button disabled"
            >
              Not Available
            </button>
          </div>
        </div>
      </div>

      <!-- No Results Section -->
      <div v-if="searchedBooks.length === 0 && searchQuery" class="no-results">
        <p>We are sorry, no search results were found for "{{ searchQuery }}".</p>
      </div>

    </section>

    <!-- Notification -->
    <div v-if="notification" class="notification">
      <p>{{ notification }}</p>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '', // Placeholder for logged-in user's name
      searchQuery: '',
      searchedBooks: [],
      notification: '', // Store notification message
      isLibrarian: false, // Determine if the user is a librarian
    };
  },
  created() {
    // Get the token and decode it manually to retrieve the username and role
    const token = localStorage.getItem('token');
    const name = localStorage.getItem('username');
    if (token) {
      const decodedToken = this.parseJwt(token);
      if (decodedToken) {
        this.username = name || 'Guest';
        this.isLibrarian = decodedToken.role === 'librarian'; // Check the role
      }
    }
  },
  methods: {
    // Manual JWT decoding
    parseJwt(token) {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        return JSON.parse(atob(base64));
      } catch (error) {
        console.error('Error decoding JWT:', error);
        return null;
      }
    },

    async searchBooks() {
      if (this.searchQuery.length > 0) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/books/search`, {
            params: { query: this.searchQuery }
          });
          this.searchedBooks = response.data.books;
        } catch (error) {
          console.error('Error fetching search results:', error);
        }
      } else {
        this.searchedBooks = [];
      }
    },

    async loanBook(book) {
      try {
        const response = await axios.post(`http://127.0.0.1:5000/loans/borrow`, {
          book_id: book.id,
          user_id: localStorage.getItem('userId'),
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });

        if (response.data.success) {
          this.notification = 'Book loaned successfully!';
          book.available = false;
        } else {
          this.notification = 'Failed to loan book.';
        }
      } catch (error) {
        console.error('Error loaning book:', error);
        this.notification = 'Error loaning book.';
      }
      setTimeout(() => { this.notification = ''; }, 3000);
    },

    logout() {
      localStorage.clear();
      this.$router.push('/login'); // Redirect to login page after logout
    }
  },
};
</script>

<style scoped>
.home-view {
  height: 100vh; 
  width: 100%; 
  padding: 0;
  background: url('images/home-background.jpg') no-repeat center center fixed;
  background-size: cover;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  overflow: auto;
  justify-content: flex-start; 
}


header {
  background-color: rgba(87, 59, 138, 0.9); 
  color: white;
  padding: 20px 0;
  margin-bottom: 30px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); 
}

nav {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  width: 100%;
  padding-right: 10px;
}

nav ul {
  display: flex;
  list-style-type: none;
  padding: 0;
  justify-content: center; 
  flex-grow: 1; 
}

nav ul li {
  margin-right: 10px;
  display: inline-block;
  text-align: center;
}

nav ul li a {
  color: white;
  text-decoration: none;
  font-size: 0.9em;
  text-transform: uppercase; 
  letter-spacing: 1px;
  transition: transform 0.3s; 
  display: block; 
  padding: 10px; 
}

nav ul li a:hover {
  transform: scale(1.1);
  background-color: rgba(87, 59, 138, 0.9);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); 
}

.user-greeting {
  display: flex;
  align-items: center;
}

.user-greeting p {
  margin: 0;
  font-size: 1.2em;
  font-weight: normal;
}

.logout-button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 15px;
  margin-left: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #d32f2f;
}

.search-section {
  text-align: center;
  padding: 20px;
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 600px;
  margin: 20px auto;
}

.search-bar {
  width: 100%;
  max-width: 700px;
  padding: 18px 25px;
  font-size: 1.2em;
  border: 2px solid #ddd;
  border-radius: 5px;
  margin: 20px 0;
  display: block;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); 
  transition: box-shadow 0.3s ease-in-out;
}

.search-bar:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 25px rgba(87, 59, 138, 0.9);
}
.search-results-table {
  width: 90%;
  margin: 20px auto;
}

.search-results-table table {
  width: 100%;
  border-collapse: collapse;
  background-color: rgba(87, 59, 138, 0.9);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.search-results-table th,
.search-results-table td {
  padding: 15px;
  font-size: 18px;
  text-align: center; 
  vertical-align: middle; 
  border-bottom: 1px solid #f0f0f0;
  font-weight: bold;
}
.search-results-table th {
  background: #f5f5f5;
  font-weight: bold;
  border-right-style: solid;
  width: 33%
}

.search-results-table tr:last-child td {
  border-bottom: none;
}

.available {
  color: green;
}


.notAvailable {
  color: red;
}
.book-image {
  width: 100%;          
  height: 20rem;        
  object-fit: cover;    
  border-radius: 8px;  
}

.book-info h3 {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}
.loan-button {
  padding: 10px 15px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-results {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 20px;
}
.book-card:hover {
  transform: translateY(-5px);
}

.book-card {
  background-color: rgba(87, 59, 138, 0.9);
  border-style: solid;
  border-width: 1px;
  border-radius: 10px;
  color:white;
  width: 250px;
  margin: 15px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  text-align: center;
}

.loan-button.disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.no-results {
  max-width: 700px;
  margin: 30px auto; 
  padding: 20px;
  border: 1px solid #f0f0f0;
  border-radius: 10px; 
  background-color: #f9f9f9; 
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
  text-align: center; 
  font-size: 1.2em;
  color: #555; 
  line-height: 1.5;
}

.no-results p {
  margin: 0;
  font-weight: bold; 
}

</style>