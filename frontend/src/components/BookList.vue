<template>
  <div>
    <!-- Improved header with stats -->
    <div
      class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4"
    >
      <div>
        <h1 class="mb-1">
          <i class="bi bi-journals me-2 text-primary"></i>Book Collection
        </h1>
        <p class="text-muted mb-0" v-if="!loading && !error">
          Managing <span class="fw-bold">{{ books.length }}</span> books in your
          library
        </p>
      </div>
      <button class="btn btn-primary mt-3 mt-md-0" @click="openAddBookModal">
        <i class="bi bi-plus-circle me-1"></i>Add New Book
      </button>
    </div>

    <!-- Stats cards -->
    <div class="row mb-4" v-if="!loading && !error && books.length > 0">
      <div class="col-md-4 mb-3 mb-md-0">
        <div class="card bg-primary text-white">
          <div class="card-body d-flex align-items-center">
            <div class="rounded-circle bg-white p-3 me-3">
              <i class="bi bi-book text-primary" style="font-size: 1.5rem"></i>
            </div>
            <div>
              <h5 class="card-title mb-0">Total Books</h5>
              <p class="card-text display-6 mb-0">{{ books.length }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3 mb-md-0">
        <div class="card bg-success text-white">
          <div class="card-body d-flex align-items-center">
            <div class="rounded-circle bg-white p-3 me-3">
              <i
                class="bi bi-check-circle text-success"
                style="font-size: 1.5rem"
              ></i>
            </div>
            <div>
              <h5 class="card-title mb-0">Available</h5>
              <p class="card-text display-6 mb-0">{{ availableCount }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-warning text-dark">
          <div class="card-body d-flex align-items-center">
            <div class="rounded-circle bg-white p-3 me-3">
              <i
                class="bi bi-people text-warning"
                style="font-size: 1.5rem"
              ></i>
            </div>
            <div>
              <h5 class="card-title mb-0">Borrowed</h5>
              <p class="card-text display-6 mb-0">{{ borrowedCount }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and filter -->
    <div class="card mb-4" v-if="!loading && !error && books.length > 0">
      <div class="card-body">
        <div class="input-group">
          <span class="input-group-text bg-white">
            <i class="bi bi-search"></i>
          </span>
          <input
            type="text"
            class="form-control border-start-0"
            placeholder="Search by title, author or ISBN..."
            v-model="searchQuery"
          />
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading books...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
    </div>

    <!-- Empty state -->
    <div
      v-else-if="books.length === 0"
      class="text-center my-5 py-5 bg-white rounded shadow-sm"
    >
      <i class="bi bi-book text-muted" style="font-size: 4rem"></i>
      <h3 class="mt-3">Your library is empty</h3>
      <p class="text-muted mb-4">
        Start building your collection by adding your first book.
      </p>
      <button class="btn btn-primary btn-lg" @click="openAddBookModal">
        <i class="bi bi-plus-circle me-1"></i>Add Your First Book
      </button>
    </div>

    <!-- Books table with improved design -->
    <div v-else>
      <div class="table-responsive">
        <table class="table table-hover bg-white">
          <thead class="table-dark">
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>ISBN</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in filteredBooks" :key="book.id">
              <td>
                <div class="d-flex align-items-center">
                  <div class="book-icon me-2">
                    <i class="bi bi-book text-primary"></i>
                  </div>
                  <div>
                    <div class="fw-bold">{{ book.title }}</div>
                  </div>
                </div>
              </td>
              <td>{{ book.author }}</td>
              <td>
                <span class="badge bg-light text-dark">{{ book.isbn }}</span>
              </td>
              <td>
                <span
                  class="badge rounded-pill"
                  :class="{
                    'bg-success': book.copies_available > 3,
                    'bg-warning text-dark':
                      book.copies_available > 0 && book.copies_available <= 3,
                    'bg-danger': book.copies_available === 0,
                  }"
                >
                  <i
                    class="bi"
                    :class="{
                      'bi-check-circle-fill': book.copies_available > 0,
                      'bi-x-circle-fill': book.copies_available === 0,
                    }"
                  ></i>
                  {{
                    book.copies_available > 0
                      ? `${book.copies_available} Available`
                      : "Out of Stock"
                  }}
                </span>
              </td>
              <td>
                <div class="btn-group">
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editBook(book)"
                    :disabled="book.copies_available < book.total_copies"
                    :title="
                      book.copies_available < book.total_copies
                        ? 'Cannot edit while copies are borrowed'
                        : 'Edit Book'
                    "
                  >
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button
                    class="btn btn-sm btn-outline-danger"
                    @click="confirmDeleteBook(book)"
                    :disabled="book.copies_available < book.total_copies"
                    title="Delete Book"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
                <small
                  v-if="book.copies_available < book.total_copies"
                  class="d-block text-danger mt-1"
                >
                  <i class="bi bi-info-circle"></i> Book has borrowed copies
                </small>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- No results message -->
      <div
        v-if="filteredBooks.length === 0 && searchQuery"
        class="alert alert-info"
      >
        <i class="bi bi-info-circle me-2"></i>No books match your search
        criteria.
      </div>
    </div>

    <!-- Add/Edit Book Modal with improved design -->
    <div class="modal fade" id="bookModal" tabindex="-1" ref="bookModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-light">
            <h5 class="modal-title">
              <i
                class="bi"
                :class="isEditing ? 'bi-pencil-square' : 'bi-plus-circle'"
              ></i>
              {{ isEditing ? "Edit Book" : "Add New Book" }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <!-- Display update error message -->
            <div v-if="updateError" class="alert alert-danger mb-3">
              <i class="bi bi-exclamation-triangle me-2"></i>{{ updateError }}
            </div>

            <form @submit.prevent="saveBook">
              <div class="mb-3">
                <label for="title" class="form-label">Title</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-book"></i
                  ></span>
                  <input
                    type="text"
                    class="form-control"
                    id="title"
                    v-model="currentBook.title"
                    required
                  />
                </div>
              </div>
              <div class="mb-3">
                <label for="author" class="form-label">Author</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-person"></i
                  ></span>
                  <input
                    type="text"
                    class="form-control"
                    id="author"
                    v-model="currentBook.author"
                    required
                  />
                </div>
              </div>
              <div class="mb-3">
                <label for="isbn" class="form-label">ISBN</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-upc-scan"></i
                  ></span>
                  <input
                    type="text"
                    class="form-control"
                    id="isbn"
                    v-model="currentBook.isbn"
                    required
                    :disabled="isEditing"
                    pattern="[0-9]{10}|[0-9]{13}"
                    title="ISBN must be 10 or 13 digits"
                  />
                </div>
                <div class="form-text" v-if="!isEditing">
                  ISBN must be 10 or 13 digits
                </div>
              </div>
              <div class="mb-3">
                <label for="copies" class="form-label">Copies Available</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-123"></i
                  ></span>
                  <input
                    type="number"
                    class="form-control"
                    id="copies"
                    v-model="currentBook.copies_available"
                    min="1"
                    required
                  />
                </div>
              </div>
              <div class="d-flex justify-content-end">
                <button
                  type="button"
                  class="btn btn-outline-secondary me-2"
                  data-bs-dismiss="modal"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="saving"
                >
                  <span
                    v-if="saving"
                    class="spinner-border spinner-border-sm me-1"
                  ></span>
                  <i
                    class="bi"
                    :class="isEditing ? 'bi-save' : 'bi-plus-circle'"
                  ></i>
                  {{ isEditing ? "Save Changes" : "Add Book" }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal with improved design -->
    <div class="modal fade" id="deleteModal" tabindex="-1" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="bi bi-exclamation-triangle me-2"></i>Confirm Delete
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              Are you sure you want to delete the book "<strong>{{
                bookToDelete?.title
              }}</strong
              >"?
            </p>
            <p class="text-danger">
              <i class="bi bi-exclamation-circle me-1"></i>This action cannot be
              undone.
            </p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-outline-secondary"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              @click="deleteBook"
              :disabled="deleting"
            >
              <span
                v-if="deleting"
                class="spinner-border spinner-border-sm me-1"
              ></span>
              <i class="bi bi-trash me-1"></i>Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Modal } from "bootstrap";

export default {
  name: "BookList",
  data() {
    return {
      books: [],
      loading: true,
      error: null,
      updateError: "", // Added to store update-specific errors
      bookModal: null,
      deleteModal: null,
      currentBook: {
        title: "",
        author: "",
        isbn: "",
        copies_available: 1,
      },
      bookToDelete: null,
      isEditing: false,
      saving: false,
      deleting: false,
      searchQuery: "",
    };
  },
  computed: {
    // Calculate total available books
    availableCount() {
      return this.books.filter((book) => book.copies_available > 0).length;
    },
    // Calculate total borrowed books
    borrowedCount() {
      return this.books.filter((book) => book.copies_available === 0).length;
    },
    // Filter books based on search query
    filteredBooks() {
      if (!this.searchQuery) return this.books;

      const query = this.searchQuery.toLowerCase();
      return this.books.filter(
        (book) =>
          book.title.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query) ||
          book.isbn.includes(query)
      );
    },
  },
  async created() {
    this.fetchBooks();
  },
  mounted() {
    // Initialize Bootstrap modals
    this.bookModal = new Modal(this.$refs.bookModal);
    this.deleteModal = new Modal(this.$refs.deleteModal);
  },
  methods: {
    async fetchBooks() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.get("books/");
        this.books = response.data;
      } catch (error) {
        console.error("Error fetching books:", error);
        this.error = "Failed to load books. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    openAddBookModal() {
      this.isEditing = false;
      this.updateError = ""; // Clear any previous errors
      this.currentBook = {
        title: "",
        author: "",
        isbn: "",
        copies_available: 1,
      };
      this.bookModal.show();
    },

    editBook(book) {
      // Check if book has borrowed copies
      if (book.copies_available < book.total_copies) {
        alert(
          "Cannot edit book while copies are borrowed. All copies must be returned first."
        );
        return;
      }

      this.isEditing = true;
      this.updateError = ""; // Clear any previous errors
      this.currentBook = { ...book };
      this.bookModal.show();
    },

    async saveBook() {
      this.saving = true;
      this.updateError = ""; // Clear any previous errors

      try {
        if (this.isEditing) {
          await axios.put(`books/${this.currentBook.id}/`, this.currentBook);
        } else {
          await axios.post("books/", this.currentBook);
        }

        this.bookModal.hide();
        this.fetchBooks();
      } catch (error) {
        console.error("Error saving book:", error);

        if (error.response && error.response.status === 400) {
          if (error.response.data && error.response.data.error) {
            // Display the specific error message from the backend
            this.updateError = error.response.data.error;
          } else {
            this.updateError = "Failed to save book due to validation errors.";
          }
        } else {
          this.updateError =
            "Failed to save book. Please check the form and try again.";
        }
      } finally {
        this.saving = false;
      }
    },

    confirmDeleteBook(book) {
      this.bookToDelete = book;
      this.deleteModal.show();
    },

    async deleteBook() {
      this.deleting = true;

      try {
        await axios.delete(`books/${this.bookToDelete.id}/`);
        this.deleteModal.hide();
        this.fetchBooks();
      } catch (error) {
        console.error("Error deleting book:", error);
        if (error.response && error.response.status === 400) {
          alert(
            error.response.data.error ||
              "Cannot delete book with active borrow records"
          );
        } else {
          alert("Failed to delete book. Please try again.");
        }
      } finally {
        this.deleting = false;
      }
    },
  },
};
</script>

<style scoped>
.book-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e9ecef;
  border-radius: 4px;
}

.table th {
  font-weight: 600;
}

.table td {
  vertical-align: middle;
}
</style>
