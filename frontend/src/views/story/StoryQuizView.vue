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

        <button v-else @click="goBack" class="btn btn-secondary full-width">
          다른 동화 만들기 🏠
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const isLoading = ref(true)
const questions = ref([])
const userAnswers = ref({})
const showResult = ref(false)

const storyId = route.params.id

const fetchOrGenerateQuestions = async () => {
  try {
    // 1. 기존 문제 조회
    let res = await axios.get(`${import.meta.env.VITE_API_URL}/stories/${storyId}/questions/`, {
      headers: { Authorization: `Token ${store.token}` }
    })

    // 2. 문제가 없으면 생성 요청 (POST)
    if (res.data.length === 0) {
      console.log('문제 생성 요청 중...')
      res = await axios.post(`${import.meta.env.VITE_API_URL}/stories/${storyId}/questions/`, 
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
  showResult.value = true
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

const goBack = () => {
  router.push('/story/create')
}

onMounted(() => {
  fetchOrGenerateQuestions()
})
</script>

<style scoped>
/* 공통 레이아웃 */
.story-container {
  display: flex;
  justify-content: center;
  align-items: center; /* 퀴즈는 중앙 정렬 */
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

/* 문제 스타일 */
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

/* 채점 후 스타일 */
.choice-btn.correct { background: #E8F5E9; border-color: #2E7D32; color: #2E7D32; font-weight: bold; }
.choice-btn.wrong { background: #FFEBEE; border-color: #D32F2F; color: #D32F2F; text-decoration: line-through; }

/* 버튼 */
.btn { padding: 15px; border-radius: 15px; border: none; font-weight: bold; cursor: pointer; font-size: 1.2rem; }
.btn-primary { background-color: #FF6B6B; color: white; }
.btn-secondary { background-color: #666; color: white; }
.full-width { width: 100%; margin-top: 10px; }

/* 점수판 */
.score-board { margin-top: 20px; font-size: 1.2rem; color: #444; }
.score { color: #FF6B6B; font-size: 1.5rem; font-weight: 900; }

/* 로딩 스피너 */
.loading-box { padding: 40px; }
.spinner {
  margin: 0 auto 20px;
  width: 50px; height: 50px;
  border: 5px solid #f3f3f3; border-top: 5px solid #FF6B6B;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>