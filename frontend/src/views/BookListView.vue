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
            <button @click="borrowBook(book.id)" class="borrow-btn">
              Borrow
            </button>
          </p>
          <p v-else>Not Available</p>
        </div>
      </div>
    </div>

    <p v-if="books.length === 0">No books available</p>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      books: [],  // Array to hold the books fetched from the backend
      userId: null,  // Logged-in user's ID
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
    async borrowBook(bookId) {
      try {
        const returnDate = this.calculateReturnDate();  // You can adjust this logic for return date (e.g., 14 days from now)
        const response = await axios.post('http://127.0.0.1:5000/loans/borrow', {
          user_id: this.userId,
          book_id: bookId,
          return_date: returnDate,
        });
        
        console.log(response);  // Check the full response object

        // Check if the response indicates success or failure
        if (response.data.success) {
          alert(response.data.message);  // Show success message
          this.fetchBooks();  // Refresh the book list to reflect the availability
        } else {
          // If success is not true, show the error message
          alert(response.data.message);  // Display message sent from the backend
        }
      } catch (error) {
        // If any error occurs during the request or response handling
        console.error('Error borrowing book:', error);
        alert('Failed to borrow book. Please try again.');
      }
    },
    calculateReturnDate() {
      // Calculate return date (e.g., 14 days from today)
      const today = new Date();
      today.setDate(today.getDate() + 14);  // Set return date to 14 days later
      return today.toISOString().split('T')[0];  // Return the date in YYYY-MM-DD format
    },
  },
};
</script>

<style scoped>
.browse-books {
  width: 100%;  /* Make the container take up the full width */
  padding: 0px; 
  overflow-x: auto;
  background-image: url('images/booklist-background.jpg'); /* Set the background image */
  background-size: cover; /* Make the image cover the entire area */
  background-position: center;   /* Ensure container does not overflow */
/* Add some padding to the container */
}
.book-list {

  padding: 50px;
  display: flex;
  flex-wrap: wrap;  /* Allow books to wrap to the next line */
  justify-content: space-between;  /* Center books in the row */
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
  background-color: #f9f9f9;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* Shadow effect */
}

.book-image {
  width: 100%;          /* Ensure image takes the full width of the container */
  height: 22rem;        /* Set a fixed height for all images */
  object-fit: cover;    /* Ensure the image covers the area without distortion */
  border-radius: 8px;   /* Keep the rounded corners */
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
  background-color: rgba(167, 199, 231, 0.7);
  padding: 2rem;
  font-size: 2rem;
  font-weight: bold;
}
</style>
