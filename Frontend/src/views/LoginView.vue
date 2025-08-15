<template>
  <div class="col-md-4 col-lg-3">
    <div class="card shadow-lg border-0">
      <div class="card-body p-4">
        <div class="text-center mb-4">
          <i class="fa-solid fa-kanban fa-3x text-primary"></i>
          <h3 class="mt-2">ProjectFlow</h3>
          <p class="text-muted">Sign in to continue</p>
        </div>
        <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" class="form-control" v-model="email" required>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" v-model="password" required>
          </div>
          <div class="d-grid">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm"></span>
              <span v-else>Login</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const email = ref('');
const password = ref('');
const errorMsg = ref('');
const loading = ref(false);
const authStore = useAuthStore();

const handleLogin = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    await authStore.login(email.value, password.value);
  } catch (e) {
    errorMsg.value = e.message;
  } finally {
    loading.value = false;
  }
};
</script>