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
                    <div class="search-wrapper">
                        <input 
                            type="text" 
                            v-model="searchQuery" 
                            placeholder="제목 검색"
                        >
                        <i class="fas fa-search search-icon"></i>
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
                        <div 
                            v-for="post in pagedPosts" 
                            :key="post.id" 
                            class="post-card"
                            @click="goDetail(post.id)"
                        >
                            <div class="card-header-img" :style="getCardHeaderStyle(post.thumbnail)">
                                <span class="genre-badge">자유</span>
                                <div class="card-icon">💬</div>
                            </div>

                            <div class="card-body">
                                <h3 class="card-title">{{ post.title }}</h3>
                                
                                <div class="card-footer">
                                    <div class="author">
                                        <div class="author-avatar">U</div>
                                        <span>{{ post.user_nickname }}</span> 
                                    </div>
                                    <div class="stats">
                                        <span class="stat-item likes"><i class="fas fa-heart"></i> {{ post.like_count || 0 }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="pagination" v-if="totalPages > 1">
                        <button 
                            class="page-link" 
                            :disabled="currentPage === 1"
                            @click="changePage(currentPage - 1)"
                        >
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

                        <button 
                            class="page-link" 
                            :disabled="currentPage === totalPages"
                            @click="changePage(currentPage + 1)"
                        >
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

const route = useRoute()
const router = useRouter()

const allPosts = ref([]) // 서버에서 가져온 전체 데이터 저장소
const loading = ref(true)
const searchQuery = ref('') // 실시간 검색어
const currentTab = ref('all') 
const pageSize = 6 // 한 페이지당 개수

// --- [A] 한글 초성 검색 로직 ---
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

// --- [B] 필터링된 게시글 (검색 + 탭 필터) ---
const filteredPosts = computed(() => {
    let result = allPosts.value;
    if (currentTab.value !== 'all') {
        result = result.filter(post => post.status === currentTab.value);
    }
    if (searchQuery.value.trim()) {
        const query = searchQuery.value.toLowerCase().trim();
        result = result.filter(post => {
            const title = post.title.toLowerCase();
            return title.includes(query) || getChosung(title).includes(query);
        });
    }
    return result;
});

// --- [C] 최종적으로 화면에 보여줄 페이지 데이터 (Pagination) ---
const currentPage = computed(() => Number(route.query.page) || 1);
const totalPages = computed(() => Math.ceil(filteredPosts.value.length / pageSize));

const pagedPosts = computed(() => {
    const start = (currentPage.value - 1) * pageSize;
    const end = start + pageSize;
    return filteredPosts.value.slice(start, end);
});

// --- [D] 데이터 불러오기 (백엔드 페이지네이션 우회) ---
const fetchPosts = async () => {
    loading.value = true
    try {
        const res = await axios.get(`/api/accounts/profile/stories/`, {
            params: { no_pagination: 'true' } // 백엔드 수정 사항과 일치시킴
        })
        allPosts.value = Array.isArray(res.data) ? res.data : res.data.results;
    } catch (error) {
        console.error("동화 로드 실패:", error)
    } finally {
        loading.value = false
    }
}

// 검색어 변경 시 1페이지로 리셋
watch(searchQuery, () => {
    router.replace({ query: { ...route.query, page: 1 } });
});

// 페이지 이동
const changePage = (page) => {
    if (page < 1 || page > totalPages.value) return
    router.push({ query: { ...route.query, page: page } })
    window.scrollTo({ top: 0, behavior: 'smooth' })
};
// 상세 페이지 이동
const goDetail = (id) => {
    router.push(`/story/read/${id}`)
}

const goToCreate = () => {
    router.push('/story/create')
}

// 썸네일 스타일 
const getCardHeaderStyle = (thumbnail) => {
    if (thumbnail) {
        let imageUrl = thumbnail;
        if (!thumbnail.startsWith('http') && !thumbnail.startsWith('data:image')) {
            imageUrl = `data:image/png;base64,${thumbnail}`;
        }
        return {
            backgroundImage: `url(${imageUrl})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center'
        }
    }
    return {
        background: 'linear-gradient(135deg, #F0F9FF 0%, #FFF9E5 100%)'
    }
}

// 파티클 효과
onMounted(() => {
    fetchPosts()

    document.addEventListener('click', (e) => {
        if(e.target.closest('.post-card') || e.target.closest('.write-btn')) return;
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                const offsetX = (Math.random() - 0.5) * 40;
                const offsetY = (Math.random() - 0.5) * 40;
                createParticle(e.clientX + offsetX, e.clientY + offsetY);
            }, i * 50);
        }
    });
})

function createParticle(x, y) {
    const emojis = ['⭐', '✨', '💖', '💬', '📖'];
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    particle.style.left = x + 'px';
    particle.style.top = y + 'px';
    document.body.appendChild(particle);
    setTimeout(() => particle.remove(), 1000);
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Nunito:wght@600;700;800;900&display=swap');

:root {
    --primary: #58CC02;
    --primary-light: #89E152;
    --primary-dark: #46A302;
    --secondary: #1CB0F6;
    --secondary-light: #58D3FF;
    --pink: #FF6B9D;
    --purple: #CE82FF;
    --orange: #FF9600;
    --yellow: #FFC800;
    --text: #3C3C3C;
    --bg: #FFFFFF;
    --gray-light: #F7F7F7;
}

/* 기존 스타일 그대로 유지 + 썸네일용 스타일 추가 */
.loading-area, .empty-area {
    text-align: center;
    padding: 50px;
    font-size: 1.2rem;
    color: #888;
    font-weight: 700;
}

.card-header-img {
    height: 160px; /* 썸네일 영역 높이 확보 */
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    border-bottom: 1px solid #f0f0f0;
}

/* 아래는 기존 CommunityRoot 스타일 그대로 */
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Nunito', 'Jua', sans-serif;
    color: var(--text);
    background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
    overflow-x: hidden;
    min-height: 100vh;
}

/* [1] 배경 애니메이션 */
.floating-bg {
    position: fixed;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.cloud {
    position: absolute;
    font-size: 60px;
    opacity: 0.3;
    animation: cloud-drift 30s infinite linear;
}
.cloud:nth-child(1) { top: 10%; animation-duration: 25s; }
.cloud:nth-child(2) { top: 30%; animation-duration: 35s; animation-delay: 5s; }
.cloud:nth-child(3) { top: 50%; animation-duration: 28s; animation-delay: 10s; }
.cloud:nth-child(4) { top: 70%; animation-duration: 32s; animation-delay: 15s; }
@keyframes cloud-drift {
    0% { left: -100px; }
    100% { left: calc(100% + 100px); }
}
.star {
    position: absolute;
    font-size: 30px;
    opacity: 0;
    animation: star-twinkle 3s infinite;
}
.star:nth-child(5) { top: 15%; left: 20%; animation-delay: 0s; }
.star:nth-child(6) { top: 25%; right: 15%; animation-delay: 1s; }
.star:nth-child(7) { top: 45%; left: 10%; animation-delay: 2s; }
.star:nth-child(8) { bottom: 30%; right: 20%; animation-delay: 1.5s; }
@keyframes star-twinkle {
    0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
    50% { opacity: 0.6; transform: scale(1.2) rotate(180deg); }
}

/* [2] 헤더 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
    z-index: 1;
}

/* -----------------------------------------------------------
    [3] 커뮤니티 게시판 스타일 (New!)
    ----------------------------------------------------------- */
.board-section {
    padding: 40px 0 80px;
}
.board-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 30px;
    flex-wrap: wrap;
    gap: 20px;
}
.page-title h1 {
    font-size: 2.5rem;
    color: var(--text);
    margin-bottom: 5px;
}
.page-title p {
    color: #888;
    font-weight: 600;
}
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
.category-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    overflow-x: auto;
    padding-bottom: 10px;
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

/* 게시글 카드 */
.post-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
    margin-bottom: 50px;
}
.post-card {
    background: white;
    border-radius: 25px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    border: 3px solid transparent;
    transition: all 0.3s;
    cursor: pointer;
    display: flex;
    flex-direction: column;
}
.post-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border-color: var(--secondary-light);
}
.genre-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    background: white;
    padding: 5px 12px;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 800;
    color: var(--primary);
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.card-icon {
    font-size: 3.5rem;
    animation: float-icon 3s infinite ease-in-out;
}
@keyframes float-icon {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}
.card-body {
    padding: 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
}
.card-title {
    font-size: 1.2rem;
    font-weight: 800;
    margin-bottom: 10px;
    color: var(--text);
}
.card-excerpt {
    font-size: 0.95rem;
    color: #777;
    margin-bottom: 20px;
    flex: 1;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 2px solid #F7F7F7;
    padding-top: 15px;
    font-size: 0.9rem;
    color: #999;
    font-weight: 600;
}
.author { display: flex; align-items: center; gap: 8px; }
.author-avatar {
    width: 28px; height: 28px; background: #E5E5E5;
    border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem;
}
.stats { display: flex; gap: 12px; }
.stat-item.likes { color: var(--pink); }

.write-btn {
    position: fixed;
    bottom: 40px; right: 40px;
    width: 65px; height: 65px;
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.8rem;
    box-shadow: 0 10px 25px rgba(88, 204, 2, 0.4);
    cursor: pointer; transition: all 0.3s;
    border: none; z-index: 100;
}
.write-btn:hover { transform: scale(1.1) rotate(90deg); }
/* 기존 pagination 스타일 수정/확장 */
.pagination { 
    display: flex; 
    justify-content: center; 
    align-items: center;
    gap: 10px; 
    margin-top: 40px; 
}

.page-link {
    width: 40px; 
    height: 40px; 
    display: flex; 
    align-items: center; 
    justify-content: center;
    border-radius: 12px; 
    background: white; 
    color: var(--text); 
    font-weight: 700; 
    border: none; /* button 태그이므로 border 제거 */
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    transition: all 0.2s;
}

.page-link:hover:not(:disabled) {
    background: #f0f0f0;
    transform: translateY(-2px);
}

.page-link.active { 
    background: var(--purple); 
    color: white; 
    box-shadow: 0 4px 15px rgba(206, 130, 255, 0.4);
}

.page-link:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background: #eee;
}

@media (max-width: 768px) {
    .nav-links { display: none; }
}
</style>