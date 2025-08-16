<template>
  <div class="task-column">
    <div class="column-header">
      <span class="status-dot" :style="{ backgroundColor: statusColor }"></span>
      <h5 class="column-title">{{ title }}</h5>
      <span class="task-count">{{ tasks.length }}</span>
    </div>
    <div class="task-list-container">
      <div v-for="task in tasks" :key="task.id" class="task-item-card">
        <div class="task-card-header">
          <h6 class="task-title">{{ task.title }}</h6>
          <span class="priority-dot" :class="`priority-${task.priority}`" :title="`Priority: ${task.priority}`"></span>
        </div>
        <p class="task-description">{{ task.description || 'No description' }}</p>
        <div class="task-card-footer">
          <span class="task-meta-item" v-if="task.due_date">
            <i class="fa-regular fa-calendar"></i> {{ task.due_date }}
          </span>
          <div class="assignee-avatar" v-if="getAssignee(task.assignee_id)" :style="{ backgroundColor: getAvatarColor(getAssignee(task.assignee_id).user.email) }" :title="getAssignee(task.assignee_id).user.email">
            {{ getInitials(getAssignee(task.assignee_id).user.email) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useProjectStore } from '@/stores/project';

const props = defineProps({
  title: String,
  status: String,
  tasks: Array,
});

const projectStore = useProjectStore();

const statusColor = computed(() => {
  const colors = {
    pending: '#f97316',
    'in_progress': '#3b82f6',
    completed: '#22c55e',
  };
  return colors[props.status] || '#6b7280';
});

const getAssignee = (assigneeId) => {
    if (!assigneeId) return null;
    return projectStore.members.find(m => m.user.id === assigneeId);
};

const getInitials = (email) => {
  const parts = email.split('@')[0].replace(/[^a-zA-Z]/g, ' ').split(' ');
  if (parts.length > 1) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  return email.substring(0, 2).toUpperCase();
};

const getAvatarColor = (email) => {
  const colors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e', '#14b8a6', '#06b6d4', '#3b82f6', '#8b5cf6', '#d946ef'];
  let hash = 0;
  for (let i = 0; i < email.length; i++) { hash = email.charCodeAt(i) + ((hash << 5) - hash); }
  return colors[Math.abs(hash) % colors.length];
};
</script>