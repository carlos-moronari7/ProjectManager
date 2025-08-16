<template>
  <div class="task-column">
    <div class="column-header">
      <span class="status-dot" :style="{ backgroundColor: statusColor }"></span>
      <h5 class="column-title">{{ title }}</h5>
      <span class="task-count">{{ taskModels.length }}</span>
    </div>
    <!-- The fix is wrapping the draggable component in a div -->
    <div class="task-list-wrapper">
        <draggable
          class="task-list-container"
          v-model="taskModels"
          group="tasks"
          item-key="id"
          :animation="200"
          ghost-class="ghost"
          drag-class="drag"
          @change="onDragChange"
        >
          <template #item="{ element }">
            <div class="task-item-card" @click="$emit('task-click', element)">
              <div class="task-card-header">
                <h6 class="task-title">{{ element.title }}</h6>
                <span class="priority-dot" :class="`priority-${element.priority}`" :title="`Priority: ${element.priority}`"></span>
              </div>
              <p class="task-description">{{ element.description || 'No description' }}</p>
              <div class="task-card-footer">
                <div class="task-meta-group">
                  <span class="task-meta-item" v-if="element.due_date">
                      <i class="fa-regular fa-calendar"></i> {{ element.due_date }}
                  </span>
                  <span class="task-meta-item" v-if="element.files.length > 0">
                      <i class="fa-solid fa-paperclip"></i> {{ element.files.length }}
                  </span>
                </div>
                <div class="assignee-avatar" v-if="getAssignee(element.assignee_id)" :style="{ backgroundColor: getAvatarColor(getAssignee(element.assignee_id).user.email) }" :title="getAssignee(element.assignee_id).user.email">
                  {{ getInitials(getAssignee(element.assignee_id).user.email) }}
                </div>
              </div>
            </div>
          </template>
        </draggable>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { useProjectStore } from '@/stores/project';
import draggable from 'vuedraggable';

const props = defineProps({
  title: String,
  status: String,
  tasks: Array,
});
const emit = defineEmits(['task-click', 'task-moved']);

const taskModels = ref([...props.tasks]);

watch(() => props.tasks, (newTasks) => {
    taskModels.value = [...newTasks];
});

const projectStore = useProjectStore();

const onDragChange = (event) => {
    if (event.added) {
        emit('task-moved', {
            taskId: event.added.element.id,
            newStatus: props.status
        });
    }
};

const statusColor = computed(() => {
  const colors = { pending: '#f97316', 'in_progress': '#3b82f6', completed: '#22c55e' };
  return colors[props.status] || '#6b7280';
});

const getAssignee = (assigneeId) => {
    if (!assigneeId) return null;
    return projectStore.members.find(m => m.user.id === assigneeId);
};

const getInitials = (email) => {
  if (!email) return '';
  const parts = email.split('@')[0].replace(/[^a-zA-Z]/g, ' ').split(' ');
  if (parts.length > 1) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  return email.substring(0, 2).toUpperCase();
};

const getAvatarColor = (email) => {
  if (!email) return '#cccccc';
  const colors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e', '#14b8a6', '#06b6d4', '#3b82f6', '#8b5cf6', '#d946ef'];
  let hash = 0;
  for (let i = 0; i < email.length; i++) { hash = email.charCodeAt(i) + ((hash << 5) - hash); }
  return colors[Math.abs(hash) % colors.length];
};
</script>