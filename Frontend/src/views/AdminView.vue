<template>
  <div>
    <h1 class="mb-4"><i class="fa-solid fa-user-shield me-2"></i> Admin Panel: User Management</h1>
    <div v-if="loading" class="text-center"><div class="spinner-border"></div></div>
    <div v-else class="card">
      <div class="card-body">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Email</th>
              <th>Current Role</th>
              <th>Change Role</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.email }}</td>
              <td><span class="badge" :class="getRoleClass(user.role.name)">{{ user.role.name }}</span></td>
              <td>
                <select class="form-select w-auto" @change="updateRole(user.id, $event.target.value)" :disabled="user.id === authStore.user.id">
                  <option v-for="role in allRoles" :key="role.id" :value="role.id" :selected="user.role.id === role.id">
                    {{ role.name }}
                  </option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api';
import { useAuthStore } from '@/stores/auth';

const users = ref([]);
const allRoles = ref([]);
const loading = ref(true);
const authStore = useAuthStore();

const fetchUsersAndRoles = async () => {
  try {
    const [usersRes, rolesRes] = await Promise.all([
      apiClient.get('/users/'),
      apiClient.get('/admin/roles')
    ]);
    users.value = usersRes.data;
    allRoles.value = rolesRes.data;
  } catch (error) {
    console.error(error);
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
  } catch (error) {
    console.error("Failed to update role", error);
    alert('Could not update role.');
  }
};

const getRoleClass = (roleName) => ({
  'bg-danger': roleName === 'superadmin',
  'bg-success': roleName === 'manager',
  'bg-secondary': roleName === 'member',
});

onMounted(fetchUsersAndRoles);
</script>