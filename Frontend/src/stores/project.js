import { defineStore } from 'pinia';
import apiClient from '@/api';
import { useUiStore } from './ui';

export const useProjectStore = defineStore('project', {
  state: () => ({
    project: null,
    tasks: [],
    members: [],
    files: [],
    allUsers: [],
    allRoles: [],
    loading: {
      details: false,
      tasks: false,
      members: false,
      files: false,
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
        console.error('Failed to fetch project details', error);
        useUiStore().showToast('Failed to load project details.', 'error');
      } finally {
        this.loading.details = false;
      }
    },
    async fetchProjectData(projectId) {
        this.loading.tasks = true;
        this.loading.members = true;
        this.loading.files = true;
        try {
            const [tasksRes, membersRes, filesRes, usersRes, rolesRes] = await Promise.all([
                apiClient.get(`/projects/${projectId}/tasks/`),
                apiClient.get(`/projects/${projectId}/members`),
                apiClient.get(`/projects/${projectId}/files`),
                apiClient.get('/users/'),
                apiClient.get('/admin/roles'),
            ]);
            this.tasks = tasksRes.data;
            this.members = membersRes.data;
            this.files = filesRes.data;
            this.allUsers = usersRes.data;
            this.allRoles = rolesRes.data;
        } catch (error) {
            console.error('Failed to fetch project data', error);
            useUiStore().showToast('Failed to load project data.', 'error');
        } finally {
            this.loading.tasks = false;
            this.loading.members = false;
            this.loading.files = false;
        }
    },
    async createTask(projectId, taskData) {
        try {
            const response = await apiClient.post(`/projects/${projectId}/tasks/`, taskData);
            this.tasks.push(response.data);
            useUiStore().showToast('Task created successfully!');
        } catch (error) {
            console.error('Failed to create task', error);
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
            console.error('Failed to add member', error);
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
            console.error('Failed to upload file', error);
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
            console.error('Failed to get download URL', error);
            useUiStore().showToast('Could not get download link.', 'error');
        }
    }
  },
});