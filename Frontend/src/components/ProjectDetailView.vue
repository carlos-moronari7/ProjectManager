<template>
  <div>
    <ProjectHeader />
    
    <div class="project-nav">
      <button v-for="tab in tabs" :key="tab.id" 
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id">
        <i :class="tab.icon"></i> {{ tab.name }}
      </button>
    </div>

    <div class="project-content">
      <div v-if="activeTab === 'tasks'">
        <div class="list-header">
            <h4><i class="fa-solid fa-columns icon"></i>Tasks Board</h4>
            <button @click="showCreateModal = true" class="btn btn-primary btn-sm">
                <i class="fa-solid fa-plus me-1"></i> New Task
            </button>
        </div>
        <SkeletonLoader v-if="projectStore.loading.tasks" type="list" :count="5" />
        <div v-else class="kanban-board">
            <TaskColumn title="To Do" status="pending" :tasks="tasksByStatus.pending || []" @task-click="openTaskDetail" />
            <TaskColumn title="In Progress" status="in_progress" :tasks="tasksByStatus.in_progress || []" @task-click="openTaskDetail" />
            <TaskColumn title="Completed" status="completed" :tasks="tasksByStatus.completed || []" @task-click="openTaskDetail" />
        </div>
      </div>

      <div v-if="activeTab === 'members'">
        <MembersList />
      </div>
      <div v-if="activeTab === 'files'">
        <FileList />
      </div>
      <div v-if="activeTab === 'milestones'">
        <MilestonesTab />
      </div>
    </div>
    
    <CreateTaskModal v-if="showCreateModal" @close="showCreateModal = false" />
    <TaskDetailModal v-if="selectedTask" :task="selectedTask" @close="selectedTask = null" />

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectStore } from '@/stores/project';
import ProjectHeader from '@/components/ProjectHeader.vue';
import MembersList from '@/components/MembersList.vue';
import FileList from '@/components/FileList.vue';
import MilestonesTab from '@/components/project/MilestonesTab.vue';
import TaskColumn from '@/components/TaskColumn.vue';
import CreateTaskModal from '@/components/CreateTaskModal.vue';
import TaskDetailModal from '@/components/project/TaskDetailModal.vue';
import SkeletonLoader from '@/components/SkeletonLoader.vue';

const route = useRoute();
const projectStore = useProjectStore();
const projectId = route.params.id;
const activeTab = ref('tasks');
const showCreateModal = ref(false);
const selectedTask = ref(null);

const tabs = [
  { id: 'tasks', name: 'Board', icon: 'fa-solid fa-columns' },
  { id: 'milestones', name: 'Milestones', icon: 'fa-solid fa-flag-checkered' },
  { id: 'members', name: 'Members', icon: 'fa-solid fa-users' },
  { id: 'files', name: 'Files', icon: 'fa-solid fa-folder-open' },
];

const tasksByStatus = computed(() => {
    return projectStore.tasks.reduce((acc, task) => {
        const status = task.status || 'pending';
        if (!acc[status]) acc[status] = [];
        acc[status].push(task);
        return acc;
    }, {});
});

const openTaskDetail = (task) => {
    selectedTask.value = task;
};

onMounted(() => {
  projectStore.$reset();
  projectStore.fetchProject(projectId);
  projectStore.fetchProjectData(projectId);
});
</script>