<template>
  <div class="project-header">
    <SkeletonLoader v-if="projectStore.loading.details" type="heading" />
    <div v-else-if="projectStore.project">
      <h1>
        <i class="fa-solid fa-briefcase icon"></i>
        {{ projectStore.project.name }}
      </h1>
      <p class="description">{{ projectStore.project.description }}</p>
    </div>
  </div>
</template>

<script setup>
import { useProjectStore } from '@/stores/project';
import SkeletonLoader from './SkeletonLoader.vue';

const projectStore = useProjectStore();
</script>