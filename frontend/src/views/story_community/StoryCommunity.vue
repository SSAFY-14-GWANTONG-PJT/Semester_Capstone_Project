<template>
  <div>
    <div class="floating-bg">
        <div class="cloud">☁️</div>
        <div class="cloud">☁️</div>
        <div class="cloud">☁️</div>
        <div class="cloud">☁️</div>
        <div class="star">⭐</div>
        <div class="star">✨</div>
        <div class="star">💫</div>
        <div class="star">🌟</div>
    </div>

    <section class="board-section">
      <div class="container">
        <div class="board-header">
            <div class="page-title">
                <h1>동화 도서관 📚</h1>
                <p>친구들과 자유롭게 동화를 공유해보세요!</p>
            </div>
            <div class="header-controls">
                <button 
                  class="like-filter-btn" 
                  :class="{ active: onlyLiked }"
                  @click="toggleLikedFilter"
                >
                  <i :class="onlyLiked ? 'fas fa-heart' : 'far fa-heart'"></i>
                  좋아요 모아보기
                </button>
                <div class="search-wrapper">
                    <input 
                        type="text" 
                        v-model="searchQuery" 
                        placeholder="제목 검색"
                    >
                    <i class="fas fa-search search-icon"></i>
                </div>
            </div>
        </div>

        <div class="category-tabs">
            <button class="tab-btn" title="동화 만들기" @click="goToCreate">✨ 동화 만들기 ✨</button>
        </div>

        <div v-if="loading" class="loading-area">
            <i class="fas fa-spinner fa-spin"></i> 이야기를 불러오고 있어요...
        </div>

        <div v-else-if="allPosts.length === 0" class="empty-area">
            <p>아직 등록된 이야기가 없어요 😢<br>첫 번째 작가가 되어보세요!</p>
        </div>

        <div v-else-if="filteredPosts.length === 0" class="empty-area">
            <p>찾으시는 검색 결과가 없어요 🔍<br>다른 단어로 검색해보시겠어요?</p>
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
                  <div class="author">
                      <div class="author-avatar">U</div>
                      <span>{{ story.user_nickname }}</span> 
                  </div>
                  <div class="card-like-info" :class="{ 'is-liked': story.is_liked }">
                      <i class="fas fa-heart"></i>
                      <span>{{ story.like_count || 0 }}</span>
                  </div>
                  <div class="date-info">
                    생성 : {{ story.created_at.slice(0, 10) }}
                  </div>
                  <div class="status-tag" :class="story.status">
                    {{ story.status === 'open' ? '공유 중 🌐' : '나만 보기 🔒' }}
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
      </div>
    </section>

    <button class="write-btn" title="동화 만들기" @click="goToCreate">
        <i class="fas fa-pen"></i>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from '@/api/index.js'

const router = useRouter()
const route = useRoute()

const allPosts = ref([]) // 템플릿과 맞춤
const loading = ref(true)
const searchQuery = ref('')
const filterStatus = ref('all')
const onlyLiked = ref(false) // 추가: 좋아요 필터 상태
const pageSize = 6

// 한글 초성 검색 로직
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

// 추가: 좋아요 필터 토글 함수
const toggleLikedFilter = () => {
    onlyLiked.value = !onlyLiked.value
}

// 검색 + 필터링 (좋아요 필터 로직 추가)
const filteredPosts = computed(() => {
  let res = [...allPosts.value];
  if (filterStatus.value !== 'all') {
    res = res.filter(s => s.status === filterStatus.value);
  }
  // 추가: 좋아요 필터링
  if (onlyLiked.value) {
    res = res.filter(s => s.is_liked);
  }
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    res = res.filter(s => s.title.toLowerCase().includes(query) || getChosung(s.title).includes(query));
  }
  return res.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
});

// 페이지네이션
const currentPage = computed(() => Number(route.query.page) || 1);
const totalPages = computed(() => Math.ceil(filteredPosts.value.length / pageSize));
const pagedStories = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredPosts.value.slice(start, start + pageSize);
});

// 데이터 로드
const fetchPosts = async () => {
  loading.value = true
  try {
    const res = await axios.get('api/community/allstories/', {
        params: { no_pagination: 'true' }
    })
    console.log(res.data)
    allPosts.value = res.data || []
  } catch (err) {
    console.error("데이터 로드 실패", err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchPosts)

watch(searchQuery, () => router.replace({ query: { ...route.query, page: 1 } }));

const changePage = (p) => {
  router.push({ query: { ...route.query, page: p } });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

const getGenreName = (g) => ({ hero: '영웅', happy: '행복', fantasy: '판타지' }[g] || '동화')
const getGenreEmoji = (g) => ({ hero: '🦸‍♂️', happy: '🥰', fantasy: '🧙‍♂️' }[g] || '📖')
const getThumbnail = (img) => img ? { backgroundImage: `url(data:image/png;base64,${img})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}
const goDetail = (id) => router.push(`/story/read/${id}`)
const goToCreate = () => router.push('/story/create')
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Nunito:wght@600;700;800;900&display=swap');

:root {
    --primary: #58CC02;
    --secondary: #1CB0F6;
    --purple: #CE82FF;
    --text: #3C3C3C;
}

/* [1] 배경 레이아웃 & 애니메이션 */
.floating-bg {
    position: fixed;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.cloud {
    position: absolute; font-size: 60px; opacity: 0.3;
    animation: cloud-drift 30s infinite linear;
}
@keyframes cloud-drift {
    0% { left: -100px; }
    100% { left: calc(100% + 100px); }
}
.star {
    position: absolute; font-size: 30px; opacity: 0;
    animation: star-twinkle 3s infinite;
}
@keyframes star-twinkle {
    0%, 100% { opacity: 0; transform: scale(0); }
    50% { opacity: 0.6; transform: scale(1.2); }
}

/* [2] 컨테이너 & 섹션 */
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; position: relative; z-index: 1; }
.board-section { padding: 40px 0 80px; }

/* [3] 헤더 & 검색 */
.board-header {
    display: flex; justify-content: space-between; align-items: flex-end;
    margin-bottom: 30px; flex-wrap: wrap; gap: 20px;
}
.page-title h1 { font-size: 2.5rem; color: var(--text); margin-bottom: 5px; }
.page-title p { color: #888; font-weight: 600; }

.header-controls { display: flex; align-items: center; gap: 15px; }

/* 추가: 좋아요 필터 버튼 스타일 */
.like-filter-btn {
    padding: 10px 20px;
    border-radius: 20px;
    border: 2px solid #E5E5E5;
    background: white;
    color: #777;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
}
.like-filter-btn.active {
    border-color: #FF6B9D;
    color: #FF6B9D;
    background: #FFF0F5;
}
.like-filter-btn:hover {
    background: #f8f8f8;
}

.search-wrapper { position: relative; width: 300px; }
.search-wrapper input {
    width: 100%; padding: 12px 20px 12px 45px;
    border: 3px solid #E5E5E5; border-radius: 25px;
    font-size: 1rem; outline: none; transition: all 0.3s;
}
.search-wrapper input:focus { border-color: var(--secondary); box-shadow: 0 5px 15px rgba(28, 176, 246, 0.2); }
.search-icon { position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: #AAA; }

/* [4] 버튼 & 탭 */
.category-tabs { margin-bottom: 30px; }
.tab-btn {
    padding: 12px 28px; border-radius: 25px; border: none;
    background: linear-gradient(135deg, #58CC02 0%, #89E152 100%);
    color: white; font-weight: 800; cursor: pointer;
    box-shadow: 0 4px 15px rgba(88, 204, 2, 0.3);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.tab-btn:hover { transform: scale(1.01); box-shadow: 0 8px 25px rgba(88, 204, 2, 0.4); }

.write-btn {
    position: fixed; bottom: 40px; right: 40px;
    width: 65px; height: 65px;
    background: linear-gradient(135deg, #58CC02, #89E152);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.8rem; border: none; cursor: pointer; z-index: 100;
}

/* [5] 카드 그리드 */
.post-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; margin-bottom: 50px; }
.post-card {
    background: white; border-radius: 25px; overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); transition: all 0.3s; cursor: pointer;
}
.post-card:hover { transform: translateY(-10px); border-color: var(--secondary); }

.card-header-img { height: 160px; display: flex; align-items: center; justify-content: center; position: relative; background: #f9f9f9; }
.genre-badge {
    position: absolute; top: 15px; right: 15px; background: white;
    padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; font-weight: 800; color: #58CC02;
}
.card-icon { font-size: 3.5rem; animation: float-icon 3s infinite ease-in-out; }
@keyframes float-icon { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }

.card-body { padding: 20px; }
.card-title { font-size: 1.2rem; font-weight: 800; margin-bottom: 10px; color: var(--text); }
.card-excerpt {
    font-size: 0.95rem; color: #777; margin-bottom: 20px;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

.card-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #eee; padding-top: 15px; flex-wrap: wrap; gap: 10px; }

/* 추가: 카드 내 좋아요 아이콘 스타일 */
.card-like-info {
    display: flex;
    align-items: center;
    gap: 5px;
    font-weight: 700;
    color: #bbb;
    font-size: 0.9rem;
}
.card-like-info.is-liked {
    color: #FF6B9D;
}

.date-info { color: #999; font-size: 0.9rem; }
.status-tag { font-size: 0.85rem; font-weight: 800; }
.status-tag.open { color: #58CC02; }

/* [6] 공통 안내 영역 */
.loading-area, .empty-area { text-align: center; padding: 100px 20px; color: #888; font-weight: 700; font-size: 1.2rem; }

/* [7] 페이지네이션 */
.pagination { display: flex; justify-content: center; gap: 10px; margin-top: 40px; }
.page-link {
    width: 40px; height: 40px; border-radius: 12px; background: white;
    display: flex; align-items: center; justify-content: center;
    border: none; cursor: pointer; font-weight: 700; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.page-link.active { background: #CE82FF; color: white; }
.page-link:disabled { opacity: 0.5; cursor: not-allowed; }


.author { display: flex; align-items: center; gap: 8px; }
.author-avatar {
    width: 28px; height: 28px; background: #E5E5E5;
    border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem;
}
</style>