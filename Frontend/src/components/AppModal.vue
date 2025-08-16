<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-content" :style="{ maxWidth: width }">
      <header class="modal-header">
        <h3>{{ title }}</h3>
        <button @click="$emit('close')" class="close-button">&times;</button>
      </header>
      <section class="modal-body">
        <slot></slot>
      </section>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  width: {
    type: String,
    default: '500px',
  },
});
defineEmits(['close']);
</script>