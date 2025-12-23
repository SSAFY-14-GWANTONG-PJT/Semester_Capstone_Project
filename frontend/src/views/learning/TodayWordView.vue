<template>
  <div class="study-container">
    <div v-if="loading" class="loading-state">
      <div class="spinner">🍎</div>
      <p>단어 친구들을 부르고 있어요...</p>
    </div>

    <div v-else-if="!canStudy" class="empty-state shadow-pop">
      <div class="icon">✨</div>
      <h2>{{ message }}</h2>
      <p class="sub-msg">오늘 공부를 정말 잘 마쳤어요!</p>
      <button @click="router.push('/learning/today')" class="action-btn-blue">목록으로 돌아가기</button>
    </div>

    <div v-else class="study-content">
      <header class="study-header-cloud">
        <div class="header-inner">
          <button class="nav-back-pill" @click="router.back()">🏠 돌아가기</button>
          
          <div class="header-center">
             <div class="level-sticker">Level {{ currentLevel }} - {{ currentUnit }}</div>
             <h2 class="title-text">오늘의 단어 친구들</h2>
          </div>

          <div class="count-bubble">{{ currentIndex + 1 }} / {{ vocas.length }}</div>
        </div>
        
        <div class="progress-wrapper">
          <div class="progress-bar-jelly">
            <div class="progress-fill" :style="{ width: progressPercentage + '%' }">
              <div class="progress-shine"></div>
            </div>
          </div>
        </div>
      </header>

      <main class="study-main">
        <div class="card-area">
          <div 
            class="flash-card" 
            :class="{ 'is-flipped': isFlipped }" 
            @click="toggleFlip"
          >
            <div class="card-face card-front">
              <div class="card-tag">English Word</div>
              
              <h1 class="word-text">{{ currentVoca.word }}</h1>
              
              <div class="flip-hint">
                <div class="tap-circle">
                  <span class="tap-icon">👆</span>
                </div>
                <p class="hint-msg">무슨 뜻일까?</p>
              </div>
            </div>

            <div class="card-face card-back">
              <div class="card-tag">Korean Meaning</div>
              <h1 class="meaning-text">{{ currentVoca.meaning }}</h1>
              <div class="difficulty-badge">난이도: {{ currentVoca.cefr_band }}</div>
            </div>
          </div>
        </div>

        <div class="controls-row">
          <button 
            class="control-btn prev-btn" 
            @click="prevCard" 
            :disabled="currentIndex === 0"
            :class="{ 'btn-inactive': currentIndex === 0 }"
          >
            이전 단어
          </button>

          <button 
            v-if="currentIndex < vocas.length - 1"
            class="control-btn next-btn" 
            @click="nextCard"
          >
            다음 단어
          </button>
          
          <button 
            v-else
            class="control-btn finish-btn" 
            @click="finishStudy"
          >
            학습 완료
          </button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/index'

const router = useRouter()

const loading = ref(true)
const canStudy = ref(false)
const message = ref('')
const currentLevel = ref(1)
const currentUnit = ref(1)
const vocas = ref([])
const currentIndex = ref(0)
const isFlipped = ref(false)

const currentVoca = computed(() => {
  if (vocas.value.length === 0) return {}
  return vocas.value[currentIndex.value]
})

const progressPercentage = computed(() => {
  if (vocas.value.length === 0) return 0
  return ((currentIndex.value + 1) / vocas.value.length) * 100
})

const fetchStudySet = async () => {
  try {
    const res = await api.get('/api/learning/today/')
    if (!res.data.can_study && res.data.message) {
      canStudy.value = false
      message.value = res.data.message
    } else {
      canStudy.value = true
      currentLevel.value = res.data.current_level
      currentUnit.value = res.data.current_unit
      vocas.value = res.data.data.vocas
    }
  } catch (error) {
    console.error('데이터 로딩 실패:', error)
  } finally {
    loading.value = false
  }
}

const toggleFlip = () => { isFlipped.value = !isFlipped.value }

const nextCard = () => {
  if (currentIndex.value < vocas.value.length - 1) {
    isFlipped.value = false
    setTimeout(() => { currentIndex.value++ }, 150) // 딜레이 단축으로 덜컥거림 방지
  }
}

const prevCard = () => {
  if (currentIndex.value > 0) {
    isFlipped.value = false
    setTimeout(() => { currentIndex.value-- }, 150)
  }
}

const finishStudy = async () => {
  try {
    const res = await api.post('/api/learning/today/')
    alert(res.data.message)
    router.push('/learning/today')
  } catch (error) {
    alert('학습 완료 처리에 실패했습니다.')
  }
}

onMounted(() => { fetchStudySet() })
</script>

<style scoped>
/* 1. 기본 배경 및 레이아웃 안정화 */
.study-container {
  height: 100vh; /* 전체 높이 고정 */
  background-color: #F0F9FF;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden; /* 페이지 자체 스크롤 방지하여 덜컥거림 차단 */
}

.study-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 2. 구름 헤더 영역 */
.study-header-cloud {
  width: 100%;
  background: white;
  padding: 30px 20px 40px;
  border-radius: 0 0 80px 80px;
  box-shadow: 0 10px 30px rgba(0, 162, 255, 0.05);
  flex-shrink: 0; /* 헤더 크기 고정 */
}

.header-inner {
  max-width: 1000px;
  margin: 0 auto 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-text { font-size: 1.8rem; font-weight: 900; color: #1E293B; margin-top: 5px; }

.nav-back-pill {
  background: #F1F5F9;
  border: none;
  padding: 10px 20px;
  border-radius: 30px;
  font-weight: 800;
  color: #64748B;
  cursor: pointer;
}

.level-sticker {
  background: #FFEDF1;
  color: #FF6B81;
  padding: 6px 15px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 900;
  display: inline-block;
}

.count-bubble {
  background: #3B82F6;
  color: white;
  padding: 8px 18px;
  border-radius: 50px;
  font-weight: 900;
  box-shadow: 0 5px 0 #1D4ED8;
}

.progress-wrapper { max-width: 800px; margin: 0 auto; width: 90%; }
.progress-bar-jelly { height: 16px; background: #E2E8F0; border-radius: 30px; overflow: hidden; }
.progress-fill {
  height: 100%;
  background: #4ADE80;
  border-radius: 30px;
  transition: width 0.4s ease;
  position: relative;
}

/* 3. 메인 학습 영역 (중앙 고정 핵심) */
.study-main {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 세로 중앙 */
  align-items: center;     /* 가로 중앙 */
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

/* 4. 카드 영역 (고정 크기 부여로 흔들림 방지) */
.card-area {
  perspective: 2000px;
  height: 520px; /* 높이 고정 */
  width: 100%;
  max-width: 700px;
}

.flash-card {
  position: relative;
  width: 100%;
  height: 80%;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  cursor: pointer;
}

.flash-card.is-flipped { transform: rotateY(180deg); }

.card-face {
  position: absolute;
  inset: 0; /* width/height 100% 대신 사용 */
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 60px;
  padding: 40px;
  box-shadow: 0 20px 0 #CBD5E1;
  border: 6px solid white;
}

.card-front {
  background: white;
  justify-content: center; /* 단어를 상하 중앙에 */
}

.card-back {
  background: #F0FFF4;
  transform: rotateY(180deg);
  border-color: #4ADE80;
  justify-content: center;
}

.card-tag {
  position: absolute;
  top: 30px;
  font-size: 1rem;
  font-weight: 900;
  color: #CBD5E1;
  letter-spacing: 2px;
}

/* 5. 텍스트 스타일 */
.word-text { 
  font-size: 500%;
  font-weight: 900; 
  color: #1E293B; 
  text-shadow: 4px 4px 0px #F1F5F9;
  text-align: center;
  margin-top: -40px; /* 손가락과 공간 배분 */
}

.meaning-text { 
  font-size: 300%; 
  font-weight: 900; 
  color: #059669; 
  padding-bottom : 10%;
}

.difficulty-badge{
  font-size: 130%;
}

/* 6. 손가락 힌트 (카드 하단 고정) */
.flip-hint {
  position: absolute;
  bottom: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tap-circle {
  width: 70px;
  height: 70px;
  background: #F0F9FF;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 8px 15px rgba(0,0,0,0.05);
  margin-bottom: 10px;
  border: 3px solid white;
}

.tap-icon {
  font-size: 2.5rem;
  animation: tap-bounce 1.2s infinite;
}

.hint-msg { font-size: 1.1rem; font-weight: 900; color: #3B82F6; }

@keyframes tap-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

/* 7. 컨트롤 버튼 스타일 */
.controls-row {
  display: flex;
  gap: 20px;
  width: 100%;
  max-width: 700px;
}

.control-btn {
  flex: 1;
  padding: 20px;
  border: none;
  border-radius: 25px;
  font-weight: 900;
  font-size: 1.3rem;
  cursor: pointer;
  transition: all 0.2s;
}

.prev-btn { background: #A7F3D0; color: #065F46; box-shadow: 0 8px 0 #34D399; }
.next-btn { background: #3B82F6; color: white; box-shadow: 0 8px 0 #1D4ED8; }
.finish-btn { background: #FBBF24; color: white; box-shadow: 0 8px 0 #D97706; }

.btn-inactive { opacity: 0.5; background: #E2E8F0 !important; color: #94A3B8 !important; box-shadow: 0 8px 0 #CBD5E1 !important; }

.control-btn:active:not(:disabled) { transform: translateY(4px); box-shadow: none; }

/* 공통 애니메이션/상태 */
.loading-state, .empty-state { margin: auto; padding: 60px; text-align: center; }
.spinner { font-size: 4rem; animation: spin 2s infinite linear; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
</style>