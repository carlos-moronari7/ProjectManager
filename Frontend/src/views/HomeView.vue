<template>
  <div>
    <h1 class="mb-4">Dashboard</h1>
    <div class="card mb-4" v-if="authStore.user && authStore.user.role.name !== 'member'">
      <div class="card-body">
        <h5 class="card-title"><i class="fa-solid fa-plus-circle me-2 text-success"></i>Create a New Project</h5>
        <form @submit.prevent="createProject">
          <div class="row">
            <div class="col-md-5 mb-2">
              <input type="text" class="form-control" placeholder="Project Name" v-model="newProject.name" required>
            </div>
            <div class="col-md-5 mb-2">
              <input type="text" class="form-control" placeholder="Project Description" v-model="newProject.description">
            </div>
            <div class="col-md-2 mb-2 d-grid">
              <button type="submit" class="btn btn-primary">Create</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <h2><i class="fa-solid fa-folder-open me-2"></i>My Projects</h2>
    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2">Loading projects...</p>
    </div>
    <div v-else-if="projects.length > 0" class="row mt-3">
      <div v-for="project in projects" :key="project.id" class="col-lg-4 col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ project.name }}</h5>
            <p class="card-text text-muted flex-grow-1">{{ project.description || 'No description.' }}</p>
            <RouterLink :to="{ name: 'project-detail', params: { id: project.id } }" class="btn btn-outline-primary mt-auto">
              Open Project <i class="fa-solid fa-arrow-right ms-1"></i>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-secondary mt-3">
      <i class="fa-solid fa-info-circle me-2"></i> You are not a member of any projects yet.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import apiClient from '@/api';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const projects = ref([]);
const loading = ref(true);
const newProject = ref({ name: '', description: '' });

const fetchProjects = async () => {
  try {
    const response = await apiClient.get('/projects/');
    projects.value = response.data;
  } catch (error) {
    console.error('Failed to fetch projects:', error);
  } finally {
    loading.value = false;
  }
};

const createProject = async () => {
  try {
    const response = await apiClient.post('/projects/', newProject.value);
    projects.value.push(response.data);
    newProject.value.name = '';
    newProject.value.description = '';
  } catch (error) {
    console.error('Failed to create project:', error);
  }
};

onMounted(fetchProjects);
</script>