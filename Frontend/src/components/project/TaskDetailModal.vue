<template>
  <AppModal :title="task.title" @close="$emit('close')" width="700px">
    <div class="task-detail-layout">
        <div class="task-detail-main">
            <h4>Description</h4>
            <p>{{ task.description || 'No description provided.' }}</p>
            
            <div v-if="task.files.length > 0">
                <h4><i class="fa-solid fa-paperclip"></i> Attachments</h4>
                <div class="attachment-list">
                    <div v-for="file in task.files" :key="file.id" class="attachment-item">
                        <span>{{ file.file_name }}</span>
                        <button class="btn btn-secondary btn-sm" @click="projectStore.getDownloadUrl(file.id)">Download</button>
                    </div>
                </div>
            </div>

            <h4><i class="fa-solid fa-comments"></i> Activity</h4>
            <div class="comment-section">
            </div>
        </div>
        <div class="task-detail-sidebar">
            <div class="detail-block">
                <label>Status</label>
                <p>{{ task.status }}</p>
            </div>
            <div class="detail-block">
                <label>Assignee</label>
                <p>{{ getAssignee(task.assignee_id)?.user.email || 'Unassigned' }}</p>
            </div>
            <div class="detail-block">
                <label>Priority</label>
                <p>{{ task.priority }}</p>
            </div>
             <div class="detail-block">
                <label>Due Date</label>
                <p>{{ task.due_date || 'Not set' }}</p>
            </div>
        </div>
    </div>
  </AppModal>
</template>

<script setup>
import { useProjectStore } from '@/stores/project';
import AppModal from '../AppModal.vue';

const props = defineProps({
  task: { type: Object, required: true }
});
defineEmits(['close']);

const projectStore = useProjectStore();

const getAssignee = (assigneeId) => {
    if (!assigneeId) return null;
    return projectStore.members.find(m => m.user.id === assigneeId);
};
</script>