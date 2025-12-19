<template>
  <div class="learning-container">
    <header class="page-header">
      <h1 class="page-title">오늘의 학습 📝</h1>
      <p class="page-subtitle">매일매일 조금씩 성장하는 나! 오늘은 무엇을 배워볼까요?</p>
    </header>

    <div class="card-grid">
      
      <div class="learning-card card-green" @click="goTo('words')">
        <div class="card-icon">🍎</div>
        <div class="card-content">
          <h3>오늘의 단어</h3>
          <p>오늘 배워야 할<br><strong>단어 세트</strong>가 기다려요!</p>
          <span class="status-badge">학습 전</span>
        </div>
        <div class="card-bg-icon">A</div>
      </div>

      <div class="learning-card card-blue" @click="goTo('interpretation')">
        <div class="card-icon">🔍</div>
        <div class="card-content">
          <h3>문장 해석</h3>
          <p>예시 문장을 읽고<br><strong>퀴즈</strong>를 풀어봐요!</p>
          <span class="status-badge">진행 중</span>
        </div>
        <div class="card-bg-icon">?</div>
      </div>

      <div class="learning-card card-purple" @click="goTo('grammar')">
        <div class="card-icon">🏗️</div>
        <div class="card-content">
          <h3>문장 형식 대탐험</h3>
          <p>1형식부터 5형식까지<br><strong>문장 구조</strong>를 익혀요!</p>
          <div class="grammar-tags">
            <span>1형식</span><span>2형식</span><span>3형식...</span>
          </div>
        </div>
        <div class="card-bg-icon">S+V</div>
      </div>

      <div class="learning-card card-yellow" @click="goTo('story')">
        <div class="card-icon">✨</div>
        <div class="card-content">
          <h3>나만의 동화 만들기</h3>
          <p>오늘 배운 내용으로<br><strong>새로운 이야기</strong>를 만들어요!</p>
          <button class="action-btn">만들러 가기 🚀</button>
        </div>
        <div class="card-bg-icon">📖</div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goTo = (type) => {
  switch(type) {
    case 'words':
      alert('오늘의 단어 학습 페이지로 이동합니다! (준비 중)')
      // router.push('/learning/words') 
      break
    case 'interpretation':
      alert('문장 해석 퀴즈 페이지로 이동합니다! (준비 중)')
      // router.push('/learning/interpretation')
      break
    case 'grammar':
      alert('문장 형식 정리 페이지로 이동합니다! (준비 중)')
      // router.push('/learning/grammar')
      break
    case 'story':
      router.push('/story/create') // 기존 스토리 생성 페이지 연결
      break
  }
}
</script>

<style scoped>
.learning-container {
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(180deg, #F0F9FF 0%, #FFF9E5 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-header {
  text-align: center;
  margin-bottom: 50px;
}

.page-title {
  font-size: 3rem;
  font-weight: 900;
  color: var(--text);
  margin-bottom: 10px;
  text-shadow: 2px 2px 0px #FFF;
}

.page-subtitle {
  font-size: 1.2rem;
  color: #666;
  font-weight: 600;
}

/* 카드 그리드 레이아웃 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  width: 100%;
  max-width: 1000px;
}

/* 공통 카드 스타일 */
.learning-card {
  background: white;
  border-radius: 30px;
  padding: 30px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 20px rgba(0,0,0,0.05);
  border: 4px solid transparent;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 280px;
}

.learning-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.learning-card:active {
  transform: scale(0.98);
}

.card-icon {
  font-size: 3.5rem;
  margin-bottom: 15px;
  z-index: 2;
}

.card-content h3 {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 10px;
  color: var(--text);
  z-index: 2;
}

.card-content p {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 15px;
  z-index: 2;
}

/* 배경 아이콘 장식 */
.card-bg-icon {
  position: absolute;
  bottom: -20px;
  right: -20px;
  font-size: 8rem;
  font-weight: 900;
  opacity: 0.1;
  transform: rotate(-15deg);
  z-index: 1;
  transition: all 0.3s;
}

.learning-card:hover .card-bg-icon {
  transform: rotate(0deg) scale(1.1);
  opacity: 0.2;
}

/* 색상 테마별 스타일 */
.card-green { border-color: var(--primary-light); }
.card-green:hover { background: #F0FFF4; }
.card-green .card-icon, .card-green h3 { color: var(--primary-dark); }

.card-blue { border-color: var(--secondary-light); }
.card-blue:hover { background: #F0F9FF; }
.card-blue .card-icon, .card-blue h3 { color: var(--secondary); }

.card-purple { border-color: var(--purple); }
.card-purple:hover { background: #FAF5FF; }
.card-purple .card-icon, .card-purple h3 { color: #9F5AFD; }

.card-yellow { border-color: var(--yellow); }
.card-yellow:hover { background: #FFFBEB; }
.card-yellow .card-icon, .card-yellow h3 { color: var(--orange); }

/* 배지 및 태그 스타일 */
.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 800;
  background: #EEE;
  color: #888;
}

.card-green .status-badge { background: var(--primary); color: white; }
.card-blue .status-badge { background: var(--secondary-light); color: white; }

.grammar-tags {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  margin-top: 10px;
}
.grammar-tags span {
  font-size: 0.8rem;
  background: rgba(206, 130, 255, 0.2);
  color: #9F5AFD;
  padding: 4px 8px;
  border-radius: 8px;
  font-weight: 700;
}

.action-btn {
  background: var(--orange);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 50px;
  font-weight: 800;
  margin-top: 10px;
  cursor: pointer;
  box-shadow: 0 4px 0 #D97706;
}
</style>