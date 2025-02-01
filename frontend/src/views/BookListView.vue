<template>
  <div class="browse-books">
    <h2>Browse All Books</h2>

    <div class="book-list">
      <div v-for="book in books" :key="book.id" class="book-item">
        <img :src="book.image_url" alt="Book Image" class="book-image" />
        <div class="book-info">
          <h3>{{ book.title }}</h3>
          <p>{{ book.author }}</p>
          <p>Quantity: {{ book.quantity }}</p>
          <p v-if="book.available && book.quantity > 0">
            <button @click="openConfirmationModal(book.id)" class="borrow-btn">
              Borrow
            </button>
          </p>
          <p v-else>Not Available</p>
        </div>
      </div>
    </div>

    <p v-if="books.length === 0">No books available</p>


    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>Are you sure you want to borrow this book?</h3>
        <button @click="confirmBorrow" class="confirm-btn">Yes, Borrow</button>
        <button @click="closeModal" class="cancel-btn">Cancel</button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import Toastify from 'toastify-js';
export default {
  data() {
    return {
      books: [],  // Array to hold the books fetched from the backend
      userId: null,
      showModal: false,  // State to control the modal visibility
      bookToBorrow: null,  
    };
  },
  created() {
    this.fetchBooks();
    this.userId = localStorage.getItem('userId') || null;  // Fetch user ID from localStorage or state
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/books');
        this.books = response.data;  // Assign the books to the array
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    openConfirmationModal(bookId) {
      this.bookToBorrow = bookId;  // Set the book to borrow
      this.showModal = true;  // Show the modal
    },
    closeModal() {
      this.showModal = false;  // Hide the modal
      this.bookToBorrow = null;  // Reset book to borrow
    },
    async confirmBorrow() {
      try {
        const returnDate = this.calculateReturnDate();  // Calculate the return date
        const response = await axios.post('http://127.0.0.1:5000/loans/borrow', {
          user_id: this.userId,
          book_id: this.bookToBorrow,
          return_date: returnDate,
        });

        if (response.data.success) {
          this.showToast('success', response.data.message);  // Show success message
          this.fetchBooks();  // Refresh the book list
        } else {
          this.showToast('error', response.data.message);   // Display failure message
        }

        this.closeModal();  // Close the modal after confirming
      } catch (error) {
        console.error('Error borrowing book:', error);
        this.showToast('error', 'Failed to borrow book. Please try again.');
        this.closeModal();  // Close the modal after error
      }
    },
    calculateReturnDate() {
      // Calculate return date (e.g., 14 days from today)
      const today = new Date();
      today.setDate(today.getDate() + 14);  // Set return date to 14 days later
      return today.toISOString().split('T')[0];  // Return the date in YYYY-MM-DD format
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
    },  //
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);  
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;  /* Ensure modal is on top */
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.confirm-btn, .cancel-btn {
  padding: 10px 20px;
  margin: 10px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
}

.confirm-btn {
  background-color: #4CAF50;
  color: white;
}

.confirm-btn:hover {
  background-color: #45a049;
}

.cancel-btn {
  background-color: #f44336;
  color: white;
}

.cancel-btn:hover {
  background-color: #e53935;
}
.browse-books {
  width: 100%;  
  padding: 0px; 
  overflow-x: auto;
  background-image: url('images/booklist-background.jpg'); 
  background-size: cover; 
  background-position: center;   
}
.book-list {

  padding: 50px;
  display: flex;
  flex-wrap: wrap;  
  justify-content: space-between;  
  gap: 6px;
  max-width: 100%;
  }

.book-item {
  width: 270px;
  display: flex;
  margin: 0px;
  margin-bottom: 2rem;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 8px;
  color:white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); 
  background-color: rgba(87, 59, 138, 1); 
}

.book-image {
  width: 100%;          
  height: 22rem;        
  object-fit: cover;    
  border-radius: 8px;   
}

.book-info {
  margin-top: 10px;
}

.book-info h3 {
  font-size: 1.2em;
  margin: 5px 0;
}

.book-info p {
  margin: 5px 0;
}

.borrow-btn {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.borrow-btn:hover {
  background-color: #45a049;
}

p {
  margin-top: 20px;
  font-size: 1.2em;
  color: #888;
}
h2{
  text-align: center;
  background-color: rgba(87, 59, 138, 0.9);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  padding: 2rem;
  font-size: 2rem;
  font-weight: bold;
  color:white;
}
</style>
