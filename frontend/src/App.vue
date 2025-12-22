<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import axios from '@/api/index.js'

const store = useCounterStore()

onMounted(() => {
  // 앱 시작 시 저장된 다크모드 상태를 실제 DOM에 반영
  store.applyTheme()
})

// 로직 추가: 스토어에서 상태 가져오기
const router = useRouter()
const { isLoggedIn, nickname, refreshToken } = storeToRefs(store)

// 로그아웃 핸들러 추가
const logoutHandler = async () => {
    try {
        // 1. 서버에 리프레시 토큰을 보내 블랙리스트 등록
        await axios.post('http://localhost:8000/api/accounts/logout/', {
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
</script>

<template>
  <div class="global-zoom-container">
    <header>
      <div class="container nav-wrapper">
        <RouterLink to="/" class="logo">
            <div class="logo-icon">📖</div>
            <span>Step-up Story</span>
        </RouterLink>
        <nav class="nav-links">
          <div class="menu-items">
            <RouterLink to="/" class="menu1">홈</RouterLink>
            <RouterLink :to="{name: 'community'}" class="menu2">커뮤니티</RouterLink>
            <RouterLink :to="{name: 'today-learning'}" class="menu3">학습 로드맵</RouterLink>
          </div>

          <div class="nav-auth-section">
            <div v-if="!isLoggedIn" class="guest-nav-capsule">
              <RouterLink :to="{name:'signup'}" class="nav-link-signup">회원가입</RouterLink>
              <RouterLink :to="{name:'login'}" class="nav-btn-login">로그인</RouterLink>
            </div>

            <div v-else class="user-profile-section">
              <div class="user-profile-chip">
                <div class="user-avatar-mini">✨</div>
                <div class="user-info-nav">
                  <span class="user-nickname-nav"><strong>{{ nickname }}</strong>님</span>
                </div>
                <div class="nav-divider"></div>
                <div class="chip-buttons">
                  <RouterLink :to="{name: 'mypage'}" class="nav-sub-btn">마이페이지</RouterLink>
                  <button class="nav-btn-logout" @click="logoutHandler">로그아웃</button>
                </div>
              </div>
            </div>
            <RouterLink to="/story/create" class="btn-start-nav">시작하기</RouterLink>
          </div>
        </nav>
      </div>
    </header>

    <RouterView />
  </div>
</template>

<style>
/* 1. 전역 컬러 변수 정의 (이게 없으면 색이 안 나옵니다) */
:root {
  --primary: #58CC02;
  --primary-light: #89E152;
  --secondary: #1CB0F6;
  --text: #2D3436;
}

/* 2. 전체 125% 확대 적용 */
.global-zoom-container {
  zoom: 1.3;
  font-family: 'Nunito', 'Jua', sans-serif;
  min-height: 100vh;
}

/* 3. 헤더 기본 스타일 복구 */
header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 15px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  zoom: 1.25;
  width: 85%;         /* 단위를 꼭 붙여야 작동합니다 (80% 등) */
  max-width: 1000px;  /* 전체 가로 길이를 제한해서 사이 공간을 줄입니다 */
  margin: 0 auto;
}

.logo {
  font-size: 1.5rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text);
  text-decoration: none;
}

.logo:hover {
  transform: scale(1.1);
  font-weight: 800;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

/* 4. 요청하신 네비게이션 스타일들 */
.nav-links {
  display: flex;
  align-items: center;
  gap: 30px;
}

.menu-items {
  display: flex;
  gap: 20px;
}

.menu-items a {
  text-decoration: none;
  color: var(--text);
  font-weight: 700;
}

.nav-auth-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.guest-nav-capsule {
  display: flex;
  align-items: center;
  background: #F2F4F6;
  padding: 4px 4px 4px 16px;
  border-radius: 50px;
  gap: 12px;
}

.nav-link-signup {
  font-size: 0.85rem;
  color: #666;
  text-decoration: none;
  font-weight: 700;
}

.nav-btn-login {
  background: white;
  padding: 7px 18px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 800;
  text-decoration: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  color: var(--text);
}

.user-profile-chip {
  display: flex;
  align-items: center;
  background: rgba(88, 204, 2, 0.08);
  padding: 5px 14px 5px 5px;
  border-radius: 50px;
  border: 1px solid rgba(88, 204, 2, 0.15);
  gap: 8px;
}

.user-avatar-mini {
  width: 30px;
  height: 30px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-divider {
  width: 1px;
  height: 12px;
  background: rgba(0,0,0,0.1);
}

.chip-buttons {
  display: flex;
  gap: 10px;
}

.nav-sub-btn {
  display: flex;
  align-items: center;
  line-height: 1;

  background: none;
  border: none;
  font-size: 0.8rem;
  font-weight: 700;
  text-decoration: none;
  color: #666;
  cursor: pointer;
  padding: 0;
    
  /* ✨ 부드러운 변화를 위한 핵심 속성 */
  transition: all 0.2s ease-in-out; 
  display: inline-block; /* transform 적용을 위해 필요 */
}

.nav-sub-btn:hover {
    /* 호버 시 빨간색으로 변경 */
    color: #4d77ff; 
    
    /* 호버 시 1.1배 커짐 (125% 확대 상태에서도 잘 작동합니다) */
    transform: scale(1.1); 
    
    /* 글자를 조금 더 진하게 해서 강조 */
    font-weight: 800;
}

.nav-btn-logout {
  display: flex;
  align-items: center;
  line-height: 1;

  background: none;
  border: none;
  font-size: 0.8rem;
  font-weight: 700;
  color: #999;
  cursor: pointer;
  padding: 0;
    
    /* ✨ 부드러운 변화를 위한 핵심 속성 */
  transition: all 0.2s ease-in-out; 
  display: inline-block; /* transform 적용을 위해 필요 */
}

.nav-btn-logout:hover {
    /* 호버 시 빨간색으로 변경 */
    color: #ff4d4f; 
    
    /* 호버 시 1.1배 커짐 (125% 확대 상태에서도 잘 작동합니다) */
    transform: scale(1.1); 
    
    /* 글자를 조금 더 진하게 해서 강조 */
    font-weight: 800;
}

.menu1:hover,
.menu2:hover,
.menu3:hover {
  /* 호버 시 빨간색으로 변경 */
    color: #0ead1b; 
    
    /* 호버 시 1.1배 커짐 (125% 확대 상태에서도 잘 작동합니다) */
    transform: scale(1.1); 
    
    /* 글자를 조금 더 진하게 해서 강조 */
    font-weight: 800;
}

.btn-start-nav {
  background: linear-gradient(135deg, var(--primary) 0%, #2BAB0D 100%);
  color: white;
  padding: 9px 20px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 800;
  font-size: 0.85rem;
}

.btn-start-nav:hover {
  transform: scale(1.1);
  font-weight: 800;
  background: #028d09;
  transition: all 0.2s ease-in-out; 
  display: inline-block; /* transform 적용을 위해 필요 */
}
</style>