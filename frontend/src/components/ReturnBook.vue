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
            <form @submit.prevent>
              <div class="mb-4">
                <label for="transaction" class="form-label">Select Borrowed Book</label>
                <div class="input-group">
                  <span class="input-group-text bg-light">
                    <i class="bi bi-book-half text-success"></i>
                  </span>
                  <select class="form-select" id="transaction" disabled>
                    <option value="" disabled>Select a book to return</option>
                  </select>
                </div>
              </div>
              <button type="submit" class="btn btn-success w-100" disabled>
                Return Book
              </button>
            </form>
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
          <div class="card-body text-center text-muted">
            <p>No recent return transactions</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReturnBook",
};
</script>
