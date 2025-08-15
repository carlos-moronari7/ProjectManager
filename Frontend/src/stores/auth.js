import { defineStore } from 'pinia';
import apiClient from '@/api';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
        isAdmin: (state) => state.user?.role?.name === 'superadmin',
    },
    actions: {
        async login(email, password) {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);
            try {
                const response = await apiClient.post('/token', formData, {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                });
                this.token = response.data.access_token;
                localStorage.setItem('token', this.token);
                
                await this.fetchUser();
                
                router.push('/');
            } catch (error) {
                this.logout();
                throw new Error('Login failed. Please check credentials.');
            }
        },
        async fetchUser() {
            if (!this.token) return;
            try {
                const response = await apiClient.get('/users/me/');
                this.user = response.data;
                localStorage.setItem('user', JSON.stringify(this.user));
            } catch (error) {
                this.logout();
            }
        },
        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            router.push('/login');
        },
    },
});