<template>
  <div class="learning-container">
    <header-Today class="page-header">
      <h1 class="page-title">오늘의 학습 📝</h1>
      <p class="page-subtitle">매일매일 조금씩 성장하는 나! 오늘은 무엇을 배워볼까요?</p>
    </header-Today>

    <div class="card-grid">
      
      <div class="learning-card card-pink" @click="goTo('pronunciation')">
          <div class="card-icon">👄</div>
          <div class="card-content">
            <h3>영어 발음표</h3>
            <p>알파벳이 내는<br><strong>여러 소리</strong>를 배워요!</p>
            <span class="status-badge">학습 하기</span>
        </div>
        <div class="card-bg-icon">ABC</div>
      </div>

      <div class="learning-card card-green" @click="goTo('words')">
        <div class="card-icon">🍎</div>
        <div class="card-content">
          <h3>오늘의 단어</h3>
          <p>오늘 배워야 할<br><strong>단어 세트</strong>가 기다려요!</p>
          <span class="status-badge">학습 하기</span>
        </div>
        <div class="card-bg-icon">Hi</div>
      </div>

      <div class="learning-card card-blue" @click="goTo('grammar')">
        <div class="card-icon">🔍</div>
        <div class="card-content">
          <h3>문장의 형식</h3>
          <p>1형식부터 5형식까지<br><strong>문장 구조</strong>를 익혀요!</p>
          <div class="grammar-tags">
            <span>1형식</span><span>2형식</span><span>3형식...</span>
          </div>
        </div>
        <div class="card-bg-icon">S+V</div>
      </div>

      <div class="learning-card card-yellow card-wide special-shine" @click="goTo('story')">
        <div class="shine-effect"></div> <div class="left-section">
          <div class="card-content">
            <h3>나만의 동화 만들기 ✨</h3>
            <p>오늘 배운 단어와 문법으로<br><strong>세상에 하나뿐인 이야기</strong>를 쓰는 작가가 되자!</p>
          </div>
          <div class="card-action-area">
            <button class="action-btn glow-btn">동화 만들러 가기</button>
          </div>
        </div>

        <div class="right-section">
          </div>
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
      router.push({ name: 'today-word' })
      break
    case 'grammar':
      router.push({ name : 'today-grammar'})
      break
    case 'story':
      router.push('/story/create') // 기존 스토리 생성 페이지 연결
      break
    case 'pronunciation': // 추가
      router.push({ name: 'today-pronunciation' })
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
  grid-template-columns: repeat(3, 1fr); /* 3개의 컬럼 고정 */
  gap: 30px;
  width: 100%;
  max-width: 1100px;
}

.card-wide {
  grid-column: 1 / -1;
  display: flex;       /* flex-direction: row 기본값 */
  align-items: center; /* 세로 중앙 정렬 */
  justify-content: space-between;
  
  min-height: 180px;   /* 높이를 살짝 줄여서 밀도 높임 */
  background: linear-gradient(135deg, #FFFBEB 0%, #FFFFFF 100%);
  border-color: #FCD34D;
  position: relative;
  overflow: hidden;
  
  /* [수정] 패딩을 줄여서 콘텐츠가 꽉 차 보이게 함 */
  padding: 0 30px; 
}

/* [수정] 배경 이미지 설정 (오른쪽을 꽉 채우는 배경) */
.card-wide::before {
  content: "";
  position: absolute;
  top: 0; right: 0; bottom: 0;
  
  /* [핵심] 너비를 50%로 설정하여 오른쪽 절반을 차지 */
  width: 50%; 
  
  background-image: url('@/assets/story_button_bg.png');
  
  /* [핵심] cover로 설정하여 빈 공간 없이 꽉 채움 */
  background-size: cover;      
  background-position: center right; 
  background-repeat: no-repeat;
  
  /* 투명도와 블렌딩으로 '배경처럼' 보이게 처리 */
  opacity: 0.5;   
  z-index: 0;
  
  /* 왼쪽으로 갈수록 자연스럽게 흐려지게 (선택 사항) */
  mask-image: linear-gradient(to right, transparent, black 20%);
  -webkit-mask-image: linear-gradient(to right, transparent, black 20%);
}

/* [수정] 왼쪽 섹션 (텍스트 + 버튼) */
.left-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 15px; /* 간격 살짝 축소 */
  
  /* [핵심] 텍스트가 이미지를 침범하지 않으면서 적당히 차지하도록 */
  width: 80%; 
  z-index: 2; 
}

/* 오른쪽 섹션 (공간 확보용 - 이미지가 보일 공간) */
.right-section {
  width: 40%;
  height: 100%;
  z-index: 2;
}

/* 텍스트 스타일 */
.card-wide h3 { 
  font-size: 2rem; 
  margin-bottom: 8px; 
  color: #D97706; 
  text-align: left;
}
.card-wide p { 
  font-size: 1.1rem; 
  text-align: left;
  line-height: 1.5;
  color: #78350F;
  word-break: keep-all; /* 한글 줄바꿈 예쁘게 */
}

.card-wide .card-action-area {
  margin: 0;
}

/* 빛나는 효과 (Shining Animation) */
.special-shine {
  box-shadow: 0 10px 30px rgba(251, 191, 36, 0.3);
  animation: border-pulse 3s infinite alternate;
}

.shine-effect {
  position: absolute;
  top: 0; left: -100%;
  width: 50%; height: 100%;
  background: linear-gradient(to right, transparent, rgba(255,255,255,0.6), transparent);
  transform: skewX(-25deg);
  animation: shine-move 4s infinite; /* 속도 조금 늦춤 */
  z-index: 1;
  pointer-events: none;
}

/* 버튼 스타일 */
.glow-btn {
  background: linear-gradient(90deg, #F59E0B, #D97706);
  padding: 12px 28px; /* 버튼 크기 살짝 조정 */
  font-size: 1.05rem;
  box-shadow: 0 5px 15px rgba(245, 158, 11, 0.4);
  transition: transform 0.2s;
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 800;
  cursor: pointer;
}
.glow-btn:hover {
  transform: scale(1.05);
  background: linear-gradient(90deg, #FBBF24, #B45309);
}


/* 공통 카드 스타일 */
.learning-card {
  background: white;
  border-radius: 30px;
  padding: 50px;
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

.card-pink { border-color: #F9A8D4; }
.card-pink:hover { background: #FDF2F8; }
.card-pink .card-icon, .card-pink h3 { color: #DB2777; }

/* 배지 및 태그 스타일 */
.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 800;
  background: #da4099;
  color: #EEE;
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
  background: rgba(21, 137, 245, 0.2);
  color: #5ea2f0;
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

@media (max-width: 900px) {
  .card-grid {
    grid-template-columns: 1fr; /* 1열로 변경 */
  }
  
  .card-wide {
    flex-direction: column; /* 다시 세로 배치 */
    align-items: flex-start;
    text-align: left;
    min-height: auto;
  }
  
  .card-wide .card-icon-area { margin-bottom: 15px; margin-right: 0; }
  .card-wide .card-action-area { margin-top: 20px; margin-left: 0; align-self: center; }
}
</style>