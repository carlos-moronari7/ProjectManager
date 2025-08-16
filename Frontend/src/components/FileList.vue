<template>
  <div>
    <div class="list-header">
      <h4><i class="fa-solid fa-folder-open icon"></i>Project Files</h4>
      <button @click="showUploadModal = true" class="btn btn-primary btn-sm">
        <i class="fa-solid fa-upload me-1"></i> Upload File
      </button>
    </div>

    <SkeletonLoader v-if="projectStore.loading.files" type="list" :count="3" />
    <div v-else-if="projectStore.files.length > 0" class="file-list">
      <div v-for="file in projectStore.files" :key="file.id" class="file-item">
        <div class="file-info">
          <i class="fa-solid fa-file me-2"></i>
          <span class="file-name">{{ file.file_name }}</span>
          <span class="file-meta">{{ (file.file_size / 1024).toFixed(1) }} KB</span>
        </div>
        <button @click="projectStore.getDownloadUrl(file.id)" class="btn btn-outline-secondary btn-sm">
          <i class="fa-solid fa-download"></i>
        </button>
      </div>
    </div>
    <div v-else class="empty-state">
      <p>No files have been uploaded to this project yet.</p>
    </div>

    <AppModal v-if="showUploadModal" title="Upload File" @close="showUploadModal = false">
        <form @submit.prevent="handleUpload">
            <div class="form-group">
                <label for="file-upload">Select a file</label>
                <input type="file" id="file-upload" @change="onFileSelected" required />
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" @click="showUploadModal = false">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="!selectedFile">Upload</button>
            </div>
        </form>
    </AppModal>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import SkeletonLoader from './SkeletonLoader.vue';
import AppModal from './AppModal.vue';

const projectStore = useProjectStore();
const route = useRoute();
const projectId = route.params.id;

const showUploadModal = ref(false);
const selectedFile = ref(null);

const onFileSelected = (event) => {
  selectedFile.value = event.target.files[0];
};

const handleUpload = async () => {
  if (!selectedFile.value) return;
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  await projectStore.uploadFile(projectId, formData);
  showUploadModal.value = false;
  selectedFile.value = null;
};
</script>