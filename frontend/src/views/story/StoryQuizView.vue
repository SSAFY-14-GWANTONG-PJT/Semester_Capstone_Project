<template>
  <div class="story-container">
    <div class="card">
      <h2 class="title">🧩 퀴즈 타임!</h2>
      <p class="subtitle">동화를 잘 읽었는지 확인해볼까요?</p>

      <div v-if="isLoading" class="loading-box">
        <div class="spinner"></div>
        <p>AI 선생님이 문제를 만들고 있어요... 🤔</p>
      </div>

      <div v-else-if="questions.length > 0" class="quiz-content">
        
        <div v-for="(q, idx) in questions" :key="q.id" class="quiz-item">
          <h3 class="question-text">Q{{ idx + 1 }}. {{ q.question }}</h3>
          <div class="choices-list">
            <button 
              v-for="choice in q.choices" 
              :key="choice.id"
              class="choice-btn"
              :class="{
                'selected': userAnswers[q.id] === choice.id,
                'correct': showResult && choice.is_correct,
                'wrong': showResult && !choice.is_correct && userAnswers[q.id] === choice.id
              }"
              @click="selectAnswer(q.id, choice.id)"
              :disabled="showResult"
            >
              {{ choice.content }}
            </button>
          </div>
        </div>

        <button v-if="!showResult" @click="checkAnswers" class="btn btn-primary full-width">
          채점하기 📝
        </button>

        <button v-else @click="finishQuiz" class="btn btn-secondary full-width">
          학습 완료하기 🎁
        </button>

        <div v-if="showResult" class="score-board">
          <span>당신의 점수는?</span>
          <strong class="score">{{ calculateScore() }}점!</strong> 🎉
        </div>

      </div>

      <div v-else class="empty-msg">
        문제를 불러오지 못했어요 😢
      </div>
    </div>
  </div>

  <div v-if="showPublishModal" class="modal-overlay">
    <div class="modal-card">
      <div class="modal-icon">🎉</div>
      <h2>축하해요! 학습을 완료했어요!</h2>
      <p>내가 만든 멋진 동화를<br><strong>커뮤니티 친구들에게 자랑할까요?</strong></p>
      
      <div class="modal-buttons">
        <button class="modal-btn btn-yes" @click="publishStory(true)">
          네! 자랑할래요 🙋‍♀️
        </button>
        <button class="modal-btn btn-no" @click="publishStory(false)">
          아니요, 나만 볼래요 🤫
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/api/index.js'
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const isLoading = ref(true)
const questions = ref([])
const userAnswers = ref({})
const showResult = ref(false)
const showPublishModal = ref(false) // 모달 상태

const storyId = route.params.id
// API URL 환경변수 사용 (없으면 하드코딩 값 사용)


const fetchOrGenerateQuestions = async () => {
  try {
    let res = await axios.get(`/api/stories/${storyId}/questions/`, {
      headers: { Authorization: `Token ${store.token}` }
    })

    if (res.data.length === 0) {
      console.log('문제 생성 요청 중...')
      res = await axios.post(`/api/stories/${storyId}/questions/`, 
        { num_questions: 3 },
        { headers: { Authorization: `Token ${store.token}` } }
      )
    }
    questions.value = res.data
  } catch (error) {
    console.error('퀴즈 로딩 에러:', error)
    alert('문제를 가져오는 중 오류가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
}

const selectAnswer = (qId, cId) => {
  if (showResult.value) return
  userAnswers.value[qId] = cId
}

const checkAnswers = () => {
  const answeredCount = Object.keys(userAnswers.value).length
  if (answeredCount < questions.value.length) {
    alert('아직 안 푼 문제가 있어요! 🧐')
    return
  }

  const score = calculateScore()
  showResult.value = true
  store.gainExperience(Math.floor(score/4) + 20)
  alert('동화 생성 경험치 : 30, 문제 풀이 경험치 : 점수 / 4를 획득했어요!')
}

const calculateScore = () => {
  let correctCount = 0
  questions.value.forEach(q => {
    const selectedId = userAnswers.value[q.id]
    const correctChoice = q.choices.find(c => c.is_correct)
    if (selectedId === correctChoice.id) correctCount++
  })
  return Math.round((correctCount / questions.value.length) * 100)
}

// (수정됨 ⭐) 버튼 클릭 시 모달 띄우기
const finishQuiz = () => {
  showPublishModal.value = true
}

const publishStory = async (isPublic) => {
  const newStatus = isPublic ? 'open' : 'normal'
  
  try {
    // (수정됨 ⭐) 헤더에 토큰 추가 & API URL 변수 사용
    await axios.put(`/api/stories/${storyId}/`, 
      { status: newStatus },
      { headers: { Authorization: `Token ${store.token}` } } // 토큰 필수!
    )
    
    alert(isPublic ? '커뮤니티에 등록되었습니다! 🎈' : '내 서재에 저장되었습니다! 📚')
    
    router.push('/mypage/stories')
    
  } catch (error) {
    console.error('상태 업데이트 실패:', error)
    alert('오류가 발생했어요. 다시 시도해주세요.')
  }
}

onMounted(() => {
  fetchOrGenerateQuestions()
})
</script>

<style scoped>
/* 기존 스타일 그대로 유지 */
.story-container {
  display: flex;
  justify-content: center;
  align-items: center; 
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
}
.card {
  background: white;
  padding: 40px;
  border-radius: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 600px;
  text-align: center;
}
.title { color: #FF6B6B; font-size: 2rem; margin-bottom: 5px; font-weight: 900; }
.subtitle { color: #888; margin-bottom: 30px; font-weight: 600; }

.quiz-item { margin-bottom: 40px; text-align: left; }
.question-text { font-size: 1.2rem; font-weight: 800; color: #444; margin-bottom: 15px; }

.choice-btn {
  display: block;
  width: 100%;
  padding: 15px;
  margin-bottom: 10px;
  border: 2px solid #EEE;
  border-radius: 15px;
  background: white;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}
.choice-btn:hover:not(:disabled) { background: #F7F7F7; border-color: #DDD; }
.choice-btn.selected { background: #E0F2FE; border-color: #0288D1; color: #0288D1; font-weight: bold; }

.choice-btn.correct { background: #E8F5E9; border-color: #2E7D32; color: #2E7D32; font-weight: bold; }
.choice-btn.wrong { background: #FFEBEE; border-color: #D32F2F; color: #D32F2F; text-decoration: line-through; }

.btn { padding: 15px; border-radius: 15px; border: none; font-weight: bold; cursor: pointer; font-size: 1.2rem; }
.btn-primary { background-color: #FF6B6B; color: white; }
.btn-secondary { background-color: #666; color: white; }
.full-width { width: 100%; margin-top: 10px; }

.score-board { margin-top: 20px; font-size: 1.2rem; color: #444; }
.score { color: #FF6B6B; font-size: 1.5rem; font-weight: 900; }

.loading-box { padding: 40px; }
.spinner {
  margin: 0 auto 20px;
  width: 50px; height: 50px;
  border: 5px solid #f3f3f3; border-top: 5px solid #FF6B6B;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.modal-card {
  background: white;
  padding: 40px;
  border-radius: 30px;
  text-align: center;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-icon { font-size: 4rem; margin-bottom: 20px; animation: bounce 2s infinite; }
.modal-card h2 { color: var(--text); font-size: 1.5rem; margin-bottom: 10px; font-weight: 800; }
.modal-card p { color: #666; margin-bottom: 30px; line-height: 1.5; font-size: 1.1rem; }

.modal-buttons { display: flex; flex-direction: column; gap: 12px; }

.modal-btn {
  padding: 15px; border: none; border-radius: 15px;
  font-size: 1.1rem; font-weight: 700; cursor: pointer;
  transition: transform 0.2s;
}
.modal-btn:hover { transform: scale(1.02); }

.btn-yes {
  background: var(--primary); color: white;
  box-shadow: 0 4px 0 var(--primary-dark);
}
.btn-no {
  background: #f0f0f0; color: #888;
}

@keyframes popUp {
  from { opacity: 0; transform: scale(0.8) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>