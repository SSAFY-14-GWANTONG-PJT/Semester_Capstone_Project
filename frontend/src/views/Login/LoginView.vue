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
                    <a href="index.html#features">주요 기능</a>
                    <a href="index.html#cycle">학습 로드맵</a>
                    <a href="index.html#team">팀 소개</a>
                    <RouterLink to="/signup" style="color: var(--secondary);">
                      회원가입
                    </RouterLink>
                </nav>
            </div>
        </header>

        <section class="login-section">
            <div class="container">
                <div class="login-content">
                    
                    <div class="login-form-container">
                        <div class="login-box">
                            <h1 class="login-title">로그인</h1>
                            <p class="login-subtitle">영어 학습 여행을 계속해볼까요? 🚀</p>

                            <form id="loginForm" @submit.prevent="loginHandler">
                                <div class="form-group">
                                    <label for="email">이메일</label>
                                    <div class="input-wrapper">
                                        <input type="email" id="email" placeholder="example@email.com" required v-model="loginForm.email">
                                        <i class="fas fa-envelope input-icon"></i>
                                    </div>
                                </div>

                                <div class="form-group">
                                    <label for="password">비밀번호</label>
                                    <div class="input-wrapper">
                                        <input type="password" id="password" placeholder="••••••••" required v-model="loginForm.password">
                                        <i class="fas fa-lock input-icon"></i>
                                    </div>
                                </div>

                                <div class="form-options">
                                    <label class="remember-me">
                                        <input type="checkbox" id="remember">
                                        <span>로그인 상태 유지</span>
                                    </label>
                                    <a href="#" class="forgot-password">비밀번호 찾기</a>
                                </div>

                                <button type="submit" form="loginForm" class="btn btn-primary">
                                    로그인 🎯
                                </button>
                            </form>

                            <!-- <div class="divider">
                                <span>또는</span>
                            </div>

                            <div class="social-login">
                                <button class="social-btn google" title="Google로 로그인">
                                    <i class="fab fa-google"></i>
                                </button>
                                <button class="social-btn kakao" title="카카오로 로그인">
                                    <i class="fas fa-comment"></i>
                                </button>
                                <button class="social-btn naver" title="네이버로 로그인">
                                    <strong>N</strong>
                                </button>
                            </div> -->

                            <div class="signup-link">
                                아직 계정이 없으신가요? <a href="signUp.html">회원가입 하기</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script setup>
import {reactive, onMounted, onUnmounted} from'vue'
import {useRouter} from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const store = useCounterStore()

const router = useRouter()

const loginForm = reactive({
    email: '',
    password: ''
})

const loginHandler = async () => {
    if (!loginForm.email || !loginForm.password) {
        alert("이메일과 비밀번호를 모두 입력해주세요.")
        return;
    }

    axios.post('http://localhost:8000/accounts/login/', {
        email: loginForm.email,
        password: loginForm.password
    })
    .then(response => {
        store.login(response.data.token, response.data.nickname)
        router.push('/')
    })
    .catch(error => {
        console.error("로그인 실패:", error);
        alert("이메일 또는 비밀번호가 틀렸습니다.");
    })
}

onMounted(() => {
    const createParticle = (x, y) => {
        const emojis = ['⭐', '✨', '💫', '🌟', '🎉', '💖'];
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        document.body.appendChild(particle);

        setTimeout(() => particle.remove(), 1000);
    }

    // 2. 클릭 이벤트 리스너
    const clickListener = (e) => {
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                const offsetX = (Math.random() - 0.5) * 40;
                const offsetY = (Math.random() - 0.5) * 40;
                createParticle(e.clientX + offsetX, e.clientY + offsetY);
            }, i * 50);
        }
    }
    document.addEventListener('click', clickListener);

    // 3. 인풋 애니메이션
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            const label = this.parentElement.parentElement.querySelector('label');
            if(label) {
                label.style.color = 'var(--primary)';
                label.style.transform = 'scale(1.05)';
            }
        });
        
        input.addEventListener('blur', function() {
            const label = this.parentElement.parentElement.querySelector('label');
            if(label) {
                label.style.color = 'var(--text)';
                label.style.transform = 'scale(1)';
            }
        });
    });

    onUnmounted(() => {
        document.removeEventListener('click', clickListener);
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
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Nunito', 'Jua', sans-serif;
    color: var(--text);
    background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
    overflow-x: hidden;
}

/* 떠다니는 배경 */
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

/* 컨테이너 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
    z-index: 1;
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

.logo {
    font-size: 2rem;
    font-weight: 900;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text);
    text-decoration: none;
    animation: spring-in 0.8s ease-out;
}

@keyframes spring-in {
    0% { transform: scale(0) rotate(-180deg); opacity: 0; }
    60% { transform: scale(1.2) rotate(20deg); }
    80% { transform: scale(0.95) rotate(-10deg); }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
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
    animation: bounce-rotate 2s infinite;
}

@keyframes bounce-rotate {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-10px) rotate(-5deg); }
    50% { transform: translateY(0) rotate(0deg); }
    75% { transform: translateY(-5px) rotate(5deg); }
}

.nav-links a {
    color: var(--text);
    text-decoration: none;
    margin-left: 30px;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    position: relative;
    display: inline-block;
}

.nav-links a:hover {
    color: var(--primary);
    transform: translateY(-3px) scale(1.1);
}

/* 로그인 섹션 */
.login-section {
    min-height: calc(100vh - 100px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 60px 0 80px;
}

/* ----------------------------------------------------
[수정됨] 로그인 컨텐츠 너비 및 배치 수정
- 로봇 삭제 후 단일 컬럼으로 변경
- 너비를 회원가입 페이지와 동일한 550px로 고정
---------------------------------------------------- */
.login-content {
    display: flex;
    flex-direction: column; /* 세로 배치 */
    align-items: center;
    justify-content: center;
    width: 550px;
    max-width: 1000px;       /* 회원가입 페이지와 동일한 너비 */
    margin: 0 auto;
}

/* 로그인 폼 컨테이너 */
.login-form-container {
    width: 100%;
    animation: zoom-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55); /* 회원가입 페이지 애니메이션 적용 */
}

@keyframes zoom-in {
    from { opacity: 0; transform: scale(0.8); }
    to { opacity: 1; transform: scale(1); }
}

.login-box {
    background: white;
    border-radius: 40px;
    padding: 50px 45px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
    border: 4px solid transparent;
    position: relative;
}

.login-box::before {
    content: '';
    position: absolute;
    inset: -4px;
    border-radius: 40px;
    padding: 4px;
    background: linear-gradient(135deg, var(--primary), var(--secondary), var(--pink));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}

.login-title {
    font-size: 2.5rem;
    font-weight: 900;
    margin-bottom: 10px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center; /* 타이틀 중앙 정렬 */
}

.login-subtitle {
    font-size: 1.1rem;
    color: #999;
    margin-bottom: 35px;
    font-weight: 600;
    text-align: center; /* 서브타이틀 중앙 정렬 */
}

/* 폼 그룹 */
.form-group {
    margin-bottom: 25px;
    animation: slide-up 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) backwards;
}

.form-group:nth-child(1) { animation-delay: 0.4s; }
.form-group:nth-child(2) { animation-delay: 0.5s; }

@keyframes slide-up {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 700;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s;
}

.input-wrapper {
    position: relative;
}

.input-icon {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.2rem;
    color: var(--secondary);
    transition: all 0.3s;
}

input {
    width: 100%;
    padding: 18px 20px 18px 55px;
    border: 3px solid #E5E5E5;
    border-radius: 25px;
    font-size: 1rem;
    font-family: 'Nunito', sans-serif;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    outline: none;
}

input:focus {
    border-color: var(--secondary);
    box-shadow: 0 5px 20px rgba(28, 176, 246, 0.2);
    transform: translateY(-2px);
}

input:focus + .input-icon {
    color: var(--primary);
    transform: translateY(-50%) scale(1.2);
}

/* 옵션 */
.form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    font-size: 0.9rem;
    animation: slide-up 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.6s backwards;
}

.remember-me {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-weight: 600;
}

.remember-me input[type="checkbox"] {
    width: auto;
    cursor: pointer;
    accent-color: var(--primary);
}

.forgot-password {
    color: var(--secondary);
    text-decoration: none;
    font-weight: 700;
    transition: all 0.3s;
}

.forgot-password:hover {
    color: var(--primary);
}

/* 버튼 */
.btn {
    width: 100%;
    padding: 18px;
    font-size: 1.2rem;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    border-radius: 25px;
    border: none;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    animation: slide-up 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.7s backwards;
    cursor: pointer; /* 커서 추가 */
    
    position: relative;  /* 위치 기준 잡기 */
    z-index: 10;         /* 다른 요소보다 위에 배치 */
}


.btn-primary {
    background: linear-gradient(135deg, var(--primary-light), var(--primary));
    color: white;
    box-shadow: 0 8px 0 var(--primary-dark), 0 12px 25px rgba(88, 204, 2, 0.4);
    margin-bottom: 15px;
}

.btn-primary:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 0 var(--primary-dark), 0 16px 35px rgba(88, 204, 2, 0.5);
}

.btn-primary:active {
    transform: translateY(4px);
    box-shadow: 0 4px 0 var(--primary-dark);
}

/* 구분선 */
.divider {
    display: flex;
    align-items: center;
    margin: 30px 0;
    animation: slide-up 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.8s backwards;
}

.divider::before,
.divider::after {
    content: '';
    flex: 1;
    height: 2px;
    background: linear-gradient(to right, transparent, #E5E5E5, transparent);
}

.divider span {
    padding: 0 15px;
    color: #999;
    font-weight: 600;
    font-size: 0.9rem;
}

/* 소셜 로그인 */
.social-login {
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
    animation: slide-up 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.9s backwards;
}

.social-btn {
    flex: 1;
    padding: 15px;
    border: 3px solid #E5E5E5;
    border-radius: 20px;
    background: white;
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    font-size: 1.5rem;
    cursor: pointer;
}

.social-btn:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.social-btn.google { color: #DB4437; }
.social-btn.google:hover { border-color: #DB4437; }

.social-btn.kakao { color: #FEE500; background: #FEE500; }
.social-btn.kakao:hover { box-shadow: 0 10px 25px rgba(254, 229, 0, 0.3); }

.social-btn.naver { color: #03C75A; }
.social-btn.naver:hover { border-color: #03C75A; }

/* 회원가입 링크 */
.signup-link {
    text-align: center;
    font-size: 1rem;
    font-weight: 600;
    color: #666;
    animation: slide-up 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 1s backwards;
}

.signup-link a {
    color: var(--secondary);
    text-decoration: none;
    font-weight: 800;
    transition: all 0.3s;
}

.signup-link a:hover {
    color: var(--primary);
}

/* 파티클 */

/* 모바일 대응 */
@media (max-width: 768px) {
    .nav-links { display: none; }
    .login-box { padding: 40px 30px; }
    .login-title { font-size: 2rem; }
}
</style>

<style>
/* 1. 폰트 불러오기 (전역) */
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Nunito:wght@600;700;800;900&display=swap');

/* 2. 색상 변수 (모든 페이지 공통 사용) */
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
}

/* 3. 기본 리셋 */
* { box-sizing: border-box; margin: 0; padding: 0; }

/* 4. 바디 스타일 (중요! scoped에 있으면 배경 적용 안됨) */
body {
    font-family: 'Nunito', 'Jua', sans-serif;
    color: var(--text);
    background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
    overflow-x: hidden;
}

.particle {
    position: fixed;
    pointer-events: none;
    z-index: 9999;
    font-size: 24px;
    animation: particle-float 1s ease-out forwards;
}

@keyframes particle-float {
    0% {
        opacity: 1;
        transform: translateY(0) scale(1) rotate(0deg);
    }
    100% {
        opacity: 0;
        transform: translateY(-100px) scale(0.5) rotate(360deg);
    }
}
</style>