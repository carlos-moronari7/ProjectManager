import { defineStore } from 'pinia';
import { useToast } from 'vue-toastification';

export const useUiStore = defineStore('ui', {
  state: () => ({
    // other global UI states here, e.g. isSidebarOpen: true
  }),
  actions: {
    showToast(message, type = 'success') {
      const toast = useToast();
      toast[type](message);
    },
  },
});