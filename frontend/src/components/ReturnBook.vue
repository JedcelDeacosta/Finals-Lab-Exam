<template>
  <div>
    <h1 class="mb-3">
      <i class="bi bi-box-arrow-in-left me-2 text-success"></i>Return Book
    </h1>

    <div class="row mt-4">
      <div class="col-lg-5">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">
              <i class="bi bi-arrow-return-left me-2"></i>Return Form
            </h5>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
            </div>

            <div v-if="success" class="alert alert-success">
              <i class="bi bi-check-circle me-2"></i>{{ success }}
            </div>

            <form @submit.prevent="returnBook">
              <div class="mb-4">
                <label for="transaction" class="form-label"
                  >Select Borrowed Book</label
                >
                <div class="input-group">
                  <span class="input-group-text bg-light">
                    <i class="bi bi-book-half text-success"></i>
                  </span>
                  <select
                    class="form-select"
                    id="transaction"
                    v-model="returnData.transaction_id"
                    required
                    :disabled="loading || borrowedBooks.length === 0"
                  >
                    <option value="" disabled>Select a book to return</option>
                    <option
                      v-for="transaction in borrowedBooks"
                      :key="transaction.id"
                      :value="transaction.id"
                    >
                      {{ transaction.book_title }} - Borrowed by
                      {{ transaction.user_name }} on
                      {{ formatDate(transaction.borrow_date) }}
                    </option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                class="btn btn-success w-100"
                :disabled="
                  loading ||
                  !returnData.transaction_id ||
                  borrowedBooks.length === 0
                "
              >
                <span
                  v-if="loading"
                  class="spinner-border spinner-border-sm me-2"
                ></span>
                <i v-else class="bi bi-box-arrow-in-left me-1"></i>
                Return Book
              </button>
            </form>

            <div
              v-if="borrowedBooks.length === 0"
              class="alert alert-info mt-4"
            >
              <div class="d-flex">
                <i class="bi bi-info-circle-fill me-2 fs-4"></i>
                <div>
                  <h6 class="alert-heading">No Books to Return</h6>
                  <p class="mb-0">
                    There are no books currently borrowed that need to be
                    returned.
                  </p>
                </div>
              </div>
            </div>

            <div class="mt-4" v-if="borrowedBooks.length > 0">
              <div class="d-flex align-items-center mb-2">
                <i class="bi bi-info-circle text-success me-2"></i>
                <h6 class="mb-0">Return Process</h6>
              </div>
              <ol class="small text-muted ps-4">
                <li>Select the book being returned from the dropdown</li>
                <li>Check the book for any damages before returning</li>
                <li>Click the "Return Book" button to complete the process</li>
                <li>The system will automatically update the inventory</li>
              </ol>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-7 mt-4 mt-lg-0">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-info text-white">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="bi bi-clock-history me-2"></i>Recently Returned Books
              </h5>
              <router-link to="/transactions" class="btn btn-sm btn-dark">
                View All
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <div v-if="loadingTransactions" class="text-center my-4">
              <div
                class="spinner-border spinner-border-sm text-info"
                role="status"
              >
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-2">Loading recent returns...</p>
            </div>

            <div
              v-else-if="recentReturns.length === 0"
              class="text-center my-5"
            >
              <i class="bi bi-inbox text-muted" style="font-size: 3rem"></i>
              <p class="mt-3">No recent return transactions</p>
            </div>

            <div v-else class="table-responsive">
              <table class="table table-hover">
                <thead class="table-light">
                  <tr>
                    <th>Book</th>
                    <th>Member</th>
                    <th>Borrowed</th>
                    <th>Returned</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="transaction in recentReturns"
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
                      <span class="badge bg-success">
                        <i class="bi bi-check-circle me-1"></i
                        >{{ formatDate(transaction.return_date) }}
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
  name: "ReturnBook",
  data() {
    return {
      returnData: {
        transaction_id: "",
      },
      borrowedBooks: [],
      recentReturns: [],
      loading: false,
      loadingTransactions: false,
      error: "",
      success: "",
    };
  },
  created() {
    this.fetchBorrowedBooks();
    this.fetchRecentReturns();
  },
  methods: {
    async fetchBorrowedBooks() {
      this.loading = true;
      try {
        const response = await axios.get("transactions/");
        this.borrowedBooks = response.data.filter(
          (t) => t.status === "borrowed"
        );
      } catch (error) {
        console.error("Error fetching borrowed books:", error);
        this.error = "Failed to load borrowed books. Please try again.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>