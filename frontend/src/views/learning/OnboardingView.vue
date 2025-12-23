<template>
  <div class="study-container">
    <div v-if="showIntroModal" class="modal-overlay">
      <div class="modal-card bounce-in">
        <div class="modal-icon">🧚🏼‍♂️</div>
        <h2 class="modal-title">반가워요</h2>
        <p class="modal-desc">
          친구의 영어 실력을 확인하기 위해<br>
          간단한 10문제를 준비했어요.<br><br>
          틀려도 괜찮으니 천천히 풀어봐요!
        </p>
        <button class="start-btn" @click="startTest">준비됐어요! 시작하기</button>
      </div>
    </div>

    <div v-if="loading && !showIntroModal" class="loading-state">
      <div class="spinner"></div>
      <p class="loading-text">문제지를 가져오고 있어요...</p>
    </div>

    <div v-else-if="finished" class="result-container fade-in">
      <div class="result-card">
        <div class="result-icon">🏆</div>
        <h2>테스트 완료!</h2>
        
        <div class="result-info">
          <p class="level-label">당신의 레벨은</p>
          <p class="level-value">Level {{ resultLevel }}</p>
        </div>

        <div class="xp-badge">
          <span>획득 경험치</span>
          <strong>+{{ earnedXp }} XP</strong>
        </div>

        <button @click="goToMain" class="action-btn-primary">학습 시작하기</button>
      </div>
    </div>

    <div v-else-if="!showIntroModal && currentProblem.target_word" class="study-content fade-in">
      <header class="study-header">
        <div class="header-top">
          <span class="page-title">Level Test</span>
          <span class="count-badge">{{ currentIndex + 1 }} / {{ problems.length }}</span>
        </div>
        
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
      </header>

      <main class="study-main">
        <div class="quiz-card">
          <div class="question-section">
            <span class="q-label">Question {{ currentIndex + 1 }}</span>
            <h1 class="target-word">{{ currentProblem.target_word }}</h1>
            <p class="instruction">이 단어의 올바른 뜻은 무엇일까요?</p>
          </div>

          <div class="options-grid">
            <button 
              v-for="(option, idx) in currentProblem.options" 
              :key="option.id"
              class="option-btn"
              :class="getOptionClass(option.id)"
              @click="selectOption(option.id)"
              :disabled="isAnswered"
            >
              <div class="opt-marker">{{ ['A', 'B', 'C', 'D'][idx] }}</div>
              <div class="opt-content-wrapper">
                <span class="opt-text">{{ option.content }}</span>
                <span class="opt-part">{{ option.part }}</span>
              </div>
            </button>
          </div>
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

// 상태 변수
const showIntroModal = ref(true) // 모달 표시 여부
const loading = ref(true)
const finished = ref(false)
const problems = ref([])
const currentIndex = ref(0)
const userAnswers = ref([])

// 퀴즈 진행 상태
const isAnswered = ref(false)
const selectedOptionId = ref(null)
const isCorrect = ref(false)

// 결과 변수
const resultLevel = ref(1)
const earnedXp = ref(0)

// 현재 문제 데이터
const currentProblem = computed(() => {
  if (problems.value.length === 0) return {}
  return problems.value[currentIndex.value]
})

// 진행률
const progressPercentage = computed(() => {
  if (problems.value.length === 0) return 0
  return ((currentIndex.value + 1) / problems.value.length) * 100
})

// 모달 닫고 테스트 시작
const startTest = () => {
  showIntroModal.value = false
}

// 1. 문제 데이터 가져오기 (데이터 필터링 강화)
const fetchProblems = async () => {
  try {
    const res = await api.get('/api/learning/onboarding/')
    const rawProblems = res.data.problems || []

    // [요구사항 2] 데이터 유효성 검사 및 필터링
    // 단어(target_word)가 없거나, 선택지(options) 중 하나라도 내용/품사가 비어있으면 해당 문제는 제외
    const validProblems = rawProblems.filter(problem => {
      // 1. 문제 단어 확인
      if (!problem.target_word || problem.target_word.trim() === '') return false;
      
      // 2. 선택지 개수 확인 (4개 미만이면 문제 성립 X)
      if (!problem.options || problem.options.length < 4) return false;

      // 3. 각 선택지의 유효성 확인
      const isOptionsValid = problem.options.every(opt => {
        return opt.content && opt.content.trim() !== '' && opt.part && opt.part.trim() !== ''
      })

      return isOptionsValid
    })

    if (validProblems.length === 0) {
      alert("문제를 불러올 수 없습니다. (데이터 부족)")
      router.push('/')
      return
    }

    problems.value = validProblems
  } catch (error) {
    console.error('문제를 가져오는데 실패했습니다:', error)
    alert('서버 연결에 실패했습니다.')
  } finally {
    loading.value = false
  }
}

// 2. 보기 선택 처리
const selectOption = (optionId) => {
  if (isAnswered.value) return

  isAnswered.value = true
  selectedOptionId.value = optionId
  
  const correctId = currentProblem.value.correct_option_id
  isCorrect.value = (optionId === correctId)
  
  userAnswers.value.push(isCorrect.value)

  // 1초 뒤 다음 문제로 이동 (딜레이 줄임)
  setTimeout(() => {
    nextProblem()
  }, 1000)
}

// 3. 다음 문제 이동
const nextProblem = () => {
  if (currentIndex.value < problems.value.length - 1) {
    currentIndex.value++
    resetProblemState()
  } else {
    finishTest()
  }
}

const resetProblemState = () => {
  isAnswered.value = false
  selectedOptionId.value = null
  isCorrect.value = false
}

// 4. 테스트 종료 및 결과 전송
const finishTest = async () => {
  loading.value = true
  try {
    const res = await api.post('/api/learning/onboarding/', {
      results: userAnswers.value
    })
    
    resultLevel.value = res.data.result_level
    earnedXp.value = res.data.total_xp
    finished.value = true
  } catch (error) {
    console.error('결과 전송 실패:', error)
    alert('결과 처리에 실패했습니다.')
  } finally {
    loading.value = false
  }
}

const goToMain = () => {
  router.push('/')
}

// 보기 스타일 클래스
const getOptionClass = (id) => {
  if (!isAnswered.value) return ''

  const correctId = currentProblem.value.correct_option_id

  if (id === correctId) return 'opt-correct'      // 정답 (초록)
  if (id === selectedOptionId.value) return 'opt-wrong' // 내가 고른 오답 (빨강)
  
  return 'opt-disabled' // 나머지 흐리게
}

onMounted(() => {
  fetchProblems()
})
</script>

<style scoped>
/* 폰트 적용 (기존 스타일 활용) */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap');

.study-container {
  height: 100vh;
  background-color: #F8FAFC; /* 아주 연한 회색/블루 톤 */
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Nunito', sans-serif;
  overflow: hidden;
  position: relative;
}

/* --- 모달 스타일 (요구사항 1) --- */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.modal-card {
  background: white;
  width: 100%;
  max-width: 400px;
  border-radius: 30px;
  padding: 40px 30px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.bounce-in { animation: bounceIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }

.modal-icon { font-size: 3rem; margin-bottom: 15px; }
.modal-title { font-size: 1.8rem; font-weight: 800; color: #1E293B; margin-bottom: 15px; }
.modal-desc { font-size: 1.1rem; color: #64748B; line-height: 1.6; margin-bottom: 30px; word-break: keep-all;}

.start-btn {
  background: linear-gradient(135deg, #6cad40, #2ea834);
  color: white;
  width: 100%;
  padding: 16px;
  border-radius: 20px;
  font-size: 1.2rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  box-shadow: 0 8px 16px rgba(59, 246, 106, 0.3);
  transition: transform 0.2s;
}
.start-btn:active { transform: scale(0.98); }

/* --- 헤더 및 프로그레스 --- */
.study-content { width: 100%; height: 100%; display: flex; flex-direction: column; }

.study-header {
  padding: 20px 24px;
  background: white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.page-title { font-size: 1.2rem; font-weight: 800; color: #94A3B8; }
.count-badge { background: #EEF2FF; color: #4F46E5; padding: 6px 12px; border-radius: 20px; font-weight: 800; font-size: 0.9rem; }

.progress-track { height: 10px; background: #F1F5F9; border-radius: 10px; overflow: hidden; }
.progress-fill { height: 100%; background: #3B82F6; border-radius: 10px; transition: width 0.5s ease; }

/* --- 메인 문제 카드 --- */
.study-main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.quiz-card {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.question-section { text-align: center; }
.q-label { font-size: 1rem; color: #3B82F6; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
.target-word { font-size: 3rem; color: #1E293B; font-weight: 900; margin: 10px 0; }
.instruction { font-size: 1.1rem; color: #64748B; font-weight: 600; }

/* --- 선택지 스타일 (깔끔하게) --- */
.options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.option-btn {
  background: white;
  border: 2px solid #E2E8F0;
  border-radius: 20px;
  padding: 20px;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.option-btn:hover:not(:disabled) { border-color: #3B82F6; transform: translateY(-3px); box-shadow: 0 8px 15px rgba(59, 130, 246, 0.1); }
.option-btn:active:not(:disabled) { transform: translateY(0); }

.opt-marker {
  width: 32px; height: 32px;
  background: #F1F5F9; color: #64748B;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 0.9rem;
  flex-shrink: 0;
}

.opt-content-wrapper { display: flex; flex-direction: column; }
.opt-text { font-size: 1.1rem; font-weight: 800; color: #334155; margin-bottom: 2px; }
.opt-part { font-size: 0.85rem; color: #94A3B8; font-weight: 600; }

/* 정답/오답 상태 */
.opt-correct { background: #ECFDF5; border-color: #10B981; }
.opt-correct .opt-marker { background: #10B981; color: white; }
.opt-correct .opt-text { color: #065F46; }

.opt-wrong { background: #FEF2F2; border-color: #EF4444; }
.opt-wrong .opt-marker { background: #EF4444; color: white; }
.opt-wrong .opt-text { color: #991B1B; }

.opt-disabled { opacity: 0.6; pointer-events: none; }

/* --- 결과 화면 --- */
.result-container {
  display: flex; justify-content: center; align-items: center; height: 100%; padding: 20px;
}
.result-card {
  background: white; padding: 50px 40px; border-radius: 40px;
  text-align: center; width: 100%; max-width: 450px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.08);
}
.result-icon { font-size: 4rem; margin-bottom: 20px; animation: pop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.result-card h2 { font-size: 2rem; color: #1E293B; font-weight: 900; margin-bottom: 30px; }

.result-info { background: #F8FAFC; padding: 20px; border-radius: 20px; margin-bottom: 20px; }
.level-label { font-size: 0.9rem; color: #64748B; font-weight: 700; margin-bottom: 5px; }
.level-value { font-size: 2rem; color: #3B82F6; font-weight: 900; }

.xp-badge {
  display: inline-flex; flex-direction: column; align-items: center;
  background: #FFFBEB; color: #B45309; border: 2px solid #FDE68A;
  padding: 10px 25px; border-radius: 15px; margin-bottom: 30px;
}
.xp-badge span { font-size: 0.8rem; font-weight: 700; opacity: 0.8; }
.xp-badge strong { font-size: 1.4rem; font-weight: 900; }

.action-btn-primary {
  width: 100%; padding: 18px; border-radius: 20px;
  background: #10B981; color: white; font-size: 1.1rem; font-weight: 800;
  border: none; cursor: pointer; box-shadow: 0 8px 0 #059669;
  transition: transform 0.1s;
}
.action-btn-primary:active { transform: translateY(4px); box-shadow: 0 2px 0 #059669; }

/* --- 애니메이션 및 로딩 --- */
.fade-in { animation: fadeIn 0.5s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes bounceIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes pop { 0% { transform: scale(0); } 80% { transform: scale(1.1); } 100% { transform: scale(1); } }

.loading-state { text-align: center; margin-top: 40vh; }
.spinner {
  width: 40px; height: 40px; border: 4px solid #E2E8F0; border-top-color: #3B82F6;
  border-radius: 50%; margin: 0 auto 20px; animation: spin 1s linear infinite;
}
.loading-text { font-weight: 700; color: #94A3B8; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 반응형 */
@media (max-width: 600px) {
  .options-grid { grid-template-columns: 1fr; }
  .target-word { font-size: 2.2rem; }
  .modal-card { padding: 30px 20px; }
}
</style>