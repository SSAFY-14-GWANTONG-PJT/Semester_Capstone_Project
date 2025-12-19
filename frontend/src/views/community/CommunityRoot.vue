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

        <header>
            <div class="container nav-wrapper">
                <RouterLink to="/" class="logo-nav">
                    <div class="logo-nav-icon">📖</div>
                    <span>Step-up Story</span>
                </RouterLink>
                <nav class="nav-links">
                    <RouterLink to="/">홈</RouterLink>
                    <RouterLink to="/community" class="active">커뮤니티</RouterLink>
                    <RouterLink to="/learning/today">학습 로드맵</RouterLink>
                    <RouterLink style="color: var(--secondary);" :to="{name: 'login'}">로그인</RouterLink>
                </nav>
            </div>
        </header>

        <section class="board-section">
            <div class="container">
                <div class="board-header">
                    <div class="page-title">
                        <h1>이야기 광장 🌳</h1>
                        <p>친구들과 만든 동화를 공유하고 이야기를 나눠보세요!</p>
                    </div>
                    <div class="search-wrapper">
                        <input type="text" placeholder="제목, 태그 검색...">
                        <i class="fas fa-search search-icon"></i>
                    </div>
                </div>

                <div class="category-tabs">
                    <button class="tab-btn active">전체 ✨</button>
                    <button class="tab-btn">동화 공유 📖</button>
                    <button class="tab-btn">자유 수다 💬</button>
                </div>

                <div v-if="loading" class="loading-area">
                    <i class="fas fa-spinner fa-spin"></i> 이야기를 불러오고 있어요...
                </div>

                <div v-else-if="stories.length === 0" class="empty-area">
                    <p>아직 등록된 이야기가 없어요 😢<br>첫 번째 작가가 되어보세요!</p>
                </div>

                <div v-else class="post-grid">
                    <div 
                        v-for="story in stories" 
                        :key="story.id" 
                        class="post-card"
                        @click="goDetail(story.id)"
                    >
                        <div class="card-header-img" :style="getCardHeaderStyle(story.thumbnail)">
                            <span class="genre-badge">{{ getGenreName(story.genre) }}</span>
                            <div v-if="!story.thumbnail" class="card-icon">📖</div>
                        </div>

                        <div class="card-body">
                            <h3 class="card-title">{{ story.title }}</h3>
                            <p class="card-excerpt">{{ story.summary || '내용 요약이 없습니다.' }}</p>
                            
                            <div class="card-footer">
                                <div class="author">
                                    <div class="author-avatar">{{ story.author_nickname ? story.author_nickname[0] : 'U' }}</div>
                                    <span>{{ story.author_nickname }}</span>
                                </div>
                                <div class="stats">
                                    <span class="stat-item likes"><i class="fas fa-heart"></i> {{ story.like_count }}</span>
                                    <span class="stat-item comments"><i class="fas fa-comment"></i> 0</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="pagination">
                    <a href="#" class="page-link active">1</a>
                </div>
            </div>
        </section>

        <button class="write-btn" title="새 글 쓰기" @click="goToCreate">
            <i class="fas fa-pen"></i>
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const stories = ref([])
const loading = ref(true)

// API URL (환경변수 없으면 기본값 사용)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// 스토리 목록 불러오기
const fetchStories = async () => {
    try {
        // status='open' 인 스토리만 요청
        const res = await axios.get(`${API_URL}/stories/`, {
            params: { status: 'open' }
        })
        stories.value = res.data
    } catch (error) {
        console.error("동화 목록 로드 실패:", error)
    } finally {
        loading.value = false
    }
}

// 상세 페이지 이동
const goDetail = (id) => {
    router.push(`/story/read/${id}`)
}

const goToCreate = () => {
    router.push('/story/create')
}

// 헬퍼 함수들
const getGenreName = (code) => {
    const map = {
        hero: '영웅', happy: '행복', sad: '슬픔',
        romance: '로맨스', horror: '호러', fantasy: '판타지', sf: 'SF/우주'
    }
    return map[code] || '동화'
}

// 썸네일 있으면 배경이미지로, 없으면 그라데이션
const getCardHeaderStyle = (thumbnail) => {
    if (thumbnail) {
        let imageUrl = thumbnail;
        
        // 만약 썸네일이 'http'로 시작하지 않고(웹주소 아님),
        // 'data:image'로도 시작하지 않는다면(이미지 태그 아님) -> 순수 Base64 데이터로 간주
        if (!thumbnail.startsWith('http') && !thumbnail.startsWith('data:image')) {
            imageUrl = `data:image/png;base64,${thumbnail}`;
        }

        return {
            backgroundImage: `url(${imageUrl})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center'
        }
    }
    // 썸네일 없으면 기본 그라데이션 배경
    return {
        background: 'linear-gradient(135deg, #F0F9FF 0%, #FFF9E5 100%)'
    }
}

// 파티클 효과 (디자인 요소)
onMounted(() => {
    fetchStories() // 데이터 로드 시작

    // 배경 클릭 시 파티클 생성
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
header {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    padding: 20px 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
.nav-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.logo-nav {
    font-size: 2rem;
    font-weight: 900;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text);
    text-decoration: none;
}
.logo-nav-icon {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
}
.nav-links a {
    color: var(--text);
    text-decoration: none;
    margin-left: 30px;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.3s;
}
.nav-links a:hover {
    color: var(--primary);
    transform: translateY(-3px);
}
.nav-links a.active {
    color: var(--secondary);
}

/* [3] 게시판 스타일 */
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
    padding: 10px 20px;
    border-radius: 20px;
    border: 2px solid #E5E5E5;
    background: white;
    font-weight: 700;
    color: #888;
    cursor: pointer;
    white-space: nowrap;
}
.tab-btn.active {
    background: var(--primary);
    border-color: var(--primary);
    color: white;
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
.pagination { display: flex; justify-content: center; gap: 10px; margin-top: 20px; }
.page-link {
    width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;
    border-radius: 12px; background: white; color: var(--text); font-weight: 700; text-decoration: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.page-link.active { background: var(--purple); color: white; }

@media (max-width: 768px) {
    .nav-links { display: none; }
}
</style>