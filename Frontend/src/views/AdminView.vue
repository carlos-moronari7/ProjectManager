<template>
  <div class="full-height-container">
    <div class="page-header">
      <h1>Admin Panel</h1>
    </div>
    <div class="admin-layout">
      <aside class="admin-sidebar">
        <nav class="admin-nav">
          <RouterLink to="/admin/users" class="admin-nav-link">
            <i class="fa-solid fa-users nav-icon"></i>
            <span>User Management</span>
          </RouterLink>
          <a href="#" class="admin-nav-link disabled" title="Coming Soon">
            <i class="fa-solid fa-shield-halved nav-icon"></i>
            <span>Roles & Permissions</span>
          </a>
          <a href="#" class="admin-nav-link disabled" title="Coming Soon">
            <i class="fa-solid fa-gears nav-icon"></i>
            <span>System Settings</span>
          </a>
        </nav>
      </aside>
      <main class="admin-content">
        <!-- The nested route component (e.g., UserManagement) will be rendered here -->
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>