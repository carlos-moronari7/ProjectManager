<template>
  <div class="card full-height-card">
    <div class="card-header">
      <h4 class="card-title"><i class="fa-solid fa-chart-line me-2"></i> Team Workload Report</h4>
    </div>
    <SkeletonLoader v-if="loading" type="list" :count="5" />
    <div v-else class="table-responsive">
      <table class="table admin-report-table">
        <thead>
          <tr>
            <th>Team Member</th>
            <th>Open Tasks</th>
            <th>Workload</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="member in workloadData" :key="member.assignee_id">
            <td>{{ member.email }}</td>
            <td>
              <span class="task-count-badge">{{ member.open_tasks_count }}</span>
            </td>
            <td>
              <div class="workload-bar-container">
                <div class="workload-bar" :style="{ width: getWorkloadPercentage(member.open_tasks_count) + '%' }"></div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import apiClient from '@/api';
import { useUiStore } from '@/stores/ui';
import SkeletonLoader from '@/components/SkeletonLoader.vue';

const loading = ref(true);
const workloadData = ref([]);
const uiStore = useUiStore();

const maxTasks = computed(() => {
    if (workloadData.value.length === 0) return 1;
    return Math.max(...workloadData.value.map(m => m.open_tasks_count), 5);
});

const getWorkloadPercentage = (taskCount) => {
    return (taskCount / maxTasks.value) * 100;
};

onMounted(async () => {
    try {
        const response = await apiClient.get('/reports/team_workload');
        workloadData.value = response.data;
    } catch (error) {
        uiStore.showToast('Failed to load workload report.', 'error');
    } finally {
        loading.value = false;
    }
});
</script>