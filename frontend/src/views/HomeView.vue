<template>
  <div class="home-container">
    <div class="floating-shapes">
        <div class="shape" style="font-size: 100px;">🌟</div>
        <div class="shape" style="font-size: 80px;">📚</div>
        <div class="shape" style="font-size: 90px;">✨</div>
        <div class="shape" style="font-size: 70px;">🎈</div>
    </div>

    <header>
        <div class="container nav-wrapper">
            <div class="logo">
                <div class="logo-icon">📖</div>
                <span>Step-up Story</span>
            </div>
            <nav class="nav-links">
                <a href="#features">홈</a>
                <RouterLink :to="{name: 'community'}">커뮤니티</RouterLink>
                <a href="#team">학습 로드맵</a>
                <span v-if="!isLoggedIn">
                    <RouterLink :to="{name:'login'}" class="btn btn-primary start-btn">로그인</RouterLink>
                    <RouterLink :to="{name:'signup'}" class="btn btn-primary start-btn">회원가입</RouterLink>
                </span>
                <span v-else style="margin-left: 20px;">
                    <u><b><span style="color: blue;">{{ nickname }}</span>님 반갑습니다!</b></u>
                    <button class="btn btn-primary start-btn" @click="logoutHandler">로그아웃</button>
                </span>
                <RouterLink to="/story/create" class="btn btn-primary start-btn">시작하기</RouterLink>
            </nav>
        </div>
    </header>

    <section class="container hero">
        <div class="hero-text">
            <h1>AI가 만들어주는<br>우리 아이 맞춤형<br>영어 동화책 📚</h1>
            <p>
                매번 똑같은 교재는 이제 그만!<br>
                아이의 흥미와 수준을 분석해 <strong>매일 새로운 동화</strong>와<br>
                <strong>맞춤형 학습 플래너</strong>를 선물하세요 🎁
            </p>
            <div class="hero-buttons">
                <RouterLink to="/story/create" class="btn btn-primary">무료 레벨 테스트 시작 🚀</RouterLink>
                <a href="#features" class="btn btn-secondary">더 알아보기</a>
            </div>
        </div>
        <div class="hero-image">
            <div class="hero-mascot">
                <div class="mascot-face">🤖</div>
            </div>
            <div class="floating-icon">⭐</div>
            <div class="floating-icon">🎨</div>
            <div class="floating-icon">📝</div>
            <div class="floating-icon">🎯</div>
        </div>
    </section>

    <section id="features" class="features">
        <div class="container">
            <h2 class="section-title">✨ 왜 스텝업 스토리인가요?</h2>
            <div class="card-grid">
                <div class="card">
                    <div class="card-icon icon-green">
                        <i class="fas fa-calendar-check"></i>
                    </div>
                    <h3>AI 학습 플래너</h3>
                    <p>아이 수준을 진단해<br>주간·월간 학습 계획을<br>자동으로 짜드려요 📅</p>
                </div>
                <div class="card">
                    <div class="card-icon icon-yellow">
                        <i class="fas fa-book-open"></i>
                    </div>
                    <h3>나만의 맞춤 동화</h3>
                    <p>아이가 좋아하는 주제에<br>학습 목표 어휘를 쏙쏙 넣어<br>동화를 만들어요 🎨</p>
                </div>
                <div class="card">
                    <div class="card-icon icon-pink">
                        <i class="fas fa-microphone-alt"></i>
                    </div>
                    <h3>발음 피드백</h3>
                    <p>AI 선생님과 함께 읽어요<br>말하면 바로바로<br>발음을 고쳐줍니다 🎤</p>
                </div>
                <div class="card">
                    <div class="card-icon icon-blue">
                        <i class="fas fa-magic"></i>
                    </div>
                    <h3>자동 문제 생성</h3>
                    <p>읽은 동화 내용으로<br>퀴즈와 단어 카드가<br>자동으로 만들어져요 ✨</p>
                </div>
            </div>
        </div>
    </section>

    <section id="cycle" class="cycle-section">
        <div class="container">
            <h2 class="section-title">🚀 영어 실력이 쑥쑥 크는 과정</h2>
            
            <div class="path-container">
                <div class="step-row">
                    <div class="step-badge badge-green">
                        <i class="fas fa-search"></i>
                        <div class="step-number">STEP 1</div>
                    </div>
                    <div class="step-content">
                        <h4>🔍 진단 & 플래닝</h4>
                        <p>AI가 아이의 레벨과 관심사를 분석해<br>딱 맞는 목표를 세워요!</p>
                    </div>
                </div>

                <div class="step-row">
                    <div class="step-badge badge-blue">
                        <i class="fas fa-book-reader"></i>
                        <div class="step-number">STEP 2</div>
                    </div>
                    <div class="step-content">
                        <h4>📖 동화 읽기</h4>
                        <p>오늘 배워야 할 단어가 들어간<br>재미있는 동화를 읽어요!</p>
                    </div>
                </div>

                <div class="step-row">
                    <div class="step-badge badge-pink">
                        <i class="fas fa-comments"></i>
                        <div class="step-number">STEP 3</div>
                    </div>
                    <div class="step-content">
                        <h4>🎤 듣고 말하기</h4>
                        <p>원어민 발음을 듣고 따라하며<br>자신감을 키워요!</p>
                    </div>
                </div>

                <div class="step-row">
                    <div class="step-badge badge-yellow">
                        <i class="fas fa-star"></i>
                        <div class="step-number">STEP 4</div>
                    </div>
                    <div class="step-content">
                        <h4>⭐ 퀴즈 & 피드백</h4>
                        <p>맞춤 퀴즈를 풀고<br>실력을 확인해요!</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="team" class="team-section">
        <div class="container">
            <h2 class="section-title">함께 만드는 사람들 👨‍👩‍👧</h2>
            
            <div class="team-members">
                <div>
                    <div class="team-member member-1">👨‍💻</div>
                    <div class="team-name">김경민</div>
                </div>
                <div>
                    <div class="team-member member-2">👨‍💻</div>
                    <div class="team-name">민승환</div>
                </div>
                <div>
                    <div class="team-member member-3">👩‍💻</div>
                    <div class="team-name">정회지</div>
                </div>
            </div>
            
            <div class="tech-section">
                <p style="color:#999; font-size: 1.2rem; font-weight: 700; margin-bottom: 10px;">Powered by 🚀</p>
                <div class="tech-badges">
                    <span class="badge">🦜 LangChain</span>
                    <span class="badge">⚡ FastAPI</span>
                    <span class="badge">🤖 OpenAI</span>
                    <span class="badge">⚛️ Vue.js</span>
                    <span class="badge">🗄️ ChromaDB</span>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2024 Step-up Story. All rights reserved.</p>
        </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import {storeToRefs} from 'pinia'
import axios from 'axios'
import {useRouter} from 'vue-router'

const router = useRouter()
const store = useCounterStore()
const { isLoggedIn, nickname, refreshToken } = storeToRefs(store);

const logoutHandler = async () => {
    try {
        // 1. 서버에 리프레시 토큰을 보내 블랙리스트 등록
        await axios.post('http://localhost:8000/accounts/logout/', {
            refresh: refreshToken.value 
        });

        // 2. 스토어 및 로컬 정보 초기화
        store.logout()

        alert("로그아웃 되었습니다. 다음에 또 봐요! 👋");
        router.push('/');
    } catch (error) {
        console.error("로그아웃 실패:", error);
        // 서버 통신에 실패하더라도 일단 클라이언트 정보는 지우는 것이 안전합니다.
        alert("서버와의 연결이 불안정하여 로컬 세션을 강제로 종료합니다. 안전하게 로그아웃되었습니다. 🛡️")
        store.logout()
        router.push('/'); 
    }
}

// 별도의 로직은 없습니다.
</script>

<style scoped>
/* HTML의 style 태그 내용을 옮겨왔습니다.
  Vue의 scoped style로 적용하여 다른 페이지에 영향을 주지 않습니다.
*/

.home-container {
    font-family: 'Nunito', 'Jua', sans-serif;
    color: var(--text);
    /* body에 있던 배경 설정을 여기로 이동 */
    background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
    overflow-x: hidden;
    min-height: 100vh;
}

/* 떠다니는 배경 요소들 */
.floating-shapes {
    position: fixed;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.shape {
    position: absolute;
    opacity: 0.1;
    animation: float 20s infinite ease-in-out;
}

.shape:nth-child(1) { left: 10%; top: 20%; animation-delay: 0s; }
.shape:nth-child(2) { right: 10%; top: 40%; animation-delay: 4s; }
.shape:nth-child(3) { left: 5%; bottom: 20%; animation-delay: 8s; }
.shape:nth-child(4) { right: 15%; bottom: 30%; animation-delay: 12s; }

@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-30px) rotate(10deg); }
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
    z-index: 1;
}

/* 버튼 스타일 */
.btn {
    display: inline-block;
    padding: 16px 32px;
    font-size: 1.1rem;
    font-weight: 800;
    border-radius: 50px;
    border: none;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease;
    text-transform: uppercase;
    position: relative;
    letter-spacing: 0.5px;
    text-align: center;
}

.btn-primary {
    background: linear-gradient(180deg, var(--primary-light) 0%, var(--primary) 100%);
    color: white;
    box-shadow: 0 6px 0 var(--primary-dark), 0 10px 20px rgba(88, 204, 2, 0.3);
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 0 var(--primary-dark), 0 15px 30px rgba(88, 204, 2, 0.4);
}

.btn-primary:active {
    transform: translateY(3px);
    box-shadow: 0 3px 0 var(--primary-dark), 0 5px 10px rgba(88, 204, 2, 0.3);
}

.btn-secondary {
    background: white;
    color: var(--secondary);
    border: 4px solid var(--secondary);
    box-shadow: 0 6px 0 var(--secondary), 0 10px 20px rgba(28, 176, 246, 0.2);
}

.btn-secondary:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 0 var(--secondary), 0 15px 30px rgba(28, 176, 246, 0.3);
}

.btn-secondary:active {
    transform: translateY(3px);
    box-shadow: 0 3px 0 var(--secondary);
}

/* 헤더 */
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

.logo {
    font-size: 2rem;
    font-weight: 900;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text);
}

.logo-icon {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.nav-links a {
    color: var(--text);
    text-decoration: none;
    margin-left: 30px;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.3s;
    position: relative;
}

.nav-links a:hover {
    color: var(--primary);
    transform: translateY(-2px);
}

.start-btn {
    padding: 10px 20px;
    font-size: 0.9rem;
    margin-left: 20px;
}

/* 히어로 섹션 */
.hero {
    padding: 100px 0;
    display: flex;
    align-items: center;
    gap: 60px;
}

.hero-text { flex: 1; }

.hero h1 {
    font-size: 4rem;
    line-height: 1.2;
    margin-bottom: 25px;
    font-weight: 900;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero p {
    font-size: 1.4rem;
    color: #666;
    margin-bottom: 40px;
    line-height: 1.8;
    font-weight: 600;
}

.hero-buttons {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.hero-image {
    flex: 1;
    position: relative;
}

.hero-mascot {
    width: 100%;
    max-width: 450px;
    height: 450px;
    background: linear-gradient(135deg, #DDF4FF 0%, #B8E6FF 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: 0 20px 60px rgba(28, 176, 246, 0.3);
    animation: float 4s infinite ease-in-out;
}

.mascot-face {
    font-size: 12rem;
    animation: wave 2s infinite;
}

@keyframes wave {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(10deg); }
    75% { transform: rotate(-10deg); }
}

.floating-icon {
    position: absolute;
    font-size: 2rem;
    animation: float 3s infinite ease-in-out;
}

.floating-icon:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.floating-icon:nth-child(2) { top: 20%; right: 15%; animation-delay: 1s; }
.floating-icon:nth-child(3) { bottom: 20%; left: 5%; animation-delay: 2s; }
.floating-icon:nth-child(4) { bottom: 15%; right: 10%; animation-delay: 1.5s; }

/* 특징 카드 섹션 */
.features {
    padding: 100px 0;
    background: white;
}

.section-title {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 60px;
    font-weight: 900;
    color: var(--text);
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 40px;
}

.card {
    background: white;
    border-radius: 30px;
    padding: 40px;
    text-align: center;
    transition: all 0.3s ease;
    border: 4px solid transparent;
    position: relative;
    cursor: pointer;
}

.card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 30px;
    padding: 4px;
    background: linear-gradient(135deg, var(--primary), var(--secondary), var(--pink), var(--purple));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.3s;
}

.card:hover::before { opacity: 1; }

.card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.card-icon {
    width: 100px;
    height: 100px;
    margin: 0 auto 25px;
    border-radius: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    animation: bounce 2s infinite;
}

.icon-green { background: linear-gradient(135deg, #58CC02, #89E152); color: white; }
.icon-yellow { background: linear-gradient(135deg, #FFC800, #FFE066); color: white; }
.icon-pink { background: linear-gradient(135deg, #FF6B9D, #FF9DBE); color: white; }
.icon-blue { background: linear-gradient(135deg, #1CB0F6, #58D3FF); color: white; }

.card h3 {
    margin: 20px 0 15px;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text);
}

.card p {
    color: #666;
    line-height: 1.7;
    font-size: 1.1rem;
    font-weight: 600;
}

/* 학습 사이클 */
.cycle-section {
    padding: 100px 0;
    background: linear-gradient(180deg, #F0F9FF 0%, #E0F2FE 100%);
    position: relative;
    overflow: hidden;
}

.path-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 0;
}

.step-row {
    display: flex;
    align-items: center;
    margin-bottom: 80px;
    gap: 40px;
}

.step-row:nth-child(even) { flex-direction: row-reverse; }

.step-badge {
    min-width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    position: relative;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.step-badge::after {
    content: '';
    position: absolute;
    width: 140%;
    height: 140%;
    border-radius: 50%;
    border: 4px dashed currentColor;
    opacity: 0.3;
    animation: rotate 10s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.badge-green { background: linear-gradient(135deg, #58CC02, #89E152); }
.badge-blue { background: linear-gradient(135deg, #1CB0F6, #58D3FF); }
.badge-pink { background: linear-gradient(135deg, #FF6B9D, #FF9DBE); }
.badge-yellow { background: linear-gradient(135deg, #FFC800, #FFE066); }

.step-number {
    font-size: 1rem;
    font-weight: 800;
    margin-top: 5px;
}

.step-content {
    flex: 1;
    background: white;
    padding: 35px;
    border-radius: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 4px solid #E5E5E5;
    transition: all 0.3s;
}

.step-content:hover {
    transform: translateX(10px);
    border-color: var(--secondary);
    box-shadow: 0 15px 40px rgba(28, 176, 246, 0.2);
}

.step-row:nth-child(even) .step-content:hover {
    transform: translateX(-10px);
}

.step-content h4 {
    margin: 0 0 15px;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text);
}

.step-content p {
    margin: 0;
    color: #666;
    font-size: 1.1rem;
    line-height: 1.7;
    font-weight: 600;
}

/* 팀 섹션 */
.team-section {
    padding: 100px 0;
    text-align: center;
    background: white;
}

.team-members {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin: 50px 0;
    flex-wrap: wrap;
}

.team-member {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    transition: all 0.3s;
    cursor: pointer;
}

.member-1 { background: linear-gradient(135deg, var(--primary), var(--secondary)); }
.member-2 { background: linear-gradient(135deg, var(--pink), var(--purple)); }
.member-3 { background: linear-gradient(135deg, var(--orange), var(--yellow)); }

.team-member:hover {
    transform: translateY(-10px) rotate(5deg);
}

.team-name {
    font-size: 1.2rem;
    font-weight: 800;
    margin-top: 15px;
    color: var(--text);
}

.tech-section {
    margin-top: 70px;
    padding: 50px;
    background: linear-gradient(135deg, #F0F9FF, #FFF9E5);
    border-radius: 40px;
}

.tech-badges {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 30px;
}

.badge {
    background: white;
    padding: 12px 24px;
    border-radius: 50px;
    font-weight: 800;
    color: var(--text);
    font-size: 1rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
    border: 3px solid transparent;
}

.badge:hover {
    transform: translateY(-5px) scale(1.1);
    border-color: var(--primary);
    box-shadow: 0 10px 25px rgba(88, 204, 2, 0.3);
}

footer {
    padding: 60px 0;
    text-align: center;
    background: linear-gradient(180deg, #FFFFFF 0%, #F9FAFB 100%);
    color: #999;
    font-size: 1rem;
    font-weight: 600;
}

</style>