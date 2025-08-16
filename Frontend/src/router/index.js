import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AdminView from '../views/AdminView.vue'
import UserManagement from '../components/UserManagement.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/projects/:id',
      name: 'project-detail',
      component: () => import('@/views/ProjectDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      component: AdminView,
      meta: { requiresAuth: true, requiresAdmin: true },
      redirect: '/admin/users', // Redirect /admin to the default users section
      children: [
        {
          path: 'users',
          name: 'admin-users',
          component: UserManagement
        },
        // add more admin sections here later
        // { path: 'roles', name: 'admin-roles', component: () => import(...) },
      ]
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Fetch user if we have a token but no user object yet
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser();
  }
  
  const requiresAuth = to.meta.requiresAuth;
  const requiresAdmin = to.meta.requiresAdmin;

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' });
  } else if (requiresAdmin && (!authStore.user || !authStore.isAdmin)) {
    // Check if user object exists before checking role
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router