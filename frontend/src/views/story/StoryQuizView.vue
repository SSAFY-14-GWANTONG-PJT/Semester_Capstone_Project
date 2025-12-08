<template>
    <div class="quiz-container">
      <div class="quiz-card">
        <div class="quiz-header">
          <span class="badge">QUIZ 1/5</span>
        </div>
  
        <div class="question-section">
          <h2 class="question-text">
            동화 속 주인공 'Dino'는 무엇을 좋아했나요?
          </h2>
        </div>
  
        <div class="choices-grid">
          <button 
            v-for="(choice, index) in choices" 
            :key="index"
            class="choice-btn"
            :class="{ 
              'selected': selectedChoice === index,
              'correct': isSolved && index === correctIndex,
              'wrong': isSolved && selectedChoice === index && index !== correctIndex
            }"
            @click="selectChoice(index)"
            :disabled="isSolved"
          >
            <span class="choice-num">{{ index + 1 }}</span>
            {{ choice }}
            <i v-if="isSolved && index === correctIndex" class="fas fa-check result-icon"></i>
            <i v-if="isSolved && selectedChoice === index && index !== correctIndex" class="fas fa-times result-icon"></i>
          </button>
        </div>
  
        <div v-if="isSolved" class="feedback-section" :class="isCorrect ? 'success' : 'fail'">
          <p class="feedback-msg">
            {{ isCorrect ? '정답입니다! 참 잘했어요! 🎉' : '아쉬워요. 다시 읽어볼까요? 💪' }}
          </p>
          <button class="btn btn-primary next-btn">다음 문제 ➡️</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  
  const choices = ['Sleeping (잠자기)', 'Exploring (탐험하기)', 'Eating (먹기)', 'Singing (노래하기)']
  const correctIndex = 1 // 정답 인덱스 (Exploring)
  
  const selectedChoice = ref(null)
  const isSolved = ref(false)
  
  const isCorrect = computed(() => selectedChoice.value === correctIndex)
  
  const selectChoice = (index) => {
    if (isSolved.value) return
    selectedChoice.value = index
    isSolved.value = true
    // 여기서 서버로 정답 제출 API 호출 가능
  }
  </script>
  
  <style scoped>
  .quiz-container {
    display: flex; justify-content: center; align-items: center;
    min-height: 90vh; padding: 20px; background: #F0F9FF;
  }
  .quiz-card {
    background: white; width: 100%; max-width: 600px;
    padding: 40px; border-radius: 30px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.1); position: relative;
  }
  .badge {
    background: var(--purple); color: white; padding: 8px 16px;
    border-radius: 20px; font-weight: 800; font-size: 0.9rem;
  }
  .question-text {
    font-size: 1.8rem; margin: 30px 0 40px; line-height: 1.4; color: var(--text);
  }
  
  .choices-grid { display: grid; gap: 15px; }
  .choice-btn {
    padding: 20px; border: 3px solid #F0F0F0; border-radius: 20px;
    background: white; font-size: 1.1rem; font-weight: bold; color: #555;
    cursor: pointer; display: flex; align-items: center; transition: all 0.2s;
    position: relative;
  }
  .choice-btn:hover:not(:disabled) { border-color: var(--secondary-light); background: #F0F9FF; }
  
  .choice-num {
    width: 30px; height: 30px; background: #EEE; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 0.9rem;
  }
  
  /* 정답/오답 스타일 */
  .choice-btn.correct { border-color: var(--primary); background: #F0FFF4; color: var(--primary-dark); }
  .choice-btn.wrong { border-color: var(--pink); background: #FFF0F5; color: #D32F2F; }
  .result-icon { margin-left: auto; font-size: 1.2rem; }
  
  .feedback-section { margin-top: 30px; text-align: center; animation: popUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
  .feedback-msg { font-size: 1.2rem; font-weight: 800; margin-bottom: 15px; }
  .success .feedback-msg { color: var(--primary); }
  .fail .feedback-msg { color: var(--pink); }
  .next-btn { width: 100%; }
  
  @keyframes popUp { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
  </style>