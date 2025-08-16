<template>
  <div class="app-container" :class="layoutClass">
    <aside v-if="authStore.isAuthenticated" class="sidebar">
      <div>
        <RouterLink to="/" class="sidebar-brand">
          <i class="fa-solid fa-rocket me-2"></i> ProjectFlow
        </RouterLink>
        <ul class="sidebar-nav">
          <li class="nav-item">
            <RouterLink to="/"><i class="fa-solid fa-table-columns nav-icon"></i> Dashboard</RouterLink>
          </li>
          <li class="nav-item" v-if="authStore.isAdmin">
            <RouterLink to="/admin"><i class="fa-solid fa-user-shield nav-icon"></i> Admin Panel</RouterLink>
          </li>
        </ul>
        <div v-if="projects.length > 0" class="sidebar-projects">
          <h6 class="projects-header">My Projects</h6>
          <ul class="projects-list">
            <li v-for="project in projects" :key="project.id">
              <RouterLink :to="{ name: 'project-detail', params: { id: project.id } }">
                <span class="project-dot"></span>
                {{ project.name }}
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
      <div class="sidebar-footer">
        <div v-if="authStore.user" class="user-profile">
            <i class="fa-solid fa-user-circle user-avatar"></i>
            <div class="user-info">
                <span class="user-name">{{ authStore.user.email }}</span>
                <span class="user-role">{{ authStore.user.role.name }}</span>
            </div>
            <button class="logout-button" @click="authStore.logout()" title="Logout">
                <i class="fa-solid fa-right-from-bracket"></i>
            </button>
        </div>
      </div>
    </aside>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/api';

const authStore = useAuthStore();
const route = useRoute();
const projects = ref([]);

const layoutClass = computed(() => {
  return authStore.isAuthenticated ? 'app-container--full' : 'app-container--centered';
});

const fetchProjects = async () => {
  if (authStore.isAuthenticated) {
    try {
      const response = await apiClient.get('/projects/');
      projects.value = response.data;
    } catch (error) {
      console.error("Failed to fetch projects for sidebar", error);
    }
  }
};

watch(() => authStore.isAuthenticated, (isAuth) => {
  if (isAuth) {
    fetchProjects();
  } else {
    projects.value = [];
  }
}, { immediate: true });

// Refetch projects when navigating to home to ensure list is fresh
watch(() => route.name, (newName) => {
    if (newName === 'home') {
        fetchProjects();
    }
});
</script>