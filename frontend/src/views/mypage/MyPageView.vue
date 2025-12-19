<template>
  <div class="mypage-container">
    <section class="profile-banner">
      <div class="container banner-inner">
        <div class="user-main-info">
          <div class="big-avatar">✨</div>
          <div class="name-zone">
            <span class="welcome-tag">오늘도 열공 중!</span>
            <h1><strong>{{ nickname }}</strong>님의 학습 공간</h1>
          </div>
        </div>
        <div class="quick-stats">
          <div class="stat-box">
            <span class="label">읽은 동화</span>
            <span class="value">12<span>권</span></span>
          </div>
          <div class="stat-box">
            <span class="label">성장 포인트</span>
            <span class="value">1,250<span>P</span></span>
          </div>
        </div>
      </div>
    </section>

    <main class="container dashboard-grid">
      <div class="dash-card progress-card">
        <div class="card-header">
          <h3>🚀 현재 학습 레벨</h3>
          <span class="level-badge">LEVEL 3</span>
        </div>
        <div class="progress-container">
          <div class="progress-labels">
            <span>다음 레벨까지</span>
            <strong>75%</strong>
          </div>
          <div class="main-progress-bar">
            <div class="fill" style="width: 75%;"></div>
          </div>
          <p class="progress-tip">5권만 더 읽으면 <strong>LEVEL 4</strong>가 될 수 있어요! 🔥</p>
        </div>
      </div>

      <div class="dash-card stories-card">
        <div class="card-header">
          <h3>📚 최근 읽은 동화</h3>
          <RouterLink to="/stories" class="more-link">전체보기</RouterLink>
        </div>
        <div class="story-list">
          <div class="story-item">
            <span class="emoji">🦁</span>
            <div class="story-info">
              <p class="title">The Brave Lion</p>
              <p class="date">2025.12.18</p>
            </div>
          </div>
          <div class="story-item">
            <span class="emoji">🚀</span>
            <div class="story-info">
              <p class="title">Space Adventure</p>
              <p class="date">2025.12.16</p>
            </div>
          </div>
        </div>
      </div>

      <div class="dash-card menu-card">
        <h3>🛠️ 계정 관리</h3>
        <div class="menu-list">
          <RouterLink to="/profile/edit" class="menu-item">
            <span>👤 프로필 수정</span>
            <i class="fas fa-chevron-right"></i>
          </RouterLink>
          <RouterLink to="/settings" class="menu-item">
            <span>⚙️ 학습 설정</span>
            <i class="fas fa-chevron-right"></i>
          </RouterLink>
          <button class="menu-item logout-btn" @click="logoutHandler">
            <span>🚪 로그아웃</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const { nickname } = storeToRefs(store);

const logoutHandler = () => {
  // App.vue에서 정의한 로그아웃 로직을 호출하거나 스토어 액션 사용
  store.logout();
};
</script>

<style scoped>
.mypage-container {
  padding-bottom: 100px;
}

/* 상단 배너 섹션 */
.profile-banner {
  background: linear-gradient(135deg, rgba(88, 204, 2, 0.1) 0%, rgba(28, 176, 246, 0.1) 100%);
  padding: 60px 0;
  margin-bottom: 40px;
}

.banner-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-main-info {
  display: flex;
  align-items: center;
  gap: 25px;
}

.big-avatar {
  width: 100px;
  height: 100px;
  background: white;
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3.5rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.welcome-tag {
  color: var(--primary);
  font-weight: 800;
  font-size: 1rem;
}

.name-zone h1 {
  font-size: 2.2rem;
  margin-top: 5px;
  color: var(--text);
}

.quick-stats {
  display: flex;
  gap: 20px;
}

.stat-box {
  background: white;
  padding: 20px 30px;
  border-radius: 25px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0,0,0,0.03);
}

.stat-box .label { display: block; color: #999; font-weight: 700; margin-bottom: 5px; }
.stat-box .value { font-size: 1.8rem; font-weight: 900; color: var(--primary); }
.stat-box .value span { font-size: 1rem; color: #666; margin-left: 2px; }

/* 대시보드 그리드 */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.dash-card {
  background: white;
  border-radius: 35px;
  padding: 35px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.04);
  border: 1px solid rgba(0,0,0,0.02);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.card-header h3 { font-size: 1.5rem; font-weight: 800; }

/* 학습 달성도 카드 */
.level-badge {
  background: var(--secondary);
  color: white;
  padding: 6px 15px;
  border-radius: 12px;
  font-weight: 800;
  font-size: 0.9rem;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-weight: 700;
}

.main-progress-bar {
  height: 20px;
  background: #f0f0f0;
  border-radius: 100px;
  overflow: hidden;
  margin-bottom: 20px;
}

.main-progress-bar .fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-light));
  border-radius: 100px;
}

.progress-tip { color: #888; font-size: 0.95rem; }

/* 최근 동화 리스트 */
.story-list { display: flex; flex-direction: column; gap: 15px; }
.story-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f9fafb;
  border-radius: 20px;
}
.story-item .emoji { font-size: 1.5rem; }
.story-item .title { font-weight: 800; color: var(--text); margin: 0; }
.story-item .date { font-size: 0.85rem; color: #999; margin: 0; }

/* 메뉴 카드 */
.menu-card { grid-column: 2; grid-row: 1 / 3; }
.menu-list { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; }
.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  background: #f8f9fa;
  border-radius: 18px;
  text-decoration: none;
  color: #555;
  font-weight: 700;
  border: none;
  width: 100%;
  cursor: pointer;
  transition: all 0.2s;
}
.menu-item:hover { background: #f0f4f8; color: var(--secondary); }
.logout-btn:hover { background: #fff5f7; color: #ff6b9d; }

@media (max-width: 992px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .menu-card { grid-column: 1; }
  .banner-inner { flex-direction: column; text-align: center; gap: 30px; }
  .user-main-info { flex-direction: column; }
}
</style>