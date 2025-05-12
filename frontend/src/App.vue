<template>
  <div class="app-container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand d-flex align-items-center" to="/">
          <i
            class="bi bi-book-half me-2 text-warning"
            style="font-size: 1.5rem"
          ></i>
          <span class="fw-bold">LibraryBro</span>
          <span class="badge bg-warning text-dark ms-2 d-none d-md-inline"
            >Management System</span
          >
        </router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <i class="bi bi-journals me-1"></i>Books
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/borrow">
                <i class="bi bi-box-arrow-right me-1"></i>Borrow
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/return">
                <i class="bi bi-box-arrow-in-left me-1"></i>Return
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/transactions">
                <i class="bi bi-list-check me-1"></i>Transactions
              </router-link>
            </li>
          </ul>
          <div class="d-flex align-items-center">
            <span class="text-light me-2 d-none d-md-block">
              <i class="bi bi-calendar-date me-1"></i>{{ currentDate }}
            </span>
          </div>
        </div>
      </div>
    </nav>

    <div class="page-content py-4">
      <div class="container">
        <router-view></router-view>
      </div>
    </div>

    <footer class="footer bg-light py-3 mt-auto">
      <div class="container">
        <div class="d-flex justify-content-between align-items-center">
          <span class="text-muted">© 2025 LibraryBro Management System</span>
          <div>
            <i class="bi bi-book text-primary me-1"></i>
            <span class="text-muted">Manage your library with ease</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      currentDate: new Date().toLocaleDateString("en-US", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      }),
    };
  },
};
</script>

<style>
/* Global styles */
:root {
  --primary-color: #2c3e50;
  --secondary-color: #f39c12;
  --accent-color: #3498db;
  --success-color: #27ae60;
  --danger-color: #e74c3c;
  --light-bg: #f8f9fa;
  --dark-bg: #343a40;
}

body {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-content {
  flex: 1;
  background-color: #f5f5f5;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-size: 1.4rem;
}

.card {
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-primary:hover {
  background-color: #1e2b38;
  border-color: #1e2b38;
}

.btn-warning {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}

.table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.table thead {
  background-color: var(--primary-color);
  color: white;
}

.nav-link.router-link-active {
  font-weight: bold;
  color: var(--secondary-color) !important;
  border-bottom: 2px solid var(--secondary-color);
}

.footer {
  border-top: 1px solid #e9ecef;
}

/* Custom form styling */
.form-control:focus,
.form-select:focus {
  border-color: var(--accent-color);
  box-shadow: 0 0 0 0.25rem rgba(52, 152, 219, 0.25);
}

/* Badge styling */
.badge.bg-warning {
  background-color: var(--secondary-color) !important;
}

.badge.bg-success {
  background-color: var(--success-color) !important;
}

.badge.bg-danger {
  background-color: var(--danger-color) !important;
}
</style>
