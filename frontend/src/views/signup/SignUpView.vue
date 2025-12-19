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

        <section class="signup-section">
            <div class="container">
                <div class="signup-container" style="margin: 0 auto;">
                    <div class="signup-box">
                        <div class="logo">
                            <div class="logo-icon">🌟</div>
                            <h1>환영합니다!</h1>
                            <p>Step-up Story와 함께 영어 여행을 시작해요</p>
                        </div>

                        <form id="signupForm" @submit.prevent="signUpHandler">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="name">닉네임</label>
                                    <div class="input-wrapper">
                                        <input type="text" id="name" placeholder="ex. 우주최강용사" required v-model="signUpForm.nickname">
                                        <i class="fas fa-user input-icon"></i>
                                    </div>
                                </div>

                                <!-- <div class="form-group">
                                    <label for="birthdate">생년월일</label>
                                    <div class="input-wrapper">
                                        <input type="date" id="birthdate" required>
                                        <i class="fas fa-calendar input-icon"></i>
                                    </div>
                                </div> -->
                            </div>

                            <div class="form-group">
                                <label for="email">이메일</label>
                                <div class="input-wrapper">
                                    <input type="email" id="email" placeholder="example@email.com" required v-model="signUpForm.email">
                                    <i class="fas fa-envelope input-icon"></i>
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="password">비밀번호</label>
                                <div class="input-wrapper">
                                    <input type="password" id="password" placeholder="8자 이상 입력해주세요" required v-model="signUpForm.password">
                                    <i class="fas fa-lock input-icon"></i>
                                </div>
                                <div class="password-strength" id="passwordStrength">
                                    <div class="password-strength-bar" id="strengthBar"></div>
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="passwordConfirm">비밀번호 확인</label>
                                <div class="input-wrapper">
                                    <input type="password" id="passwordConfirm" placeholder="비밀번호를 다시 입력해주세요" required>
                                    <i class="fas fa-check-circle input-icon"></i>
                                </div>
                            </div>

                            <div class="form-row">
                                <!-- <div class="form-group">
                                    <label for="childName">아이 이름</label>
                                    <div class="input-wrapper">
                                        <input type="text" id="childName" placeholder="아이 이름" required>
                                        <i class="fas fa-child input-icon"></i>
                                    </div>
                                </div> -->

                                <div class="form-group">
                                    <label for="childAge">아이 나이</label>
                                    <div class="input-wrapper">
                                        <select id="childAge" required v-model="signUpForm.age">
                                            <option value="">선택</option>
                                            <option value="3">3세</option>
                                            <option value="4">4세</option>
                                            <option value="5">5세</option>
                                            <option value="6">6세</option>
                                            <option value="7">7세</option>
                                            <option value="8">8세</option>
                                            <option value="9">9세</option>
                                            <option value="10">10세</option>
                                        </select>
                                        <i class="fas fa-birthday-cake input-icon"></i>
                                    </div>
                                </div>

                                <div class="form-group">
                                    <label for="level">Level</label>
                                    <div class="input-wrapper">
                                        <select id="level" required v-model="signUpForm.level">
                                            <option value="">선택</option>
                                            <option value="1">Lv.1</option>
                                            <option value="2">Lv.2</option>
                                            <option value="3">Lv.3</option>
                                            <option value="4">Lv.4</option>
                                            <option value="5">Lv.5</option>
                                            <option value="6">Lv.6</option>
                                            <option value="7">Lv.7</option>
                                            <option value="8">Lv.8</option>
                                            <option value="9">Lv.9</option>
                                            <option value="10">Lv.10</option>
                                        </select>
                                        <i class="fas fa-layer-group input-icon"></i>
                                    </div>
                                </div>
                            </div>

                            <div class="terms">
                                <div class="terms-item all-agree">
                                    <input type="checkbox" id="agreeAll">
                                    <label for="agreeAll">모두 동의합니다</label>
                                </div>
                                <div class="terms-item">
                                    <input type="checkbox" class="agree-item" id="agree1">
                                    <label for="agree1">[필수] 만 14세 이상입니다</label>
                                </div>
                                <div class="terms-item">
                                    <input type="checkbox" class="agree-item" id="agree2">
                                    <label for="agree2">[필수] 이용약관 동의</label>
                                </div>
                                <div class="terms-item">
                                    <input type="checkbox" class="agree-item" id="agree3">
                                    <label for="agree3">[필수] 개인정보 수집 및 이용 동의</label>
                                </div>
                                <div class="terms-item">
                                    <input type="checkbox" class="agree-item" id="agree4">
                                    <label for="agree4">[선택] 마케팅 정보 수신 동의</label>
                                </div>
                            </div>

                            <div class="btn-group">
                                <a href="" class="btn btn-secondary">취소</a>
                                <button type="submit" class="btn btn-primary">가입하기 🎉</button>
                            </div>
                        </form>

                        <div class="login-link">
                            이미 계정이 있으신가요? <a href="">로그인 하기</a>
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

const router = useRouter()
const store = useCounterStore()

const signUpForm = reactive({
    nickname: '',
    email: '',
    password: '',
    age: 0,
    level: 0,
})

const signUpHandler = async () => {
    if (!signUpForm.nickname || !signUpForm.email || !signUpForm.password || !signUpForm.age || !signUpForm.level) {
        alert("비어있는 항목을 채워주세요.")
        return;
    }

    axios.post('/api/accounts/signup/', {
        nickname: signUpForm.nickname,
        email: signUpForm.email,
        password: signUpForm.password,
        age: signUpForm.age,
        level: signUpForm.level
    })
    .then(response => {
        store.login(
            response.data.token, 
            response.data.refreshToken,
            response.data.nickname
        )
        router.push('/')
    })
    .catch(error => {
        console.error("회원가입 실패:", error);
        alert("회원가입에 실패했습니다. 다시 시도해주세요.");
    })
}

function createParticle(x, y) {
    const emojis = ['🎉', '🎊', '⭐', '✨', '💫', '🌟', '💖', '🎈'];
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    particle.style.left = x + 'px';
    particle.style.top = y + 'px';
    document.body.appendChild(particle);

    setTimeout(() => particle.remove(), 1000);
}

onMounted(() => {
    // 클릭 이벤트 (파티클)
    document.addEventListener('click', (e) => {
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                const offsetX = (Math.random() - 0.5) * 40;
                const offsetY = (Math.random() - 0.5) * 40;
                createParticle(e.clientX + offsetX, e.clientY + offsetY);
            }, i * 50);
        }
    });

    // 로고 클릭 효과
    const logoIcon = document.querySelector('.logo-icon');
    if (logoIcon) { // 안전하게 있는지 확인
        logoIcon.addEventListener('click', (e) => {
            e.stopPropagation();
            for (let i = 0; i < 12; i++) {
                setTimeout(() => {
                    const angle = (Math.PI * 2 * i) / 12;
                    const distance = 70;
                    const x = e.clientX + Math.cos(angle) * distance;
                    const y = e.clientY + Math.sin(angle) * distance;
                    createParticle(x, y);
                }, i * 25);
            }
        });
    }

    // 비밀번호 강도 체크
    const passwordInput = document.getElementById('password');
    const strengthIndicator = document.getElementById('passwordStrength');
    const strengthBar = document.getElementById('strengthBar');

    if (passwordInput && strengthIndicator && strengthBar) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            strengthIndicator.classList.add('show');

            if (password.length === 0) {
                strengthIndicator.classList.remove('show');
                return;
            }

            let strength = 0;
            if (password.length >= 8) strength++;
            if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
            if (/\d/.test(password)) strength++;
            if (/[^a-zA-Z\d]/.test(password)) strength++;

            strengthBar.className = 'password-strength-bar';
            if (strength <= 1) {
                strengthBar.classList.add('weak');
            } else if (strength <= 2) {
                strengthBar.classList.add('medium');
            } else {
                strengthBar.classList.add('strong');
            }
        });
    }

    // 전체 동의 체크박스 로직
    const agreeAll = document.getElementById('agreeAll');
    const agreeItems = document.querySelectorAll('.agree-item');

    if (agreeAll) {
        agreeAll.addEventListener('change', function() {
            agreeItems.forEach(item => {
                item.checked = this.checked;
            });
        });
    }

    agreeItems.forEach(item => {
        item.addEventListener('change', function() {
            const allChecked = Array.from(agreeItems).every(i => i.checked);
            if (agreeAll) agreeAll.checked = allChecked;
        });
    });

    // 인풋 포커스 시 라벨 애니메이션
    document.querySelectorAll('input, select').forEach(input => {
        input.addEventListener('focus', function() {
            const label = this.closest('.form-group')?.querySelector('label');
            if (label) {
                label.style.color = 'var(--purple)';
                label.style.transform = 'scale(1.05)';
            }
        });
        
        input.addEventListener('blur', function() {
            const label = this.closest('.form-group')?.querySelector('label');
            if (label) {
                label.style.color = 'var(--text)';
                label.style.transform = 'scale(1)';
            }
        });
    });

    // 폼 제출
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const requiredAgree = document.querySelectorAll('.agree-item[required]');
            const allAgreed = Array.from(requiredAgree).every(item => item.checked);
            
            if (!allAgreed) {
                alert('필수 약관에 모두 동의해주세요! 📝');
                return;
            }

            const password = document.getElementById('password').value;
            const passwordConfirm = document.getElementById('passwordConfirm').value;
            
            if (password !== passwordConfirm) {
                alert('비밀번호가 일치하지 않습니다! 🔒');
                return;
            }

            const btn = e.target.querySelector('.btn-primary');
            btn.textContent = '가입 중... 🚀';
            btn.style.background = 'linear-gradient(135deg, var(--secondary-light), var(--secondary))';
            
            for (let i = 0; i < 30; i++) {
                setTimeout(() => {
                    const x = Math.random() * window.innerWidth;
                    const y = Math.random() * window.innerHeight;
                    createParticle(x, y);
                }, i * 50);
            }

            setTimeout(() => {
                btn.textContent = '가입 완료! ✨';
                btn.style.background = 'linear-gradient(135deg, var(--primary-light), var(--primary))';
                
                setTimeout(() => {
                    router.push('/');
                }, 1500);
            }, 2000);
        });
    }
});
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

/* 배경 애니메이션 */
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

/* 헤더 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
    z-index: 1;
}


/* 회원가입 섹션 */
.signup-section {
    min-height: calc(100vh - 100px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 60px 0 80px;
}

.signup-container {
    width: 550px;
    animation: zoom-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes zoom-in {
    from { opacity: 0; transform: scale(0.8); }
    to { opacity: 1; transform: scale(1); }
}

.signup-box {
    background: white;
    border-radius: 40px;
    padding: 50px 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    position: relative;
    /* overflow: hidden; <--- 삭제됨 (테두리 보이게 하기 위해) */
    border: 4px solid transparent;
    z-index: 1;
}

/* 테두리 그라데이션 */
.signup-box::before {
    content: '';
    position: absolute;
    inset: -4px;
    border-radius: 40px;
    padding: 4px;
    background: linear-gradient(135deg, var(--primary), var(--secondary), var(--pink), var(--purple));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}

/* 로고 */
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

@keyframes bounce-in {
    0% { transform: scale(0) rotate(-180deg); opacity: 0; }
    60% { transform: scale(1.1) rotate(10deg); }
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

@keyframes rotate-logo {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(5deg) scale(1.05); }
}

.logo h1 {
    font-size: 1.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--pink), var(--purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 5px;
}

.logo p {
    font-size: 0.9rem;
    color: #999;
    font-weight: 600;
}

/* 폼 스타일 */
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.form-group {
    margin-bottom: 20px;
    animation: slide-right 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) backwards;
}

/* 순차적 등장 애니메이션 (항목이 늘어나서 딜레이 추가) */
.form-group:nth-child(1) { animation-delay: 0.3s; }
.form-group:nth-child(2) { animation-delay: 0.35s; }
.form-group:nth-child(3) { animation-delay: 0.4s; }
.form-group:nth-child(4) { animation-delay: 0.45s; }
.form-group:nth-child(5) { animation-delay: 0.5s; }
.form-group:nth-child(6) { animation-delay: 0.55s; } /* 추가됨 */

@keyframes slide-right {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 700;
    color: var(--text);
    font-size: 0.95rem;
    transition: all 0.3s;
}

.input-wrapper { position: relative; }

.input-icon {
    position: absolute;
    left: 18px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.1rem;
    color: var(--purple);
    transition: all 0.3s;
}

input, select {
    width: 100%;
    padding: 15px 18px 15px 50px;
    border: 3px solid #E5E5E5;
    border-radius: 20px;
    font-size: 0.95rem;
    font-family: 'Nunito', sans-serif;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    outline: none;
    background: white;
}

select {
    appearance: none;
    background-image: url('data:image/svg+xml;charset=UTF-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23CE82FF"><path d="M7 10l5 5 5-5z"/></svg>');
    background-repeat: no-repeat;
    background-position: right 15px center;
    background-size: 24px;
    cursor: pointer;
}

input:focus, select:focus {
    border-color: var(--purple);
    box-shadow: 0 5px 20px rgba(206, 130, 255, 0.2);
    transform: translateY(-2px);
}

input:focus + .input-icon, select:focus + .input-icon {
    color: var(--pink);
    transform: translateY(-50%) scale(1.2);
}

.terms {
    margin: 25px 0;
    padding: 20px;
    background: linear-gradient(135deg, #FFF9E5, #F0F9FF);
    border-radius: 20px;
    animation: slide-right 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.6s backwards;
}

.terms-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: transform 0.3s;
}

.terms-item:hover { transform: translateX(5px); }
.terms-item:last-child { margin-bottom: 0; }

.terms-item input[type="checkbox"] {
    width: 20px;
    height: 20px;
    padding: 0;
    cursor: pointer;
    accent-color: var(--purple);
}

.terms-item label { margin: 0; font-size: 0.9rem; cursor: pointer; }

.terms-item.all-agree {
    font-weight: 800;
    color: var(--purple);
    padding-bottom: 12px;
    border-bottom: 2px solid #E5E5E5;
    margin-bottom: 15px;
}

.btn-group {
    display: flex;
    gap: 15px;
    animation: slide-right 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.65s backwards;
}

.btn {
    flex: 1;
    padding: 18px;
    font-size: 1.1rem;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    border-radius: 25px;
    border: none;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    text-decoration: none;
    display: inline-block;
    text-align: center;
    position: relative;  /* 위치 기준 잡기 */
    z-index: 10;
}

.btn-primary {
    background: linear-gradient(135deg, var(--pink), var(--purple));
    color: white;
    box-shadow: 0 8px 0 #9B5FCC, 0 12px 25px rgba(206, 130, 255, 0.4);
}

.btn-primary:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 0 #9B5FCC, 0 16px 35px rgba(206, 130, 255, 0.5);
}

.btn-primary:active {
    transform: translateY(4px);
    box-shadow: 0 4px 0 #9B5FCC;
}

.btn-secondary {
    background: white;
    color: var(--purple);
    border: 3px solid var(--purple);
    box-shadow: 0 6px 0 #9B5FCC;
}

.btn-secondary:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 0 #9B5FCC;
}

.btn-secondary:active {
    transform: translateY(3px);
    box-shadow: 0 3px 0 #9B5FCC;
}

.login-link {
    text-align: center;
    margin-top: 25px;
    font-size: 1rem;
    font-weight: 600;
    color: #666;
    animation: slide-right 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.7s backwards;
}

.login-link a {
    color: var(--purple);
    text-decoration: none;
    font-weight: 800;
    transition: all 0.3s;
}

.login-link a:hover {
    color: var(--pink);
    transform: scale(1.05);
    display: inline-block;
}

/* 비밀번호 강도 */
.password-strength {
    margin-top: 8px;
    height: 4px;
    background: #E5E5E5;
    border-radius: 2px;
    overflow: hidden;
    opacity: 0;
    transition: opacity 0.3s;
}

.password-strength.show { opacity: 1; }

.password-strength-bar {
    height: 100%;
    width: 0;
    transition: all 0.3s;
    border-radius: 2px;
}

.password-strength-bar.weak { width: 33%; background: var(--pink); }
.password-strength-bar.medium { width: 66%; background: var(--orange); }
.password-strength-bar.strong { width: 100%; background: var(--primary); }

/* 파티클 */
.particle {
    position: fixed;
    pointer-events: none;
    z-index: 9999;
    font-size: 24px;
    animation: particle-float 1s ease-out forwards;
}

@keyframes particle-float {
    0% { opacity: 1; transform: translateY(0) scale(1) rotate(0deg); }
    100% { opacity: 0; transform: translateY(-100px) scale(0.5) rotate(360deg); }
}

/* 모바일 대응 */
@media (max-width: 768px) {
    .nav-links { display: none; }
    .signup-box { padding: 40px 25px; }
    .form-row { grid-template-columns: 1fr; }
    input, select { padding: 14px 16px 14px 45px; }
    .btn-group { flex-direction: column; }
}
</style>
