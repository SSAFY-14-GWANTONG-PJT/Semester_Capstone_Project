<template>
  <div class="my-library-page">
    <section class="board-section container">
      <div class="board-header">
        <div class="page-title-group">
          <div class="back-link" @click="router.push('/mypage')">⬅️ 마이페이지로</div>
          <div class="page-title">
            <h1>나의 비밀 서재 📖</h1>
            <p>그동안 모험하며 직접 만든 소중한 이야기들이에요.</p>
          </div>
          
          <div class="filter-tabs">
            <button 
              class="filter-btn" 
              :class="{ active: filterStatus === 'all' }" 
              @click="setFilter('all')"
            >전체보기</button>
            <button 
              class="filter-btn" 
              :class="{ active: filterStatus === 'open' }" 
              @click="setFilter('open')"
            >공유 중 🌐</button>
            <button 
              class="filter-btn" 
              :class="{ active: filterStatus === 'normal' }" 
              @click="setFilter('normal')"
            >비공개 🔒</button>
          </div>

          <button class="tab-btn" @click="goToCreate" style="margin-top: 20px;">✨ 동화 만들기 ✨</button>
        </div>
        
        <div class="search-wrapper">
          <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="제목 검색"
          >
          <i class="fas fa-search search-icon"></i>
        </div>
      </div>

      <div v-if="loading" class="loading-area">
        <i class="fas fa-spinner fa-spin"></i> 서재를 정리하고 있어요...
      </div>

      <div v-else-if="stories.length === 0" class="empty-area">
        <p>서재가 아직 비어있네요 😢<br>첫 번째 이야기를 만들러 가볼까요?</p>
      </div>

      <div v-else-if="filteredStories.length === 0" class="empty-area">
        <p>찾으시는 이야기가 서재에 없어요 🔍<br>다른 제목으로 찾아볼까요?</p>
      </div>

      <div v-else>
        <div class="post-grid">
          <div v-for="story in pagedStories" :key="story.id" class="post-card" @click="goDetail(story.id)">
            <div class="card-header-img" :style="getThumbnail(story.thumbnail)">
              <span class="genre-badge">{{ getGenreName(story.genre) }}</span>
              <div v-if="!story.thumbnail" class="card-icon">{{ getGenreEmoji(story.genre) }}</div>
            </div>

            <div class="card-body">
              <h3 class="card-title">{{ story.title }}</h3>
              <p class="card-excerpt">{{ story.summary || '아이와 함께 만든 소중한 이야기입니다.' }}</p>
              
              <div class="card-footer">
                <div class="date-info">
                  <i class="far fa-calendar-alt"></i> {{ story.created_at?.slice(0, 10) }}
                </div>
                <div class="status-tag" :class="story.status">
                  {{ story.status?.trim() === 'open' ? '공유 중 🌐' : '나만 보기 🔒' }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="pagination" v-if="totalPages > 1">
          <button class="page-link" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
            <i class="fas fa-chevron-left"></i>
          </button>
          
          <button 
            v-for="page in totalPages" 
            :key="page"
            class="page-link"
            :class="{ active: currentPage === page }"
            @click="changePage(page)"
          >
            {{ page }}
          </button>

          <button class="page-link" :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '@/api/index.js'

const router = useRouter()
const route = useRoute()

// stories 변수 하나로 통일
const stories = ref([])
const loading = ref(true)
const searchQuery = ref('')
const filterStatus = ref('all')
const pageSize = 6

// --- 초성 검색 로직 ---
const CHO_HANGUL = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
const getChosung = (str) => {
  let result = "";
  for (let i = 0; i < str.length; i++) {
    const code = str.charCodeAt(i) - 44032;
    if (code > -1 && code < 11172) result += CHO_HANGUL[Math.floor(code / 588)];
    else result += str.charAt(i);
  }
  return result;
};

// --- 검색 + 상태필터 + 정렬 필터링 ---
const filteredStories = computed(() => {
  let res = [...stories.value];
  
  // 1. 상태 필터링 (trim() 추가하여 정확도 향상 ⭐)
  if (filterStatus.value !== 'all') {
    res = res.filter(s => s.status?.trim() === filterStatus.value);
  }
  
  // 2. 검색어 필터링
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    res = res.filter(s => s.title.toLowerCase().includes(query) || getChosung(s.title).includes(query));
  }
  
  // 3. 최신순 정렬
  return res.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
});

// --- 페이지네이션 계산 ---
const currentPage = computed(() => Number(route.query.page) || 1);
const totalPages = computed(() => Math.ceil(filteredStories.value.length / pageSize));
const pagedStories = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredStories.value.slice(start, start + pageSize);
});

// --- 데이터 로드 ---
const fetchStories = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/accounts/profile/stories/', {
        params: { no_pagination: 'true' }
    })
    // stories 변수에 데이터 할당
    stories.value = res.data || []
  } catch (err) {
    console.error("데이터 로드 실패", err)
  } finally {
    loading.value = false
  }
}

const setFilter = (status) => {
  filterStatus.value = status;
  router.replace({ query: { ...route.query, page: 1 } });
};

onMounted(fetchStories)

watch(searchQuery, () => router.replace({ query: { ...route.query, page: 1 } }));

const changePage = (p) => {
  router.push({ query: { ...route.query, page: p } });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 헬퍼 함수
const getGenreName = (g) => ({ hero: '영웅', happy: '행복', fantasy: '판타지' }[g] || '동화')
const getGenreEmoji = (g) => ({ hero: '🦸‍♂️', happy: '🥰', fantasy: '🧙‍♂️' }[g] || '📖')
const getThumbnail = (img) => img ? { backgroundImage: `url(data:image/png;base64,${img})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}
const goDetail = (id) => router.push(`/story/read/${id}`)
const goToCreate = () => router.push('/story/create')
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

/* 헤더 레이아웃 수정 */
.board-header {
  display: flex;
  justify-content: space-between; /* 양 끝 정렬 */
  align-items: flex-end; /* 아래쪽 라인 맞춤 */
  margin-bottom: 40px;
  gap: 20px;
  flex-wrap: wrap; /* 모바일 대응 */
}

.page-title-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.back-link { 
  cursor: pointer; 
  font-weight: 800; 
  color: var(--secondary); 
  font-size: 0.95rem;
  transition: 0.2s;
}
.back-link:hover { transform: translateX(-5px); }

.pagination { display: flex; justify-content: center; gap: 10px; margin-top: 40px; }
.page-link {
  width: 40px; height: 40px; border-radius: 12px; background: white;
  display: flex; align-items: center; justify-content: center;
  border: none; cursor: pointer; font-weight: 700; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.page-link.active { background: var(--purple); color: white; }
.page-link:disabled { opacity: 0.5; cursor: not-allowed; }

.loading-area, .empty-area { text-align: center; padding: 100px 20px; color: #888; font-weight: 700; }

.search-wrapper {
    position: relative;
    width: 300px;
}
.search-wrapper input {
    width: 100%;
    padding: 12px 20px 12px 45px;
    border: 3px solid #E5E5E5;
    border-radius: 25px;
    font-size: 1rem;
    font-family: 'Nunito', sans-serif;
    font-weight: 600;
    outline: none;
    transition: all 0.3s;
    background: white;
}
.search-wrapper input:focus {
    border-color: var(--secondary);
    box-shadow: 0 5px 15px rgba(28, 176, 246, 0.2);
}
.search-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #AAA;
}

.tab-btn {
    padding: 12px 28px;
    border-radius: 25px;
    border: none; /* 테두리를 없애고 그림자로 입체감 표현 */
    background: linear-gradient(135deg, #58CC02 0%, #89E152 100%); /* 화사한 초록 그라데이션 */
    color: white; /* 글자는 흰색으로 대비 */
    font-size: 1.05rem;
    font-weight: 800;
    cursor: pointer;
    white-space: nowrap;
    box-shadow: 0 4px 15px rgba(88, 204, 2, 0.3); /* 부드러운 초록색 그림자 */
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* 통통 튀는 느낌의 애니메이션 */
    font-family: 'Jua', 'Nunito', sans-serif;
}

/* 마우스를 올렸을 때 (Hover) */
.tab-btn:hover {
    transform: scale(1.01); /* 살짝 커지면서 위로 떠오름 */
    box-shadow: 0 8px 25px rgba(88, 204, 2, 0.4); /* 그림자가 깊어짐 */
    background: linear-gradient(135deg, #46A302 0%, #58CC02 100%); /* 색상이 살짝 진해짐 */
}

/* 클릭하는 순간 (Active) */
.tab-btn:active {
    transform: scale(0.95) translateY(0); /* 살짝 눌리는 느낌 */
    box-shadow: 0 2px 10px rgba(88, 204, 2, 0.2);
}

/* 필터 탭 스타일 추가 ⭐ */
.filter-tabs {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.filter-btn {
  padding: 8px 16px;
  border-radius: 12px;
  border: 2px solid #E5E5E5;
  background: white;
  font-weight: 700;
  color: #888;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: #f7f7f7;
}

/* 활성화된 버튼 스타일 (초록색 계열 추천) */
.filter-btn.active {
  background: var(--secondary); /* 혹은 var(--primary) */
  border-color: var(--secondary);
  color: white;
  box-shadow: 0 4px 10px rgba(28, 176, 246, 0.2);
}
</style>