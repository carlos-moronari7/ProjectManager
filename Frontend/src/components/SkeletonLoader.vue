<template>
  <div>
    <div v-if="type === 'heading'" class="skeleton-heading">
      <div class="skeleton-line title"></div>
      <div class="skeleton-line subtitle"></div>
    </div>
    <div v-if="type === 'list'" class="skeleton-list">
      <div v-for="n in count" :key="n" class="skeleton-list-item">
        <div class="skeleton-line"></div>
      </div>
    </div>
    <div v-if="type === 'card'" class="skeleton-card-grid">
       <div v-for="n in count" :key="n" class="skeleton-card">
          <div class="skeleton-line" style="width: 60%;"></div>
          <div class="skeleton-line" style="width: 90%;"></div>
          <div class="skeleton-line" style="width: 80%;"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'list', // list, heading, card
  },
  count: {
    type: Number,
    default: 1,
  },
});
</script>