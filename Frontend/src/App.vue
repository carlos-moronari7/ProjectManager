<template>
  <div v-if="!authStore.isAuthenticated" class="login-container">
    <RouterView />
  </div>
  <div v-else class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <i class="fa-solid fa-kanban me-2"></i> ProjectFlow
      </div>
      <ul class="sidebar-nav">
        <li class="nav-item">
          <RouterLink to="/"><i class="fa-solid fa-table-columns nav-icon"></i> Dashboard</RouterLink>
        </li>
        <li class="nav-item" v-if="authStore.isAdmin">
          <RouterLink to="/admin"><i class="fa-solid fa-user-shield nav-icon"></i> Admin Panel</RouterLink>
        </li>
      </ul>
    </aside>
    <div class="main-content">
      <header class="topbar">
        <div v-if="authStore.user" class="dropdown">
          <button class="btn btn-light dropdown-toggle" type="button" data-bs-toggle="dropdown">
            <i class="fa-solid fa-user-circle me-2"></i> {{ authStore.user.email }}
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><button class="dropdown-item" @click="authStore.logout()">
              <i class="fa-solid fa-right-from-bracket me-2"></i> Logout
            </button></li>
          </ul>
        </div>
      </header>
      <main class="content-wrapper">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
</script>

<style scoped>
.app-layout {
  display: flex;
  width: 100%;
}
.login-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>