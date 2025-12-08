<template>
    <div class="loading-container">
      <div class="mascot-wrapper">
        <div class="mascot">🤖</div>
        <div class="particle p1">⭐</div>
        <div class="particle p2">✨</div>
      </div>
      <h2>AI가 재미있는 이야기를<br>만들고 있어요!</h2>
      <p>잠시만 기다려주세요...</p>
      <div class="progress-bar">
        <div class="progress-fill"></div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  onMounted(() => {
    // 3초 뒤에 결과 페이지로 이동 (시뮬레이션)
    setTimeout(() => {
      router.push('/story/read/1') // 임의의 ID 1번
    }, 3000)
  })
  </script>
  
  <style scoped>
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    text-align: center;
  }
  .mascot-wrapper { position: relative; margin-bottom: 30px; }
  .mascot { font-size: 6rem; animation: bounce 1s infinite alternate; }
  .particle { position: absolute; font-size: 2rem; animation: spin 2s infinite linear; }
  .p1 { top: 0; left: -20px; }
  .p2 { bottom: 0; right: -20px; }
  
  h2 { font-size: 1.8rem; color: var(--primary-dark); margin-bottom: 10px; }
  p { color: #888; }
  
  .progress-bar {
    width: 300px; height: 10px; background: #E5E5E5;
    border-radius: 10px; margin-top: 30px; overflow: hidden;
  }
  .progress-fill {
    height: 100%; background: var(--secondary);
    width: 0%; animation: fill 3s ease-in-out forwards;
  }
  
  @keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-20px); } }
  @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
  @keyframes fill { to { width: 100%; } }
  </style>