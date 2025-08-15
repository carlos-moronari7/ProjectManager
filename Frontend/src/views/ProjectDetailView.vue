<template>
  <div v-if="project">
    <h1 class="mb-4"><i class="fa-solid fa-briefcase text-primary me-2"></i>{{ project.name }}</h1>
    
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'tasks' }" @click="activeTab = 'tasks'">
          <i class="fa-solid fa-list-check me-1"></i> Tasks
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'members' }" @click="activeTab = 'members'">
          <i class="fa-solid fa-users me-1"></i> Members
          <span class="badge rounded-pill bg-secondary ms-1">{{ projectMembers.length }}</span>
        </a>
      </li>
    </ul>

    <!-- TASKS TAB -->
    <div v-if="activeTab === 'tasks'">
      <div class="alert alert-info"><i class="fa-solid fa-wrench me-2"></i> Task management interface coming soon!</div>
    </div>

    <!-- MEMBERS TAB -->
    <div v-if="activeTab === 'members'">
      <div class="row">
        <div class="col-md-7">
          <div class="card">
            <div class="card-header">Current Members</div>
            <ul class="list-group list-group-flush">
              <li v-for="member in projectMembers" :key="member.user.id" class="list-group-item d-flex justify-content-between align-items-center">
                {{ member.user.email }}
                <span class="badge" :class="getRoleClass(member.role.name)">{{ member.role.name }}</span>
              </li>
            </ul>
          </div>
        </div>
        <div class="col-md-5">
          <div class="card bg-light">
            <div class="card-body">
              <h5 class="card-title"><i class="fa-solid fa-user-plus me-1"></i> Add Member</h5>
              <form @submit.prevent="addMember">
                <div class="mb-3">
                  <label class="form-label">User</label>
                  <select class="form-select" v-model="newMember.userId">
                    <option disabled value="">Select a user to add...</option>
                    <option v-for="user in availableUsers" :key="user.id" :value="user.id">{{ user.email }}</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label">Project Role</label>
                  <select class="form-select" v-model="newMember.roleId">
                    <option v-for="role in projectRoles" :key="role.id" :value="role.id">{{ role.name }}</option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary w-100">Add to Project</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import apiClient from '@/api';

const route = useRoute();
const projectId = route.params.id;
const project = ref(null);
const activeTab = ref('members');
const allUsers = ref([]);
const allRoles = ref([]);
const projectMembers = ref([]);
const newMember = ref({ userId: '', roleId: '' });

const projectRoles = computed(() => allRoles.value.filter(r => r.name !== 'superadmin'));
const availableUsers = computed(() => {
  const memberIds = new Set(projectMembers.value.map(pm => pm.user.id));
  return allUsers.value.filter(user => !memberIds.has(user.id));
});

const fetchAllData = async () => {
  try {
    const [projRes, usersRes, rolesRes, membersRes] = await Promise.all([
      apiClient.get(`/projects/${projectId}`),
      apiClient.get('/users/'),
      apiClient.get('/admin/roles'),
      apiClient.get(`/projects/${projectId}/members`)
    ]);
    project.value = projRes.data;
    allUsers.value = usersRes.data;
    allRoles.value = rolesRes.data;
    projectMembers.value = membersRes.data;
    // Set a default role for the form
    const defaultRole = projectRoles.value.find(r => r.name === 'member');
    if (defaultRole) newMember.value.roleId = defaultRole.id;
  } catch (error) {
    console.error("Failed to load project data:", error);
  }
};

const addMember = async () => {
  if (!newMember.value.userId) return;
  try {
    await apiClient.post(`/projects/${projectId}/members`, {
      user_id: newMember.value.userId,
      role_id: newMember.value.roleId
    });
    await fetchAllData(); // Refresh all data
    newMember.value.userId = '';
  } catch (error) {
    alert(error.response?.data?.detail || "Failed to add member.");
  }
};

const getRoleClass = (roleName) => ({
  'bg-success': roleName === 'manager',
  'bg-info text-dark': roleName === 'member',
});

onMounted(fetchAllData);
</script>

<style scoped>
.nav-link { cursor: pointer; }
</style>