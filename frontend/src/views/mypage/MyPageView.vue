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
            <span class="value">{{ stories.length }}<span>권</span></span>
          </div>
          <div class="stat-box">
            <span class="label">성장 포인트</span>
            <span class="value">{{ store.experience }}<span>P</span></span>
          </div>
        </div>
      </div>
    </section>

    <main class="container dashboard-grid">
      <div class="dash-card progress-card">
        <div class="card-header">
          <h3>🚀 현재 학습 레벨</h3>
          <span class="level-badge">LEVEL {{ userInfo.level }}</span>
        </div>
        <div class="progress-container">
          <div class="progress-labels">
            <span>다음 레벨까지</span>
            <strong>75%</strong>
          </div>
          <div class="main-progress-bar">
            <div class="fill" style="width: 75%;"></div>
          </div>
          <p v-if="userInfo.level < 10" class="progress-tip">5권만 더 읽으면 <strong>LEVEL {{ userInfo.level + 1 }}</strong>가 될 수 있어요! 🔥</p>
          <p v-else class="progress-tip">최고 레벨이에요! 대단해요!</p>
        </div>
      </div>

      <div class="dash-card stories-card">
        <div class="card-header">
          <h3>📚 내가 쓴 동화</h3>
          <RouterLink :to="{name: 'user-total-stories'}">전체보기</RouterLink>
        </div>
        <div class="story-list">
          <MyPageStoryView v-for="story in latestStories" :key="story.id" :story="story" />
          <p v-if="latestStories.length === 0" class="empty-msg">아직 작성한 동화가 없어요! ✍️</p>
        </div>
      </div>

      <div class="dash-card menu-card">
        <h3>🛠️ 계정 관리</h3>
        <div class="menu-list">
          <RouterLink :to="{name: 'profile-edit'}" class="menu-item" :userInfo="userInfo">
            <span>👤 프로필 수정</span>
            <i class="fas fa-chevron-right"></i>
          </RouterLink>
          <RouterLink :to="{name: 'profile-learning-settings'}" class="menu-item">
            <span>⚙️ 학습 설정</span>
            <i class="fas fa-chevron-right"></i>
          </RouterLink>
          <button class="menu-item account-deactivate-btn" @click="showModal = true">
            <span>🚪 회원탈퇴</span>
          </button>
        </div>
      </div>
    </main>
  </div>

  <Transition name="bounce">
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <div class="emoji">🥺</div>
      <h2 class="modal-title">정말 떠나실 건가요?</h2>
      <p class="modal-text">많은 동화가 기다리고 있어요...</p>
      
      <div class="modal-buttons">
        <button @click="showModal = false" class="btn-keep">계속하기 ✨</button>
        <button @click="confirmDeactivation" class="btn-leave">탈퇴하기</button>
      </div>
    </div>
  </div>
</Transition>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useCounterStore } from '@/stores/counter';
import { RouterLink, RouterView, useRouter } from 'vue-router'
import {ref, onMounted, computed} from 'vue'
import axios from '@/api/index.js'
import MyPageStoryView from '@/components/profile/MyPageStoryView.vue';

const router = useRouter()
const store = useCounterStore();
const { nickname } = storeToRefs(store);

const userInfo = ref({
  nickname: '',
  email: '',
  age: null,
  level: 0,
})

// 회원탈퇴 --------------------------------------------------
const showModal = ref(false)

const confirmDeactivation = async () => {
  showModal.value = false
  await accountDeactiveHandler()
}

const accountDeactiveHandler = async () => {
  try {
    await axios.post('/api/accounts/accountDeactive/', {
      refresh: store.refreshToken.value 
    });
    alert("회원탈퇴 되었습니다. 👋\n그동안 이용해주셔서 감사합니다!")
    store.logout()
    router.push('/')
  } catch (error) {
    console.error("회원탈퇴 실패:", error)
    store.logout()
    router.push('/')
  }
};

onMounted(async () => {
  try {
    const response = await axios.get(
      '/api/accounts/profile/'
    )
    userInfo.value.level = response.data.level
    userInfo.value.nickname = response.data.nickname
    userInfo.value.email = response.data.email
    userInfo.value.age = response.data.age
  } catch (error) {
    console.error("프로필 가져오기 실패:", error)
  }
})

// 회원탈퇴 --------------------------------------------------

// 동화 리스트 가져오기
const stories = ref([])
onMounted(async () => {
  try {
    const response = await axios.get('/api/accounts/profile/story/')
    stories.value = response.data
  } catch (error) {
    console.error("동화 리스트 가져오기 실패:", error)
  }
})

const latestStories = computed(() => {
  const sorted = [...stories.value].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at)
  })

  return sorted.slice(0, 5)
})
// 동화 리스트 가져오기
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

.account-deactivate-btn {
  color: red;
}
.account-deactivate-btn:hover { background: #fff5f7; color: #f7135f; }

@media (max-width: 992px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .menu-card { grid-column: 1; }
  .banner-inner { flex-direction: column; text-align: center; gap: 30px; }
  .user-main-info { flex-direction: column; }
}

/* 회원탈퇴 모달 */ 
/* 모달 배경 */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px);
  display: flex; justify-content: center; align-items: center; z-index: 999;
}

/* 모달 박스 */
.modal-content {
  background: white; padding: 30px; border-radius: 30px;
  text-align: center; border: 5px solid #FFD54F;
  width: 90%; max-width: 400px;
}

.emoji { font-size: 3rem; margin-bottom: 10px; }
.modal-title { font-size: 1.5rem; color: #333; font-weight: 900; }
.modal-text { color: #888; margin-bottom: 25px; font-weight: 700; }

/* 버튼들 */
.modal-buttons { display: flex; gap: 10px; }
.btn-keep {
  flex: 1; padding: 12px; background: #FF6B6B; color: white;
  border: none; border-radius: 15px; font-weight: 800; cursor: pointer;
  box-shadow: 0 4px 0 #FA5252;
}
.btn-leave {
  flex: 1; padding: 12px; background: #EEE; color: #888;
  border: none; border-radius: 15px; font-weight: 800; cursor: pointer;
}

/* 통통 튀는 애니메이션 */
.bounce-enter-active { animation: bounce-in 0.5s; }
.bounce-leave-active { animation: bounce-in 0.5s reverse; }
@keyframes bounce-in {
  0% { transform: scale(0); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
</style>