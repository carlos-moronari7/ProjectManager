<template>
  <div>
    <div class="list-header">
      <h4><i class="fa-solid fa-flag-checkered icon"></i>Milestones</h4>
      <button class="btn btn-primary btn-sm">
        <i class="fa-solid fa-plus me-1"></i> New Milestone
      </button>
    </div>

    <SkeletonLoader v-if="projectStore.loading.milestones" type="list" :count="3" />
    <div v-else-if="projectStore.milestones.length > 0" class="milestone-list">
        <div v-for="milestone in projectStore.milestones" :key="milestone.id" class="card milestone-card">
            <h5>{{ milestone.name }}</h5>
            <p>{{ milestone.description }}</p>
            <div class="milestone-footer">
                <span>Due: {{ milestone.due_date || 'N/A' }}</span>
                <span class="badge" :class="`bg-info`">{{ milestone.status }}</span>
            </div>
        </div>
    </div>
    <div v-else class="empty-state">
      <p>No milestones have been defined for this project yet.</p>
    </div>
  </div>
</template>

<script setup>
import { useProjectStore } from '@/stores/project';
import SkeletonLoader from '@/components/SkeletonLoader.vue';

const projectStore = useProjectStore();
</script>