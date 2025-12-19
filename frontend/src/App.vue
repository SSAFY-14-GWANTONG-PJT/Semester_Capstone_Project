<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { storeToRefs } from 'pinia'
import axios from 'axios'

// 로직 추가: 스토어에서 상태 가져오기
const router = useRouter()
const store = useCounterStore()
const { isLoggedIn, nickname, refreshToken } = storeToRefs(store)

// 로그아웃 핸들러 추가
const logoutHandler = async () => {
  try {
    await axios.post('http://localhost:8000/accounts/logout/', {
      refresh: refreshToken.value 
    });
    store.logout()
    alert("로그아웃 되었습니다. 👋")
    router.push('/')
  } catch (error) {
    console.error("로그아웃 실패:", error)
    store.logout()
    router.push('/')
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
            <RouterLink to="/">홈</RouterLink>
            <RouterLink :to="{name: 'community'}">커뮤니티</RouterLink>
            
            <RouterLink :to="{name: 'today-learning'}">학습 로드맵</RouterLink>
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
  font-size: 0.8rem;
  font-weight: 700;
  text-decoration: none;
  color: #666;
}

.nav-btn-logout {
  background: none;
  border: none;
  font-size: 0.8rem;
  font-weight: 700;
  color: #999;
  cursor: pointer;
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
</style>