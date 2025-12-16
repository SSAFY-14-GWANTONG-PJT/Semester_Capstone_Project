<template>
  <div class="community-page">
    <header class="page-header">
      <h1>Community</h1>

      <div class="actions">
        <button @click="goWrite">글 작성</button>
      </div>
    </header>

    <section class="filters">
      <select v-model="filters.status" @change="fetchPosts">
        <option value="">전체</option>
        <option value="review">학습 후기</option>
        <option value="question">질문</option>
      </select>

      <select v-model="filters.sort" @change="fetchPosts">
        <option value="-created_at">최신순</option>
        <option value="created_at">오래된순</option>
      </select>
    </section>

    <main>
      <div v-if="loading">로딩중</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else-if="posts.length === 0">게시글이 없습니다.</div>

      <ul v-else class="post-list">
        <li v-for="post in posts" :key="post.id" class="post-card" @click="goDetail(post.id)">
          <h3>{{ post.title }}</h3>
          <p class="meta">
            작성자: {{ post.user }} · 좋아요: {{ post.like ?? 0 }}
          </p>
        </li>
      </ul>
    </main>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
// TODO: axios api 연결 전까지 더미 사용
// import { fetchPostList } from "@/services/communityApi";

const router = useRouter();

const posts = ref([]);
const loading = ref(false);
const error = ref("");

const filters = reactive({
  status: "",
  sort: "-created_at",
});

const fetchPosts = async () => {
  loading.value = true;
  error.value = "";
  try {
    // TODO: 백엔드 연동 시 교체
    // const data = await fetchPostList(filters);
    // posts.value = data;

    posts.value = []; // 임시
  } catch (e) {
    error.value = "게시글 목록 조회 실패";
  } finally {
    loading.value = false;
  }
};

const goDetail = (postId) => router.push(`/community/${postId}`);
const goWrite = () => router.push(`/community/write`);

onMounted(fetchPosts);
</script>

<style scoped>
.community-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.post-list {
  list-style: none;
  padding: 0;
}
.post-card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 14px;
  margin: 12px 0;
  cursor: pointer;
}
</style>
