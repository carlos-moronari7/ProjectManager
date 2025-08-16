<template>
  <div class="login-card">
    <div class="login-header">
      <i class="fa-solid fa-rocket fa-2x logo"></i>
      <h1>ProjectFlow</h1>
      <p>Sign in to your account</p>
    </div>
    <div v-if="errorMsg" class="error-banner">{{ errorMsg }}</div>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="email">Email Address</label>
        <input type="email" id="email" v-model="email" placeholder="e.g., you@example.com" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="loading">
        <span v-if="loading" class="spinner"></span>
        <span v-else>Sign In</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const email = ref('manager@example.com');
const password = ref('password');
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