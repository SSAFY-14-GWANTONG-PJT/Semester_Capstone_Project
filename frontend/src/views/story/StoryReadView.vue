<template>
    <div class="read-container">
      <div class="book-card">
        <div class="story-image">
          <div class="placeholder-img">🎨 삽화 영역</div>
        </div>
        
        <div class="story-content">
          <h1 class="story-title">용감한 공룡 디노</h1>
          
          <div class="text-box">
            <p class="english-text">
              Once upon a time, there was a brave dinosaur named <span class="highlight">Dino</span>.
              He loved to <span class="highlight">explore</span> the forest.
            </p>
            <p class="korean-text">
              옛날 옛적에, 디노라는 용감한 공룡이 살았어요.
              그는 숲을 탐험하는 것을 좋아했답니다.
            </p>
          </div>
  
          <div class="action-buttons">
            <button class="btn-icon">🔊 듣기</button>
            <button @click="goQuiz" class="btn btn-primary">
              퀴즈 풀러 가기 🎯
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter, useRoute } from 'vue-router'
  const router = useRouter()
  const route = useRoute()
  
  const goQuiz = () => {
    router.push(`/story/quiz/${route.params.id}`)
  }
  </script>
  
  <style scoped>
  .read-container { padding: 40px 20px; max-width: 1000px; margin: 0 auto; }
  .book-card {
    background: white; border-radius: 40px; overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.1); display: flex; flex-direction: column;
  }
  .story-image { height: 300px; background: #E0F2FE; display: flex; align-items: center; justify-content: center; }
  .placeholder-img { font-size: 2rem; color: var(--secondary); opacity: 0.5; }
  
  .story-content { padding: 40px; }
  .story-title { font-size: 2.5rem; color: var(--text); margin-bottom: 30px; text-align: center; }
  
  .text-box { 
    background: #FFF9E5; padding: 30px; border-radius: 20px; margin-bottom: 30px;
    border: 2px dashed var(--yellow);
  }
  .english-text { font-size: 1.5rem; margin-bottom: 15px; line-height: 1.6; }
  .highlight { color: var(--secondary); font-weight: 800; background: rgba(28, 176, 246, 0.1); padding: 0 5px; border-radius: 5px;}
  .korean-text { color: #666; font-size: 1.1rem; }
  
  .action-buttons { display: flex; gap: 15px; justify-content: center; }
  .btn-icon {
    background: #f0f0f0; border: none; padding: 15px 25px; border-radius: 50px;
    font-weight: bold; cursor: pointer; font-size: 1.1rem;
  }
  .btn-icon:hover { background: #e0e0e0; }
  
  @media (min-width: 768px) {
    .book-card { flex-direction: row; }
    .story-image { flex: 1; height: auto; min-height: 500px; }
    .story-content { flex: 1; overflow-y: auto; max-height: 80vh; }
  }
  </style>