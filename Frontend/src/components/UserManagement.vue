<template>
  <div class="card full-height-card">
    <div class="card-header">
      <h4 class="card-title"><i class="fa-solid fa-users me-2"></i> User Management</h4>
    </div>
    <SkeletonLoader v-if="loading" type="list" :count="5" />
    <div v-else class="table-responsive">
      <table class="table admin-user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>User Email</th>
            <th>Current Role</th>
            <th>Change Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>
              <span class="user-id-badge">{{ user.id }}</span>
            </td>
            <td>{{ user.email }}</td>
            <td><span class="badge" :class="getRoleClass(user.role.name)">{{ user.role.name }}</span></td>
            <td>
              <div class="select-wrapper">
                  <select @change="updateRole(user.id, $event.target.value)" :disabled="user.id === authStore.user.id">
                      <option v-for="role in allRoles" :key="role.id" :value="role.id" :selected="user.role.id === role.id">
                          {{ role.name }}
                      </option>
                  </select>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api';
import { useAuthStore } from '@/stores/auth';
import { useUiStore } from '@/stores/ui';
import SkeletonLoader from '@/components/SkeletonLoader.vue';

const users = ref([]);
const allRoles = ref([]);
const loading = ref(true);
const authStore = useAuthStore();
const uiStore = useUiStore();

const fetchUsersAndRoles = async () => {
  try {
    const [usersRes, rolesRes] = await Promise.all([
      apiClient.get('/users/'),
      apiClient.get('/admin/roles')
    ]);
    users.value = usersRes.data;
    allRoles.value = rolesRes.data;
  } catch (error) {
    uiStore.showToast('Failed to load admin data.', 'error');
  } finally {
    loading.value = false;
  }
};

const updateRole = async (userId, roleId) => {
  try {
    const response = await apiClient.put(`/admin/users/${userId}/role/${roleId}`);
    const updatedUserIndex = users.value.findIndex(u => u.id === userId);
    if (updatedUserIndex !== -1) {
      users.value[updatedUserIndex] = response.data;
    }
    uiStore.showToast("User's role updated successfully!");
  } catch (error) {
    uiStore.showToast('Could not update role.', 'error');
    fetchUsersAndRoles();
  }
};

const getRoleClass = (roleName) => ({
  'bg-danger': roleName === 'superadmin',
  'bg-success': roleName === 'manager',
  'bg-info': roleName === 'member',
});

onMounted(fetchUsersAndRoles);
</script>