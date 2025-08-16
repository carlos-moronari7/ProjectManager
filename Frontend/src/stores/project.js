import { defineStore } from 'pinia';
import apiClient from '@/api';
import { useUiStore } from './ui';

export const useProjectStore = defineStore('project', {
  state: () => ({
    project: null,
    tasks: [],
    members: [],
    files: [],
    milestones: [],
    allUsers: [],
    allRoles: [],
    loading: {
      details: false,
      tasks: false,
      members: false,
      files: false,
      milestones: false,
    },
  }),
  getters: {
    projectRoles: (state) => state.allRoles.filter(r => r.name !== 'superadmin'),
    availableUsers: (state) => {
      const memberIds = new Set(state.members.map(pm => pm.user.id));
      return state.allUsers.filter(user => !memberIds.has(user.id));
    },
  },
  actions: {
    async fetchProject(projectId) {
      this.loading.details = true;
      try {
        const response = await apiClient.get(`/projects/${projectId}`);
        this.project = response.data;
      } catch (error) {
        useUiStore().showToast('Failed to load project details.', 'error');
      } finally {
        this.loading.details = false;
      }
    },
    async updateTaskStatus(taskId, newStatus) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) return;

        const originalStatus = task.status;
        task.status = newStatus;

        try {
            const payload = { ...task, status: newStatus };
            delete payload.id;
            delete payload.project_id;
            delete payload.created_at;
            delete payload.files;

            await apiClient.put(`/tasks/${taskId}`, payload);
            
        } catch (error) {
            task.status = originalStatus; // Revert on failure
            useUiStore().showToast('Failed to update task status.', 'error');
        }
    },
    async fetchProjectData(projectId) {
        const dataTypes = ['tasks', 'members', 'files', 'milestones'];
        dataTypes.forEach(type => this.loading[type] = true);
        
        try {
            const [tasksRes, membersRes, filesRes, usersRes, rolesRes, milestonesRes] = await Promise.all([
                apiClient.get(`/projects/${projectId}/tasks/`),
                apiClient.get(`/projects/${projectId}/members`),
                apiClient.get(`/projects/${projectId}/files`),
                apiClient.get('/users/'),
                apiClient.get('/admin/roles'),
                apiClient.get(`/projects/${projectId}/milestones/`),
            ]);
            this.tasks = tasksRes.data;
            this.members = membersRes.data;
            this.files = filesRes.data;
            this.allUsers = usersRes.data;
            this.allRoles = rolesRes.data;
            this.milestones = milestonesRes.data;
        } catch (error) {
            useUiStore().showToast('Failed to load project data.', 'error');
        } finally {
            dataTypes.forEach(type => this.loading[type] = false);
        }
    },
    async createTask(projectId, taskData) {
        try {
            const response = await apiClient.post(`/projects/${projectId}/tasks/`, taskData);
            this.tasks.push(response.data);
            useUiStore().showToast('Task created successfully!');
        } catch (error) {
            useUiStore().showToast(error.response?.data?.detail || 'Failed to create task.', 'error');
        }
    },
    async addMember(projectId, memberData) {
        try {
            await apiClient.post(`/projects/${projectId}/members`, {
                user_id: memberData.userId,
                role_id: memberData.roleId,
            });
            await this.fetchProjectData(projectId);
            useUiStore().showToast('Member added successfully!');
        } catch (error) {
            useUiStore().showToast(error.response?.data?.detail || 'Failed to add member.', 'error');
        }
    },
    async uploadFile(projectId, formData) {
        this.loading.files = true;
        try {
            const response = await apiClient.post(`/projects/${projectId}/files`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            this.files.push(response.data);
            useUiStore().showToast('File uploaded successfully!');
        } catch (error) {
            useUiStore().showToast('Failed to upload file.', 'error');
        } finally {
            this.loading.files = false;
        }
    },
    async getDownloadUrl(fileId) {
        try {
            const response = await apiClient.get(`/files/${fileId}/download`);
            window.open(response.data.url, '_blank');
        } catch (error) {
            useUiStore().showToast('Could not get download link.', 'error');
        }
    }
  },
});