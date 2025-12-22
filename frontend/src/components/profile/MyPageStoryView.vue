<template>
  <div class="story-item">
    <span class="emoji">📔</span>
    <div class="story-info">
      <p class="title">{{ story.title }}</p>
      <p class="date">{{ story.created_at.slice(0, 10) }}</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  story: Object
});
</script>

<style scoped>
.story-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f9fafb;
  border-radius: 20px;
}
.story-item .emoji { font-size: 1.5rem; }
.story-item .title { font-weight: 800; color: var(--text); margin: 0; }
.story-item .date { font-size: 0.85rem; color: #999; margin: 0; }
</style>