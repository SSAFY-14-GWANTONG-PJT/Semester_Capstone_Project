<template>
  <div class="my-library-page">
    <section class="board-section container">
      <div class="board-header">
        <div class="page-title">
          <h1>나의 비밀 서재 📖</h1>
          <p>그동안 모험하며 직접 만든 소중한 이야기들이에요.</p>
        </div>
        <div class="back-link" @click="router.back()">⬅️ 마이페이지로</div>
      </div>

      <div class="post-grid">
        <div v-for="story in sortedAllStories" :key="story.id" class="post-card" @click="goDetail(story.id)">
          <div class="card-header-img" :style="getThumbnail(story.thumbnail)">
            <span class="genre-badge">{{ getGenreName(story.genre) }}</span>
            <div v-if="!story.thumbnail" class="card-icon">{{ getGenreEmoji(story.genre) }}</div>
          </div>

          <div class="card-body">
            <h3 class="card-title">{{ story.title }}</h3>
            <p class="card-excerpt">{{ story.summary || '아이와 함께 만든 소중한 이야기입니다.' }}</p>
            
            <div class="card-footer">
              <div class="date-info">
                <i class="far fa-calendar-alt"></i> {{ story.created_at.slice(0, 10) }}
              </div>
              <div class="status-tag" :class="story.status">
                {{ story.status === 'open' ? '공유 중 🌐' : '나만 보기 🔒' }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/api/index.js'

const router = useRouter()
const stories = ref([])

const sortedAllStories = computed(() => {
  return [...stories.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

onMounted(async () => {
  try {
    const res = await axios.get('/api/accounts/profile/stories/') // 유저 정보에서 동화 리스트 추출
    stories.value = res.data || []
  } catch (err) {
    console.error("데이터 로드 실패", err)
  }
})

// 헬퍼 함수 (커뮤니티 코드 참고)
const getGenreName = (g) => ({ hero: '영웅', happy: '행복', fantasy: '판타지' }[g] || '동화')
const getGenreEmoji = (g) => ({ hero: '🦸‍♂️', happy: '🥰', fantasy: '🧙‍♂️' }[g] || '📖')
const getThumbnail = (img) => img ? { backgroundImage: `url(data:image/png;base64,${img})`, backgroundSize: 'cover' } : {}
const goDetail = (id) => router.push(`/story/read/${id}`)
</script>

<style scoped>
.my-library-page { min-height: 100vh; padding-top: 40px; }
.post-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }
.post-card { 
  background: white; border-radius: 25px; overflow: hidden; 
  box-shadow: 0 10px 30px rgba(0,0,0,0.05); transition: 0.3s; cursor: pointer;
  border: 3px solid transparent;
}
.post-card:hover { transform: translateY(-10px); border-color: var(--secondary); }

.card-header-img { height: 160px; display: flex; align-items: center; justify-content: center; position: relative; background: #f9f9f9; }
.card-body { padding: 20px; }
.card-title { font-size: 1.2rem; font-weight: 800; margin-bottom: 10px; color: #333; }
.card-footer { display: flex; justify-content: space-between; padding-top: 15px; border-top: 1px solid #eee; font-size: 0.85rem; color: #999; }

.status-tag.open { color: var(--primary); font-weight: 800; }
.back-link { cursor: pointer; font-weight: 800; color: var(--secondary); margin-bottom: 10px; }
</style>