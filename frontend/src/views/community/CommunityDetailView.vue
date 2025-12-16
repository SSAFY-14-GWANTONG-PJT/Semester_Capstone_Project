<template>
  <div class="detail-page">
    <button @click="goBack">← 목록</button>
    <h2>게시글 상세: {{ postId }}</h2>

    <!-- TODO: 게시글 상세 영역 -->
    <!-- TODO: 댓글 목록 + 작성 영역 -->
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const postId = route.params.postId;

const goBack = () => router.push("/community");
</script>
