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
                <RouterLink to="/" class="logo">
                    <div class="logo-icon">📖</div>
                    <span>Step-up Story</span>
                </RouterLink>
                <nav class="nav-links">
                    <a href="index.html">홈</a>
                    <a href="#" class="active">커뮤니티</a>
                    <a href="#">학습 로드맵</a>
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
                    <button class="tab-btn">질문 있어요 🙋</button>
                    <button class="tab-btn">꿀팁 저장소 🍯</button>
                </div>

                <div class="post-grid">
                    <div class="post-card">
                        <div class="card-header">
                            <span class="genre-badge">판타지</span>
                            <div class="card-icon">🐉</div>
                        </div>
                        <div class="card-body">
                            <h3 class="card-title">용감한 드래곤과 잃어버린 보석</h3>
                            <p class="card-excerpt">AI가 만들어준 첫 번째 동화예요! 결말이 너무 감동적이라 공유합니다...</p>
                            <div class="card-footer">
                                <div class="author">
                                    <div class="author-avatar" style="background:#FFD1DC">홍</div>
                                    <span>홍길동</span>
                                </div>
                                <div class="stats">
                                    <span class="stat-item likes"><i class="fas fa-heart"></i> 12</span>
                                    <span class="stat-item comments"><i class="fas fa-comment"></i> 5</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="post-card">
                        <div class="card-header" style="background: linear-gradient(135deg, #FFF0F5 0%, #E6E6FA 100%);">
                            <span class="genre-badge">일상</span>
                            <div class="card-icon">🐱</div>
                        </div>
                        <div class="card-body">
                            <h3 class="card-title">고양이 탐정 냥냥이의 하루</h3>
                            <p class="card-excerpt">우리 집 고양이를 주인공으로 썼어요. 영단어 'Investigate'를 배웠어요!</p>
                            <div class="card-footer">
                                <div class="author">
                                    <div class="author-avatar" style="background:#D1EAFF">김</div>
                                    <span>김철수</span>
                                </div>
                                <div class="stats">
                                    <span class="stat-item likes"><i class="fas fa-heart"></i> 8</span>
                                    <span class="stat-item comments"><i class="fas fa-comment"></i> 2</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="post-card">
                        <div class="card-header" style="background: linear-gradient(135deg, #E0F7FA 0%, #B2EBF2 100%);">
                            <span class="genre-badge">SF/우주</span>
                            <div class="card-icon">🚀</div>
                        </div>
                        <div class="card-body">
                            <h3 class="card-title">화성으로 간 꼬마 로봇</h3>
                            <p class="card-excerpt">Lv.5 수준으로 만들었는데 생각보다 단어가 어렵네요. 피드백 부탁드려요.</p>
                            <div class="card-footer">
                                <div class="author">
                                    <div class="author-avatar" style="background:#FFF9C4">이</div>
                                    <span>이영희</span>
                                </div>
                                <div class="stats">
                                    <span class="stat-item likes"><i class="fas fa-heart"></i> 24</span>
                                    <span class="stat-item comments"><i class="fas fa-comment"></i> 11</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="post-card">
                        <div class="card-header" style="background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);">
                            <span class="genre-badge">미스터리</span>
                            <div class="card-icon">🕵️‍♀️</div>
                        </div>
                        <div class="card-body">
                            <h3 class="card-title">사라진 케이크의 비밀</h3>
                            <p class="card-excerpt">범인은 바로...?! 반전이 있는 스토리를 좋아하신다면 읽어보세요!</p>
                            <div class="card-footer">
                                <div class="author">
                                    <div class="author-avatar" style="background:#C8E6C9">P</div>
                                    <span>Park</span>
                                </div>
                                <div class="stats">
                                    <span class="stat-item likes"><i class="fas fa-heart"></i> 5</span>
                                    <span class="stat-item comments"><i class="fas fa-comment"></i> 0</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="post-card">
                        <div class="card-header" style="background: linear-gradient(135deg, #FFECB3 0%, #FFE082 100%);">
                            <span class="genre-badge">질문</span>
                            <div class="card-icon">❓</div>
                        </div>
                        <div class="card-body">
                            <h3 class="card-title">동화 생성할 때 질문있어요!</h3>
                            <p class="card-excerpt">주인공 이름을 제 이름으로 바꾸려면 어떻게 설정해야 하나요?</p>
                            <div class="card-footer">
                                <div class="author">
                                    <div class="author-avatar" style="background:#FFCCBC">Choi</div>
                                    <span>최자두</span>
                                </div>
                                <div class="stats">
                                    <span class="stat-item likes"><i class="fas fa-heart"></i> 1</span>
                                    <span class="stat-item comments"><i class="fas fa-comment"></i> 4</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="post-card">
                        <div class="card-header" style="background: linear-gradient(135deg, #B2DFDB 0%, #80CBC4 100%);">
                            <span class="genre-badge">자유</span>
                            <div class="card-icon">🎉</div>
                        </div>
                        <div class="card-body">
                            <h3 class="card-title">오늘 가입했어요! 반갑습니다.</h3>
                            <p class="card-excerpt">영어 공부 열심히 해보려고요. 잘 부탁드립니다~ 서로 팔로우해요!</p>
                            <div class="card-footer">
                                <div class="author">
                                    <div class="author-avatar" style="background:#CFD8DC">N</div>
                                    <span>Newbie</span>
                                </div>
                                <div class="stats">
                                    <span class="stat-item likes"><i class="fas fa-heart"></i> 15</span>
                                    <span class="stat-item comments"><i class="fas fa-comment"></i> 8</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="pagination">
                    <a href="#" class="page-link"><i class="fas fa-chevron-left"></i></a>
                    <a href="#" class="page-link active">1</a>
                    <a href="#" class="page-link">2</a>
                    <a href="#" class="page-link">3</a>
                    <a href="#" class="page-link"><i class="fas fa-chevron-right"></i></a>
                </div>
            </div>
        </section>

        <button class="write-btn" title="새 글 쓰기">
            <i class="fas fa-pen"></i>
        </button>
    </div>
</template>

<script setup>
// 파티클 생성 함수
import {onMounted} from 'vue'
import {RouterLink} from 'vue-router'
onMounted(() => {
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

    // 클릭 이벤트 (배경 파티클)
    document.addEventListener('click', (e) => {
        // 카드나 버튼 클릭 시에는 파티클 제외 (선택 사항)
        if(e.target.closest('.post-card') || e.target.closest('.write-btn')) return;

        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                const offsetX = (Math.random() - 0.5) * 40;
                const offsetY = (Math.random() - 0.5) * 40;
                createParticle(e.clientX + offsetX, e.clientY + offsetY);
            }, i * 50);
        }
    });

    // 탭 버튼 클릭 효과
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // 글쓰기 버튼 클릭
    document.querySelector('.write-btn').addEventListener('click', () => {
        alert('새로운 이야기를 작성하러 가볼까요? ✍️');
        // window.location.href = 'write.html'; // 나중에 글쓰기 페이지로 연결
    });

    // 좋아요 버튼 인터랙션 (간단 구현)
    document.querySelectorAll('.stat-item.likes').forEach(item => {
        item.addEventListener('click', function(e) {
            e.stopPropagation(); // 카드 클릭 방지
            
            // 간단한 토글 로직
            if(this.style.color === 'var(--pink)') {
                this.style.color = '';
                this.innerHTML = `<i class="fas fa-heart"></i> ${parseInt(this.innerText) - 1}`;
            } else {
                this.style.color = 'var(--pink)';
                this.innerHTML = `<i class="fas fa-heart"></i> ${parseInt(this.innerText) + 1}`;
                
                // 하트 파티클 효과
                const rect = this.getBoundingClientRect();
                for(let i=0; i<5; i++) {
                    createParticle(rect.left + 10, rect.top);
                }
            }
        });
    });
})
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

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Nunito', 'Jua', sans-serif;
    color: var(--text);
    background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
    overflow-x: hidden;
    min-height: 100vh;
}

/* -----------------------------------------------------------
    [1] 배경 애니메이션 (기존 유지)
    ----------------------------------------------------------- */
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

/* -----------------------------------------------------------
    [2] 헤더 네비게이션 (기존 유지)
    ----------------------------------------------------------- */
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
    animation: slide-down 0.6s ease-out;
}

@keyframes slide-down {
    from { transform: translateY(-100%); }
    to { transform: translateY(0); }
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
    animation: spring-in 0.8s ease-out;
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

@keyframes spring-in {
    0% { transform: scale(0) rotate(-180deg); opacity: 0; }
    60% { transform: scale(1.2) rotate(20deg); }
    80% { transform: scale(0.95) rotate(-10deg); }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
}

.nav-links a {
    color: var(--text);
    text-decoration: none;
    margin-left: 30px;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.3s;
    display: inline-block;
}

.nav-links a:hover {
    color: var(--primary);
    transform: translateY(-3px) scale(1.1);
}

.nav-links a.active {
    color: var(--secondary);
}

/* -----------------------------------------------------------
    [3] 커뮤니티 게시판 스타일 (New!)
    ----------------------------------------------------------- */
.board-section {
    padding: 40px 0 80px;
}

/* 상단 검색 및 타이틀 영역 */
.board-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 30px;
    flex-wrap: wrap;
    gap: 20px;
    animation: fade-in-up 0.6s ease-out;
}

@keyframes fade-in-up {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
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

/* 검색바 스타일 */
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

/* 카테고리 탭 */
.category-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    overflow-x: auto;
    padding-bottom: 10px; /* 스크롤바 공간 */
    animation: fade-in-up 0.6s ease-out 0.2s backwards;
}

.tab-btn {
    padding: 10px 20px;
    border-radius: 20px;
    border: 2px solid #E5E5E5;
    background: white;
    font-weight: 700;
    color: #888;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
    font-family: 'Nunito', 'Jua', sans-serif;
}

.tab-btn:hover {
    background: #F7F7F7;
    transform: translateY(-2px);
}

.tab-btn.active {
    background: var(--primary);
    border-color: var(--primary);
    color: white;
    box-shadow: 0 4px 10px rgba(88, 204, 2, 0.3);
}

/* 게시글 그리드 (카드형) */
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
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    cursor: pointer;
    animation: fade-in-up 0.6s ease-out backwards;
    position: relative;
    display: flex;
    flex-direction: column;
}

/* 카드 등장 딜레이 */
.post-card:nth-child(1) { animation-delay: 0.3s; }
.post-card:nth-child(2) { animation-delay: 0.35s; }
.post-card:nth-child(3) { animation-delay: 0.4s; }
.post-card:nth-child(4) { animation-delay: 0.45s; }
.post-card:nth-child(5) { animation-delay: 0.5s; }
.post-card:nth-child(6) { animation-delay: 0.55s; }

.post-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border-color: var(--secondary-light);
}

/* 카드 상단 (이미지/색상 영역) */
.card-header {
    height: 140px;
    background: linear-gradient(135deg, #F0F9FF 0%, #FFF9E5 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
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

/* 카드 내용 */
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
    line-height: 1.4;
    color: var(--text);
}

.card-excerpt {
    font-size: 0.95rem;
    color: #777;
    margin-bottom: 20px;
    line-height: 1.5;
    flex: 1; /* 남은 공간 차지 */
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

.author {
    display: flex;
    align-items: center;
    gap: 8px;
}

.author-avatar {
    width: 28px;
    height: 28px;
    background: #E5E5E5;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
}

.stats {
    display: flex;
    gap: 12px;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 5px;
    transition: color 0.2s;
}

.stat-item.likes:hover { color: var(--pink); }
.stat-item.comments:hover { color: var(--secondary); }

/* 글쓰기 버튼 (Floating Action Button 느낌) */
.write-btn {
    position: fixed;
    bottom: 40px;
    right: 40px;
    width: 65px;
    height: 65px;
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.8rem;
    box-shadow: 0 10px 25px rgba(88, 204, 2, 0.4);
    cursor: pointer;
    transition: all 0.3s;
    z-index: 1000;
    border: none;
}

.write-btn:hover {
    transform: scale(1.1) rotate(90deg);
    box-shadow: 0 15px 35px rgba(88, 204, 2, 0.5);
}

/* 페이지네이션 */
.pagination {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
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
    text-decoration: none;
    transition: all 0.2s;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.page-link:hover, .page-link.active {
    background: var(--purple);
    color: white;
    transform: translateY(-3px);
}

/* 모바일 대응 */
@media (max-width: 768px) {
    .nav-links { display: none; }
    .board-header { flex-direction: column; align-items: flex-start; }
    .search-wrapper { width: 100%; }
    .write-btn { width: 55px; height: 55px; bottom: 20px; right: 20px; font-size: 1.5rem; }
}
</style>