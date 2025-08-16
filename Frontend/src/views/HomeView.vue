<template>
  <div>
    <div class="page-header">
      <h1>Dashboard</h1>
      <button @click="showCreateModal = true" class="btn btn-primary" v-if="canCreateProjects">
        <i class="fa-solid fa-plus me-1"></i> New Project
      </button>
    </div>

    <SkeletonLoader v-if="loading" type="card" :count="3" />
    <div v-else-if="projects.length > 0" class="project-grid">
      <RouterLink v-for="project in projects" :key="project.id" :to="{ name: 'project-detail', params: { id: project.id } }" class="project-card-link">
        <div class="project-card">
            <div class="project-card-header">
                <h5 class="project-card-title">{{ project.name }}</h5>
                <button @click.prevent class="options-button"><i class="fa-solid fa-ellipsis-vertical"></i></button>
            </div>
            <div class="project-card-body">
                <p class="project-card-description">{{ project.description || 'No description provided.' }}</p>
            </div>
            <div class="project-card-footer">
                <div class="project-team">
                    <div v-for="member in project.project_members.slice(0, 3)" :key="member.user.id" class="avatar" :style="{ backgroundColor: getAvatarColor(member.user.email) }" :title="member.user.email">
                        {{ getInitials(member.user.email) }}
                    </div>
                    <div v-if="project.project_members.length > 3" class="avatar-more">+{{ project.project_members.length - 3 }}</div>
                </div>
            </div>
        </div>
      </RouterLink>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">
        <i class="fa-solid fa-folder-open"></i>
      </div>
      <h2>No Projects Found</h2>
      <p>You haven't been assigned to any projects yet.</p>
      <button @click="showCreateModal = true" class="btn btn-primary mt-3" v-if="canCreateProjects">
        <i class="fa-solid fa-plus me-1"></i> Create Your First Project
      </button>
    </div>
    
    <!-- THIS IS THE CORRECT MODAL IMPLEMENTATION -->
    <AppModal v-if="showCreateModal" title="Create New Project" @close="showCreateModal = false">
        <form @submit.prevent="createProject">
            <div class="form-group">
                <label>Project Name</label>
                <input type="text" v-model="newProject.name" placeholder="e.g., Q4 Marketing Campaign" required />
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea v-model="newProject.description" rows="3" placeholder="A short summary of what this project is about..."></textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" @click="showCreateModal = false">Cancel</button>
                <button type="submit" class="btn btn-primary">Create Project</button>
            </div>
        </form>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { RouterLink } from 'vue-router';
import apiClient from '@/api';
import { useAuthStore } from '@/stores/auth';
import { useUiStore } from '@/stores/ui';
import AppModal from '@/components/AppModal.vue';
import SkeletonLoader from '@/components/SkeletonLoader.vue';

const authStore = useAuthStore();
const uiStore = useUiStore();
const projects = ref([]);
const loading = ref(true);
const newProject = ref({ name: '', description: '' });
const showCreateModal = ref(false);

const canCreateProjects = computed(() => {
    const role = authStore.user?.role?.name;
    return role === 'superadmin' || role === 'manager';
});

const fetchProjects = async () => {
  try {
    const response = await apiClient.get('/projects/');
    projects.value = response.data;
  } catch (error) {
    console.error('Failed to fetch projects:', error);
    uiStore.showToast('Failed to load projects.', 'error');
  } finally {
    loading.value = false;
  }
};

const createProject = async () => {
  try {
    const response = await apiClient.post('/projects/', newProject.value);
    projects.value.unshift(response.data);
    newProject.value = { name: '', description: '' };
    showCreateModal.value = false;
    uiStore.showToast('Project created successfully!');
  } catch (error)
 {
    console.error('Failed to create project:', error);
    uiStore.showToast('Failed to create project.', 'error');
  }
};

const getInitials = (email) => {
  if(!email) return '';
  const parts = email.split('@')[0].replace(/[^a-zA-Z]/g, ' ').split(' ');
  if (parts.length > 1 && parts[0] && parts[parts.length - 1]) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
  return email.substring(0, 2).toUpperCase();
};

const getAvatarColor = (email) => {
  if(!email) return '#cccccc';
  const colors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e', '#14b8a6', '#06b6d4', '#3b82f6', '#8b5cf6', '#d946ef'];
  let hash = 0;
  for (let i = 0; i < email.length; i++) {
    hash = email.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
};

onMounted(fetchProjects);
</script>