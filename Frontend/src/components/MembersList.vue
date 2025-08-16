<template>
  <div>
    <div class="list-header">
      <h4><i class="fa-solid fa-users icon"></i>Project Members</h4>
      <button @click="showAddModal = true" class="btn btn-primary btn-sm">
        <i class="fa-solid fa-user-plus me-1"></i> Add Member
      </button>
    </div>

    <SkeletonLoader v-if="projectStore.loading.members" type="list" :count="4" />
    <div v-else class="member-list">
      <div v-for="member in projectStore.members" :key="member.user.id" class="member-item">
        <div class="member-info">
          <i class="fa-solid fa-user-circle me-2"></i>
          <span>{{ member.user.email }}</span>
        </div>
        <span class="badge" :class="getRoleClass(member.role.name)">{{ member.role.name }}</span>
      </div>
    </div>

    <AppModal v-if="showAddModal" title="Add Member to Project" @close="showAddModal = false">
      <form @submit.prevent="handleAddMember">
        <div class="form-group">
            <label>User</label>
            <select v-model="newMember.userId" required>
                <option disabled value="">Select a user...</option>
                <option v-for="user in projectStore.availableUsers" :key="user.id" :value="user.id">
                    {{ user.email }}
                </option>
            </select>
        </div>
        <div class="form-group">
            <label>Project Role</label>
            <select v-model="newMember.roleId" required>
                <option v-for="role in projectStore.projectRoles" :key="role.id" :value="role.id">
                    {{ role.name }}
                </option>
            </select>
        </div>
        <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="showAddModal = false">Cancel</button>
            <button type="submit" class="btn btn-primary">Add Member</button>
        </div>
      </form>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import SkeletonLoader from './SkeletonLoader.vue';
import AppModal from './AppModal.vue';

const projectStore = useProjectStore();
const route = useRoute();
const projectId = route.params.id;

const showAddModal = ref(false);
const newMember = ref({ userId: '', roleId: '' });

const getRoleClass = (roleName) => ({
  'bg-success': roleName === 'manager',
  'bg-info': roleName === 'member',
});

const handleAddMember = async () => {
    await projectStore.addMember(projectId, newMember.value);
    showAddModal.value = false;
    newMember.value.userId = '';
};

onMounted(() => {
    const defaultRole = projectStore.projectRoles.find(r => r.name === 'member');
    if (defaultRole) newMember.value.roleId = defaultRole.id;
});
</script>