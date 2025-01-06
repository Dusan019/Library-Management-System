<template>
  
  <div class="manage-books">
    <h1>Manage Books</h1>
    <Button 
      buttonText="Add New Book" 
      color="blue" 
      @click="showAddModal = true" 
    />
    <!-- Button to open the modal for adding a new book -->
    
    <!-- Book Table -->
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Author</th>
          <th>Availability</th>
          <th>Quantity</th>
          <th>Book Image</th> <!-- Display Quantity -->
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in paginatedBooks" :key="book.id">

          <td>{{ book.title }}</td>
          <td>{{ book.author }}</td>
          <td>{{ book.available ? 'Available' : 'Not Available' }}</td>
          <td><span id="quantity-cell">{{ book.quantity }}</span></td>
          <td>
        <!-- Display image with small size and zoom effect on hover -->
        <div class="book-image" @click="openImageModal(book.image_url)">
              <img :src="book.image_url" alt="Book Image" />
            </div>
      </td> <!-- Show Quantity -->
          <td>
            <button class="edit-btn" @click="editBook(book.id)">✏️</button>
            <button class="delete-btn" @click="deleteBook(book.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
  <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
  <span>Page {{ currentPage }}</span>
  <button @click="nextPage" :disabled="currentPage * booksPerPage >= books.length">Next</button>
</div>
<div v-if="showImageModal" class="image-modal" @click="closeImageModal">
      <div class="image-modal-content" @click.stop>
        <img :src="modalImage" alt="Enlarged Book Image" />
        <button @click="closeImageModal" class="close-button">Close</button>
      </div>
    </div>  

    <!-- Modal for adding a new book -->
    <div v-if="showAddModal" class="modal">
  <div class="modal-content">
    <h2>Add New Book</h2>
    <form @submit.prevent="addBook">
      <label for="title">Title:</label>
      <input type="text" v-model="newBook.title" required />
      
      <label for="author">Author:</label>
      <input type="text" v-model="newBook.author" required />
      
      <label for="quantity">Quantity:</label>
      <input type="number" v-model="newBook.quantity" required min="0" />
      
      <label for="image">Book Image:</label>
      <input type="file" id='image' @change="handleImageUpload" accept="image/*" />

      <button type="submit">Add Book</button>
      <button @click="closeAddModal" type="button">Close</button>
    </form>
  </div>
</div>

<!-- Modal for editing a book -->
<div v-if="showEditModal" class="modal">
  <div class="modal-content">
    <h2>Edit Book</h2>
    <form @submit.prevent="updateBook">
      <label for="title">Title:</label>
      <input type="text" v-model="editForm.title" required />
      
      <label for="author">Author:</label>
      <input type="text" v-model="editForm.author" required />
      
      <label for="quantity">Quantity:</label>
      <input type="number" v-model="editForm.quantity" required min="0" />
      
      <label for="image">Book Image:</label>
      <input type="file" @change="handleImageUpload" accept="image/*" />
      

      <button type="submit">Update</button>
      <button @click="closeEditModal" type="button">Close</button>
    </form>
  </div>
</div>
  </div>
</template>

<script>
import axios from 'axios';
import Button from '@/components/Button.vue';
export default {
  data() {
    return {
      books: [],
      showImageModal: false, // Control visibility of the image modal
      modalImage: '',   // Store list of books
      showEditModal: false, // Control visibility of the edit modal
      showAddModal: false, // Control visibility of the add book modal
      editForm: {
        id: null,
        title: '',
        author: '',
        available: true,
        quantity: 1, // Ensure quantity field is initialized
      },
      newBook: {
        title: '',
        author: '',
        available: true,
        quantity: 1,
        image: null, // Ensure quantity field is initialized
      },
      currentPage: 1, // Current page number
    booksPerPage: 3,
    };
  },
  computed: {
  paginatedBooks() {
    const startIndex = (this.currentPage - 1) * this.booksPerPage;
    const endIndex = startIndex + this.booksPerPage;
    return this.books.slice(startIndex, endIndex);
  },
},
  components: {
    Button, // Register the Button component
  },
  created() {
    this.fetchBooks(); // Fetch books when the page loads
  },
  methods: {
    openImageModal(imageUrl) {
      this.modalImage = imageUrl; // Set the image URL to be shown in the modal
      this.showImageModal = true; // Show the modal
    },
    // Close the modal
    closeImageModal() {
      this.showImageModal = false; // Hide the modal
    },  
  handleImageUpload(event) {
  const file = event.target.files[0];
  if (file) {
    this.newBook.image = file;
    this.editForm.image = file;
  }
},
    // Fetch all books from the backend
    async fetchBooks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/books');
        this.books = response.data;
        this.resetPage();
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },

    // Add a new book
    async addBook() {
  try {
    const formData = new FormData();
    formData.append('title', this.newBook.title);
    formData.append('author', this.newBook.author);
    formData.append('quantity', this.newBook.quantity);

    // Add image file only once
    if (this.newBook.image) {
      formData.append('image', this.newBook.image);
    }

    // Send the FormData object
    const response = await axios.post('http://127.0.0.1:5000/books/add', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.message === 'Book added successfully') {
      this.fetchBooks(); // Reload books after successful addition
      this.newBook = { title: '', author: '', available: true, quantity: 1, image: null }; // Clear form
      this.closeAddModal(); // Close the add modal
    }
  } catch (error) {
    console.error('Error adding book:', error);
  }
},

    // Open the edit modal and populate the form with the book's details
    editBook(bookId) {
      const book = this.books.find(b => b.id === bookId);
      if (book) {
        this.editForm = { ...book }; // Copy book details to editForm
        this.showEditModal = true; // Show the modal
      }
    },

    // Close the add book modal
    closeAddModal() {
      this.showAddModal = false;
    },

    // Close the edit book modal
    closeEditModal() {
      this.showEditModal = false;
    },

    // Update the book information
    async updateBook() {
    try {
      const formData = new FormData();
      formData.append('title', this.editForm.title);
      formData.append('author', this.editForm.author);
      formData.append('quantity', this.editForm.quantity);
      
      // Add image if it's present
      if (this.editForm.image) {
        formData.append('image', this.editForm.image);
      }

      const response = await axios.put(`http://127.0.0.1:5000/books/${this.editForm.id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.message === 'Book updated successfully') {
        this.fetchBooks(); // Reload books after successful update
        this.closeEditModal(); // Close the modal
      }
    } catch (error) {
      console.error('Error updating book:', error);
    }
  },

    // Delete a book
    async deleteBook(bookId) {
      try {
        const response = await axios.delete(`http://127.0.0.1:5000/books/${bookId}`);
        if (response.data.message === 'Book deleted successfully') {
          this.fetchBooks(); // Reload books after successful deletion
        }
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    },
    nextPage() {
    if (this.currentPage * this.booksPerPage < this.books.length) {
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
  }
  },
};

</script>

<style scoped>
#quantity-cell{
  font-size: 1.9rem;
}
.book-image img {
  width: 50px; /* Small thumbnail size */
  height: 70px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.book-image:hover img {
  transform: scale(1.1); /* Slight zoom on hover */
}

/* Modal background */
.image-modal {
  height: 100%;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7); /* Semi-transparent black background */
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(10px); /* Blur the background behind the image */
  z-index: 1000; /* Ensure modal is on top */
}

/* Modal content for the image */
.image-modal-content {
  position: relative;
  background-color: transparent; /* Remove background color */
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 70%; /* Limit the width of the image */
  max-height: 70%; /* Limit the height of the image */
  padding: 0;
  border-radius: 10px; /* Optionally add rounded corners */
  box-shadow: none; /* Remove any shadow */
}

/* Image styling */
.image-modal-content img {
  width: 100%; /* Image width will be 100% of the modal content container */
  height: auto; /* Maintain aspect ratio */
  max-width: 400px; /* Limit the maximum size of the image */
  max-height: 400px; /* Limit the maximum height of the image */
  object-fit: contain; /* Maintain aspect ratio */
  border-radius: 5px; /* Optional rounded corners */
}

/* Close button */
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: red;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
}

.close-button:hover {
  background-color: darkred;
}
.pagination{
  text-align: center;
  margin-top: 0.5rem;
}
.manage-books {
  margin: 0px;
  max-width: 100%;
  max-height: 100%;
  height: 100%;
  width:100%;
  padding: 3rem;
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
.edit-btn{
  width: 3rem;
  font-size: 1.2rem;
  height: 3rem;
}
.delete-btn{
  width: 3rem;
  font-size: 1.2rem;
  height: 3rem;
  
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
  width:16.6%;
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
  font-size: 1.2rem;
  padding: 0rem;
  
}

button {
  padding: 8px 12px;
  margin-right: 10px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

 button:hover {
  background-color: #0056b3;
}
 button:focus {
  outline: none;
}

.add-book-form {
  margin-bottom: 20px;
}

.add-book-form form {
  display: flex;
  flex-direction: column;
}

.add-book-form label {
  margin-bottom: 8px;
  font-weight: 600;
}

.add-book-form input, .add-book-form select {
  margin-bottom: 12px;
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #f9f9f9;
}

.add-book-form button {
  padding: 12px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-book-form button:hover {
  background-color: #218838;
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
  padding: 30px;
  border-radius: 8px;
  width: 450px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
}

input, select {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #f9f9f9;
}

button[type="submit"] {
  background-color: #28a745;
  padding: 12px;
}

button[type="submit"]:hover {
  background-color: #218838;
}

button[type="button"] {
  background-color: #dc3545;
  padding: 12px;
}

button[type="button"]:hover {
  background-color: #c82333;
}
</style>
