<template>
  <div>
    <h1 class="mb-3">
      <i class="bi bi-box-arrow-right me-2 text-warning"></i>Borrow Book
    </h1>

    <div class="row mt-4">
      <div class="col-lg-5">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">
              <i class="bi bi-pencil-square me-2"></i>Borrow Form
            </h5>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
            </div>

            <div v-if="success" class="alert alert-success">
              <i class="bi bi-check-circle me-2"></i>{{ success }}
            </div>

            <form @submit.prevent="borrowBook">
              <div class="mb-3">
                <label for="user" class="form-label">Select Member</label>
                <div class="input-group">
                  <span class="input-group-text bg-light">
                    <i class="bi bi-person text-primary"></i>
                  </span>
                  <select
                    class="form-select"
                    id="user"
                    v-model="borrowData.user"
                    required
                    :disabled="loading"
                  >
                    <option value="" disabled>Select a library member</option>
                    <option
                      v-for="user in regularUsers"
                      :key="user.id"
                      :value="user.id"
                    >
                      {{ user.username }} ({{ user.first_name }}
                      {{ user.last_name }})
                    </option>
                  </select>
                </div>
                <div class="form-text" v-if="regularUsers.length === 0">
                  <i class="bi bi-info-circle me-1"></i>No members available.
                </div>
              </div>

              <div class="mb-4">
                <label for="book" class="form-label">Select Book</label>
                <div class="input-group">
                  <span class="input-group-text bg-light">
                    <i class="bi bi-book text-primary"></i>
                  </span>
                  <select
                    class="form-select"
                    id="book"
                    v-model="borrowData.book"
                    required
                    :disabled="loading"
                  >
                    <option value="" disabled>Select a book to borrow</option>
                    <option
                      v-for="book in availableBooks"
                      :key="book.id"
                      :value="book.id"
                      :disabled="book.copies_available <= 0"
                    >
                      {{ book.title }} by {{ book.author }} ({{
                        book.copies_available
                      }}
                      copies available)
                    </option>
                  </select>
                </div>
                <div class="form-text" v-if="availableBooks.length === 0">
                  <i class="bi bi-info-circle me-1"></i>No books available for
                  borrowing.
                </div>
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="loading || !borrowData.user || !borrowData.book"
              >
                <span
                  v-if="loading"
                  class="spinner-border spinner-border-sm me-2"
                ></span>
                <i v-else class="bi bi-box-arrow-right me-1"></i>
                Borrow Book
              </button>
            </form>

            <div class="mt-4">
              <div class="d-flex align-items-center mb-2">
                <i class="bi bi-info-circle text-primary me-2"></i>
                <h6 class="mb-0">Borrowing Guidelines</h6>
              </div>
              <ul class="small text-muted ps-4">
                <li>Books can be borrowed for up to 14 days</li>
                <li>Return books on time to avoid late fees</li>
                <li>Handle books with care</li>
                <li>Report any damages immediately</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-7 mt-4 mt-lg-0">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-warning text-dark">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="bi bi-clock-history me-2"></i>Recently Borrowed Books
              </h5>
              <router-link to="/transactions" class="btn btn-sm btn-dark">
                View All
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <div v-if="loadingTransactions" class="text-center my-4">
              <div
                class="spinner-border spinner-border-sm text-primary"
                role="status"
              >
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-2">Loading recent transactions...</p>
            </div>

            <div
              v-else-if="recentTransactions.length === 0"
              class="text-center my-5"
            >
              <i class="bi bi-inbox text-muted" style="font-size: 3rem"></i>
              <p class="mt-3">No recent borrowing transactions</p>
            </div>

            <div v-else class="table-responsive">
              <table class="table table-hover">
                <thead class="table-light">
                  <tr>
                    <th>Book</th>
                    <th>Member</th>
                    <th>Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="transaction in recentTransactions"
                    :key="transaction.id"
                  >
                    <td>
                      <div class="d-flex align-items-center">
                        <i class="bi bi-book text-primary me-2"></i>
                        <span>{{ transaction.book_title }}</span>
                      </div>
                    </td>
                    <td>
                      <div class="d-flex align-items-center">
                        <i class="bi bi-person text-secondary me-2"></i>
                        <span>{{ transaction.user_name }}</span>
                      </div>
                    </td>
                    <td>{{ formatDate(transaction.borrow_date) }}</td>
                    <td>
                      <span class="badge bg-warning text-dark">
                        <i class="bi bi-arrow-right-circle me-1"></i>Borrowed
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BorrowBook",
  data() {
    return {
      borrowData: {
        user: "",
        book: "",
      },
      users: [],
      books: [],
      recentTransactions: [],
      loading: false,
      loadingTransactions: false,
      error: "",
      success: "",
    };
  },
  computed: {
    availableBooks() {
      return this.books.filter((book) => book.copies_available > 0);
    },
    regularUsers() {
      // Filter out users with is_superuser flag
      return this.users.filter((user) => !user.is_superuser);
    },
  },
  created() {
    this.fetchUsers();
    this.fetchBooks();
    this.fetchRecentTransactions();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get("users/");
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },

    async fetchBooks() {
      try {
        const response = await axios.get("books/");
        this.books = response.data;
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    },

    async fetchRecentTransactions() {
      this.loadingTransactions = true;
      try {
        const response = await axios.get("transactions/");
        this.recentTransactions = response.data
          .filter((t) => t.status === "borrowed")
          .slice(0, 5);
      } catch (error) {
        console.error("Error fetching transactions:", error);
      } finally {
        this.loadingTransactions = false;
      }
    },

    async borrowBook() {
      this.loading = true;
      this.error = "";
      this.success = "";

      try {
        await axios.post("borrow/", this.borrowData);

        this.success = "Book borrowed successfully!";
        this.borrowData = { user: "", book: "" };

        // Refresh data
        this.fetchBooks();
        this.fetchRecentTransactions();
      } catch (error) {
        console.error("Error borrowing book:", error);
        if (
          error.response &&
          error.response.data &&
          error.response.data.error
        ) {
          this.error = error.response.data.error;
        } else {
          this.error = "Failed to borrow book. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },
  },
};
</script>
