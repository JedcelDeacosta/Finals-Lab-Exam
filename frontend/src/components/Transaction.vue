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
    <div class="card shadow-sm">
      <div class="card-header bg-white">
        <div class="row align-items-center">
          <div class="col-md-6 mb-3 mb-md-0">
            <div class="btn-group">
              <button
                class="btn"
                :class="{
                  'btn-primary': filter === 'all',
                  'btn-outline-primary': filter !== 'all',
                }"
                @click="filter = 'all'"
              >
                <i class="bi bi-grid me-1"></i>All
              </button>
              <button
                class="btn"
                :class="{
                  'btn-warning': filter === 'borrowed',
                  'btn-outline-warning': filter !== 'borrowed',
                }"
                @click="filter = 'borrowed'"
              >
                <i class="bi bi-arrow-right me-1"></i>Borrowed
              </button>
              <button
                class="btn"
                :class="{
                  'btn-success': filter === 'returned',
                  'btn-outline-success': filter !== 'returned',
                }"
                @click="filter = 'returned'"
              >
                <i class="bi bi-arrow-return-left me-1"></i>Returned
              </button>
            </div>
          </div>

          <div class="col-md-6">
            <div class="input-group">
              <span class="input-group-text bg-light">
                <i class="bi bi-search"></i>
              </span>
              <input
                type="text"
                class="form-control"
                placeholder="Search by book title or username..."
                v-model="searchQuery"
              />
            </div>
          </div>
        </div>
      </div>
    </template>