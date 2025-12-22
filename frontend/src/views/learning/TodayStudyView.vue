<template>
  <div class="study-container">
    <div v-if="loading" class="loading-state">
      <div class="spinner">🍎</div>
      <p>오늘의 단어를 불러오고 있어요...</p>
    </div>

    <div v-else-if="!canStudy" class="empty-state">
      <div class="icon">🎉</div>
      <h2>{{ message }}</h2>
      <button @click="router.push('/learning/today')" class="back-btn">목록으로 돌아가기</button>
    </div>

    <div v-else class="study-content">
      <header class="study-header">
        <button class="nav-back" @click="router.back()">← 뒤로</button>
        <div class="progress-info">
          <span class="level-badge">Level {{ currentLevel }} - Unit {{ currentUnit }}</span>
          <span class="count">{{ currentIndex + 1 }} / {{ vocas.length }}</span>
        </div>
      </header>
      
      <div class="progress-bar-container">
        <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
      </div>

      <div class="card-area">
        <div 
          class="flash-card" 
          :class="{ 'is-flipped': isFlipped }" 
          @click="toggleFlip"
        >
          <div class="card-face card-front">
            <span class="card-label">Word</span>
            <h1 class="word">{{ currentVoca.word }}</h1>
            <p class="click-hint">카드를 눌러 뜻을 확인하세요 👆</p>
          </div>

          <div class="card-face card-back">
            <span class="card-label">Meaning</span>
            <h1 class="meaning">{{ currentVoca.meaning }}</h1>
            <div class="meta-info">
              <span class="cefr">난이도: {{ currentVoca.cefr_band }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="controls">
        <button 
          class="control-btn prev" 
          @click="prevCard" 
          :disabled="currentIndex === 0"
        >
          이전 단어
        </button>

        <button 
          v-if="currentIndex < vocas.length - 1"
          class="control-btn next" 
          @click="nextCard"
        >
          다음 단어
        </button>
        
        <button 
          v-else
          class="control-btn finish" 
          @click="finishStudy"
        >
          학습 완료! 🎁
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/index'

const router = useRouter()

// 상태 변수
const loading = ref(true)
const canStudy = ref(false)
const message = ref('')
const currentLevel = ref(1)
const currentUnit = ref(1)
const vocas = ref([])
const currentIndex = ref(0)
const isFlipped = ref(false)

// 현재 보여줄 단어
const currentVoca = computed(() => {
  if (vocas.value.length === 0) return {}
  return vocas.value[currentIndex.value]
})

// 진행률 계산
const progressPercentage = computed(() => {
  if (vocas.value.length === 0) return 0
  return ((currentIndex.value + 1) / vocas.value.length) * 100
})

// 데이터 가져오기
const fetchStudySet = async () => {
  try {
    const res = await api.get('/api/learning/today/')
    
    // 이미 학습을 완료했거나 다음 레벨이 필요한 경우
    if (!res.data.can_study && res.data.message) {
      canStudy.value = false
      message.value = res.data.message
    } else {
      canStudy.value = true
      currentLevel.value = res.data.current_level
      currentUnit.value = res.data.current_unit
      vocas.value = res.data.data.vocas // 단어 목록
    }
  } catch (error) {
    console.error('학습 데이터 로딩 실패:', error)
    alert('데이터를 불러오는 중 오류가 발생했습니다.')
  } finally {
    loading.value = false
  }
}

// 카드 뒤집기
const toggleFlip = () => {
  isFlipped.value = !isFlipped.value
}

// 다음/이전 이동 시 카드 상태 초기화
const nextCard = () => {
  if (currentIndex.value < vocas.value.length - 1) {
    isFlipped.value = false
    setTimeout(() => {
      currentIndex.value++
    }, 200) // 부드러운 전환을 위해 약간 딜레이
  }
}

const prevCard = () => {
  if (currentIndex.value > 0) {
    isFlipped.value = false
    setTimeout(() => {
      currentIndex.value--
    }, 200)
  }
}

// 학습 완료 처리
const finishStudy = async () => {
  try {
    const res = await api.post('/api/learning/today/')
    alert(res.data.message) // "학습 완료! 다음 유닛으로 넘어갑니다."
    router.push('/learning/today') // 목록 화면으로 이동하여 업데이트된 상태 확인
  } catch (error) {
    console.error('학습 완료 처리 실패:', error)
    alert('학습 완료 처리에 실패했습니다.')
  }
}

onMounted(() => {
  fetchStudySet()
})
</script>

<style scoped>
.study-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #F0F9FF 0%, #FFF9E5 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* 로딩 및 빈 상태 */
.loading-state, .empty-state {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
.spinner {
  font-size: 3rem;
  animation: spin 1s infinite linear;
  margin-bottom: 20px;
}
.icon { font-size: 4rem; margin-bottom: 20px; }
.back-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
}

@keyframes spin { 
  from { transform: rotate(0deg); } 
  to { transform: rotate(360deg); } 
}

/* 메인 학습 화면 */
.study-content {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.study-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.nav-back {
  background: none;
  border: none;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  font-weight: 600;
}

.progress-info {
  display: flex;
  gap: 10px;
  align-items: center;
}

.level-badge {
  background: #E0F2FE;
  color: #0284C7;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 700;
}

.count {
  font-weight: 800;
  color: var(--text);
}

/* 진행바 */
.progress-bar-container {
  height: 8px;
  background: #E5E7EB;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  transition: width 0.3s ease;
}

/* 3D 플래시 카드 */
.card-area {
  perspective: 1000px;
  height: 400px;
  width: 100%;
  cursor: pointer;
}

.flash-card {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s;
  transform-style: preserve-3d;
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
  border-radius: 30px;
}

.flash-card.is-flipped {
  transform: rotateY(180deg);
}

.card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden; /* 뒷면 숨김 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 30px;
  background: white;
  padding: 20px;
  border: 4px solid white;
}

/* 카드 앞면 스타일 */
.card-front {
  background: white;
  border-color: var(--primary-light);
}

.card-back {
  background: #F0FFF4;
  transform: rotateY(180deg);
  border-color: var(--primary);
}

.card-label {
  font-size: 0.9rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 20px;
}

.word {
  font-size: 3.5rem;
  font-weight: 900;
  color: var(--text);
  margin-bottom: 30px;
}

.meaning {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--primary-dark);
  word-break: keep-all;
  margin-bottom: 20px;
}

.click-hint {
  font-size: 0.9rem;
  color: #AAA;
  margin-top: auto;
  animation: bounce 2s infinite;
}

.meta-info {
  margin-top: auto;
  font-size: 0.9rem;
  color: #666;
  background: rgba(255,255,255,0.6);
  padding: 5px 10px;
  border-radius: 10px;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
  40% {transform: translateY(-5px);}
  60% {transform: translateY(-3px);}
}

/* 컨트롤 버튼 */
.controls {
  display: flex;
  gap: 15px;
  width: 100%;
}

.control-btn {
  flex: 1;
  padding: 15px;
  border: none;
  border-radius: 15px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.prev {
  background: white;
  color: #666;
  box-shadow: 0 4px 0 #E5E7EB;
}
.prev:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.next {
  background: var(--primary);
  color: white;
  box-shadow: 0 4px 0 #059669;
}
.next:active {
  transform: translateY(4px);
  box-shadow: none;
}

.finish {
  background: var(--orange);
  color: white;
  box-shadow: 0 4px 0 #D97706;
}
.finish:hover {
  background: #F59E0B;
}
</style>