<template>
  <div>
    <div
      class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4"
    >
      <div>
        <h1 class="mb-1">
          <i class="bi bi-list-check me-2 text-primary"></i>Borrowing
          Transactions
        </h1>
        <p class="text-muted mb-0" v-if="!loading && !error">
          Tracking all book borrowing and return activities
        </p>
      </div>
    </div>

    <!-- Stats cards -->
    <div class="row mb-4" v-if="!loading && !error && transactions.length > 0">
      <div class="col-md-4 mb-3 mb-md-0">
        <div class="card bg-primary text-white">
          <div class="card-body d-flex align-items-center">
            <div class="rounded-circle bg-white p-3 me-3">
              <i
                class="bi bi-list-check text-primary"
                style="font-size: 1.5rem"
              ></i>
            </div>
            <div>
              <h5 class="card-title mb-0">Total</h5>
              <p class="card-text display-6 mb-0">{{ transactions.length }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3 mb-md-0">
        <div class="card bg-warning text-dark">
          <div class="card-body d-flex align-items-center">
            <div class="rounded-circle bg-white p-3 me-3">
              <i
                class="bi bi-arrow-right text-warning"
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
      <div class="col-md-4">
        <div class="card bg-success text-white">
          <div class="card-body d-flex align-items-center">
            <div class="rounded-circle bg-white p-3 me-3">
              <i
                class="bi bi-arrow-return-left text-success"
                style="font-size: 1.5rem"
              ></i>
            </div>
            <div>
              <h5 class="card-title mb-0">Returned</h5>
              <p class="card-text display-6 mb-0">{{ returnedCount }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
    </template>