<template>
  <AppModal title="Create New Task" @close="$emit('close')">
    <form @submit.prevent="submitTask">
      <div class="form-group">
        <label for="title">Task Title</label>
        <input type="text" id="title" v-model="task.title" required />
      </div>
      <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" v-model="task.description" rows="3"></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
            <label for="assignee">Assign To</label>
            <select id="assignee" v-model="task.assignee_id">
                <option :value="null">Unassigned</option>
                <option v-for="member in projectStore.members" :key="member.user.id" :value="member.user.id">
                    {{ member.user.email }}
                </option>
            </select>
        </div>
        <div class="form-group">
            <label for="due_date">Due Date</label>
            <input type="date" id="due_date" v-model="task.due_date" />
        </div>
      </div>
      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
        <button type="submit" class="btn btn-primary">Create Task</button>
      </div>
    </form>
  </AppModal>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import AppModal from './AppModal.vue';

const emit = defineEmits(['close']);
const route = useRoute();
const projectStore = useProjectStore();
const projectId = route.params.id;

const task = ref({
  title: '',
  description: '',
  assignee_id: null,
  due_date: null,
});

const submitTask = async () => {
  await projectStore.createTask(projectId, task.value);
  emit('close');
};
</script>