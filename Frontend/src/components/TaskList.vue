<template>
  <div>
    <div class="list-header">
      <h4><i class="fa-solid fa-list-check icon"></i>Tasks</h4>
      <button @click="showCreateModal = true" class="btn btn-primary btn-sm">
        <i class="fa-solid fa-plus me-1"></i> New Task
      </button>
    </div>
    
    <SkeletonLoader v-if="projectStore.loading.tasks" type="list" :count="5" />
    <div v-else-if="projectStore.tasks.length > 0" class="task-list">
        <div v-for="task in projectStore.tasks" :key="task.id" class="task-item card">
            <h5>{{ task.title }}</h5>
            <p>{{ task.description || 'No description provided.' }}</p>
            <div class="task-meta">
                <span><i class="fa-solid fa-flag"></i> {{ task.status }}</span>
                <span><i class="fa-solid fa-user"></i> {{ getAssigneeEmail(task.assignee_id) }}</span>
                <span><i class="fa-solid fa-calendar-days"></i> {{ task.due_date || 'No due date' }}</span>
            </div>
        </div>
    </div>
    <div v-else class="empty-state">
      <p>No tasks have been created for this project yet.</p>
    </div>

    <CreateTaskModal v-if="showCreateModal" @close="showCreateModal = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useProjectStore } from '@/stores/project';
import SkeletonLoader from './SkeletonLoader.vue';
import CreateTaskModal from './CreateTaskModal.vue';

const projectStore = useProjectStore();
const showCreateModal = ref(false);

const getAssigneeEmail = (assigneeId) => {
    if (!assigneeId) return 'Unassigned';
    const member = projectStore.members.find(m => m.user.id === assigneeId);
    return member ? member.user.email : 'Unknown User';
}
</script>