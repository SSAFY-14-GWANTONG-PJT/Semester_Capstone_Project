<template>
  <div class="settings-page-container">
    <main class="container">
      <div class="settings-box">
        <div class="settings-header">
          <div class="back-link" @click="router.back()">⬅️ 돌아가기</div>
          <h1>학습 환경 설정 ⚙️</h1>
          <p>나에게 딱 맞는 학습 환경을 만들어봐요!</p>
        </div>

        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-icon">🌙</span>
              <div class="text-group">
                <h3>다크모드</h3>
                <p>어두운 화면으로 눈을 보호해요</p>
              </div>
            </div>
            <label class="switch">
              <input type="checkbox" :checked="store.darkMode" @change="store.toggleDarkMode">
              <span class="slider round"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-icon">🔔</span>
              <div class="text-group">
                <h3>효과음</h3>
                <p>정답을 맞혔을 때 소리를 들을까요?</p>
              </div>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="store.soundEffects">
              <span class="slider round"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-icon">🎧</span>
              <div class="text-group">
                <h3>음성 자동 재생</h3>
                <p>페이지를 넘기면 AI가 바로 읽어줘요</p>
              </div>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="store.autoPlay">
              <span class="slider round"></span>
            </label>
          </div>

          <div class="setting-item goal-item">
            <div class="setting-info">
              <span class="setting-icon">🎯</span>
              <div class="text-group">
                <h3>일일 학습 목표</h3>
                <p>하루에 동화 <strong>{{ store.dailyGoal }}권</strong> 읽기</p>
              </div>
            </div>
            <div class="goal-selector">
              <button @click="store.dailyGoal--" :disabled="store.dailyGoal <= 1">-</button>
              <span class="goal-number">{{ store.dailyGoal }}</span>
              <button @click="store.dailyGoal++" :disabled="store.dailyGoal >= 10">+</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const router = useRouter()
// 로컬 reactive settings와 applyDarkMode 로직을 모두 삭제했습니다.
// 모든 상태와 로직은 이제 Pinia store에서 관리합니다.
</script>

<style scoped>
.settings-page-container {
  min-height: 100vh;
  padding: 60px 20px;
  background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
  transition: background 0.3s ease;
}

.settings-box {
  max-width: 650px;
  margin: 0 auto;
  background: white;
  border-radius: 40px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.05);
  border: 4px solid #1CB0F6;
}

.settings-header { text-align: center; margin-bottom: 40px; }
.settings-header h1 { font-size: 2.2rem; font-weight: 900; color: #3C3C3C; }
.back-link { cursor: pointer; color: #999; font-weight: 800; margin-bottom: 10px; }

.settings-list { display: flex; flex-direction: column; gap: 15px; }

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #F7F7F7;
  border-radius: 25px;
  border: 2px solid transparent;
  transition: 0.2s;
}

.setting-item:hover { border-color: #1CB0F6; background: #F0F9FF; }

.setting-info { display: flex; align-items: center; gap: 20px; }
.setting-icon { font-size: 2rem; }
.text-group h3 { font-size: 1.2rem; font-weight: 800; color: #3C3C3C; margin: 0; }
.text-group p { font-size: 0.95rem; color: #777; margin: 5px 0 0; font-weight: 600; }

/* 토글 스위치 스타일 */
.switch { position: relative; display: inline-block; width: 60px; height: 34px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
  background-color: #ccc; transition: .4s; border-radius: 34px;
}
.slider:before {
  position: absolute; content: ""; height: 26px; width: 26px; left: 4px; bottom: 4px;
  background-color: white; transition: .4s; border-radius: 50%;
}
input:checked + .slider { background-color: #58CC02; }
input:checked + .slider:before { transform: translateX(26px); }

/* 목표 조절기 */
.goal-selector { display: flex; align-items: center; gap: 15px; }
.goal-selector button {
  width: 35px; height: 35px; border-radius: 50%; border: none;
  background: #1CB0F6; color: white; font-weight: 900; cursor: pointer;
}
.goal-selector button:disabled { background: #CCC; }
.goal-number { font-size: 1.5rem; font-weight: 900; color: #1CB0F6; min-width: 30px; text-align: center; }

.save-notice {
  position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
  background: #3C3C3C; color: white; padding: 12px 25px; border-radius: 50px;
  font-weight: 700; z-index: 100;
}
</style>