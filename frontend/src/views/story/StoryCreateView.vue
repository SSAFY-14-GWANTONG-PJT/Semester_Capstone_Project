<template>
  <div class="story-container">
    <div class="card">
      <h2 class="title">동화 만들기 ✍🏻</h2>
      <p class="subtitle">어떤 이야기를 만들고 싶나요?</p>

      <div class="form-group">
        <label>장르를 골라주세요 🎭</label>
        <div class="genre-scroll-wrapper">
          <div class="genre-row">
            <button 
              v-for="g in genres" 
              :key="g.value"
              :class="['genre-btn', { active: selectedGenre === g.value && !customGenre }]"
              @click="selectGenre(g.value)"
            >
              <span class="genre-icon">{{ g.icon }}</span>
              <span class="genre-text">{{ g.label }}</span>
            </button>
          </div>
        </div>
        <div class="custom-genre-box">
          <br>
          <label>내가 찾는 장르가 없다면?</label>
          <input v-model="customGenre" type="text" class="mini-input" placeholder="직접 입력 (예: 탐정, 모험)" @input="selectedGenre = ''" />
        </div>
      </div>

      <div class="form-group">
        <label>동화에 넣고 싶은 내용</label>
        <textarea v-model="userPrompt" class="story-input" placeholder="ex. 왕자, 공주, 여우, 악당, 마녀, 마법의 성, 숲속마을, 사랑, 전쟁..."></textarea>
      </div>

      <div class="form-group">
        <label>단어 학습 포함</label>
        <div class="toggle-group">
          <button :class="['toggle-btn', { active: includeWord === true }]" @click="includeWord = true">❤️ 네, 넣어주세요!</button>
          <button :class="['toggle-btn', { active: includeWord === false }]" @click="includeWord = false">❌ 아니요, 괜찮아요!</button>
        </div>
      </div>

      <button @click="createStory" class="btn btn-primary full-width" :disabled="isLoading">
        {{ isLoading ? '작가님이 글 쓰는 중...' : '이야기 만들기' }}
      </button>
    </div>

    <Teleport to="body">
      <div v-show="isLoading" class="loading-overlay">
        
        <div class="game-header">
          <div class="score-board-outer">
            <span class="score-label">MY SCORE</span>
            <span class="score-value">{{ totalScore }}</span>
          </div>
        </div>

        <div class="machine">
          <div class="rail"></div>
          
          <div id="claw-container" class="claw-container" :style="{ left: clawX + 'px' }">
            <div class="claw-string" :style="{ height: clawY + 'px' }"></div>
            <div class="claw-head">
              <div class="arm left"></div>
              <div class="arm right"></div>
            </div>
          </div>

          <div class="doll-display">
            <div 
              v-for="doll in dolls" 
              :key="doll.id" 
              :class="['doll', doll.type]"
              :style="{ 
                left: doll.x + 'px', 
                bottom: doll.y + 'px', 
                zIndex: doll.zIndex,
                transform: `rotate(${doll.rotate}deg)`,
                position: 'absolute'
              }"
            ></div>
          </div>
          <div class="drop-zone"></div>

          <div class="controls">
            <button class="ctrl-btn" @mousedown="moveLeft" @mouseup="stopMoving" @touchstart.prevent="moveLeft" @touchend="stopMoving">◀</button>
            <button class="ctrl-btn down" @click="startDrop">PICK!</button>
            <button class="ctrl-btn" @mousedown="moveRight" @mouseup="stopMoving" @touchstart.prevent="moveRight" @touchend="stopMoving">▶</button>
          </div>
        </div>

        <div v-show="isGameSuccess" class="modal-overlay">
          <div class="modal-content" :class="{ 'villain-hit': grabbedDollType === 'villain' }">
            <h2 class="modal-title">
              {{ grabbedDollType === 'villain' ? '💀 앗! 함정이야!' : '🎉 인형을 뽑았어요!' }}
            </h2>
            
            <div class="points-wrapper">
              <span class="doll-name-tag">{{ successDollName }}</span>
              <p class="point-text" :class="lastPoints > 0 ? 'plus' : 'minus'">
                {{ lastPoints > 0 ? `+${lastPoints}` : lastPoints }} 점
              </p>
            </div>

            <div id="result-doll-display">
              <div :class="['doll', grabbedDollType]" style="position: relative; transform: scale(2.2);"></div>
            </div>

            <button class="cute-retry-btn" @click="closeGameModal">
              한 번 더 뽑기 🧸
            </button>
          </div>
        </div>
        
        <div class="loading-content">
          <div class="spinner"></div>
          <p class="loading-text">🧚‍♀️ AI 작가님이 동화를 쓰고 있어요...</p>
          <p class="sub-text">인형을 뽑으며 기다리면 곧 이야기가 시작돼요!</p>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/api/index.js'
import { useCounterStore } from '@/stores/counter'

const router = useRouter()
const store = useCounterStore()

// --- 상태 관리 ---
const isLoading = ref(false)
const selectedGenre = ref('')
const customGenre = ref('')
const userPrompt = ref('')
const includeWord = ref(true)
const totalScore = ref(0)
const lastPoints = ref(0)

const genres = [
  { label: '영웅', value: 'hero', icon: '🦸‍♂️' },
  { label: '행복', value: 'happy', icon: '🥰' },
  { label: '슬픔', value: 'sad', icon: '😢' },
  { label: '로맨스', value: 'romance', icon: '💖' },
  { label: '호러', value: 'horror', icon: '👻' },
  { label: '판타지', value: 'fantasy', icon: '🧙‍♂️' },
  { label: 'SF/우주', value: 'sf', icon: '🚀' },
]

const selectGenre = (val) => { selectedGenre.value = val; customGenre.value = ''; }
const parseKeywords = (text) => text ? text.split(/,| /).map(w => w.trim()).filter(w => w.length > 0) : []

const createStory = async () => {
  const finalGenre = customGenre.value || selectedGenre.value
  if (!finalGenre || !userPrompt.value) return alert('입력창을 채워주세요!')
  isLoading.value = true
  totalScore.value = 0
  try {
    const response = await axios.post(`/api/stories/`, {
      age: 7, story_level: 2, genre: finalGenre,
      keywords: parseKeywords(userPrompt.value),
      study_set_id: includeWord.value ? 1 : null,
      vocab_words: []
    }, {
      headers: { Authorization: `Bearer ${store.token}` }
    })
    router.push({ name: 'story-read', params: { id: response.data.id } })
  } catch (error) {
    console.error('실패:', error); isLoading.value = false;
  }
}

// --- 미니게임 로직 ---
const dolls = ref([])
const isGameSuccess = ref(false)
const successDollName = ref('')
const grabbedDollType = ref('')
const clawX = ref(150);
const clawY = ref(30);
let state = 'IDLE'; 
let grabbedDoll = null;

const dollConfig = [
  { type: 'bear', points: 10, count: 7, name: '곰돌이' },
  { type: 'rabbit', points: 20, count: 4, name: '토끼' },
  { type: 'penguin', points: 30, count: 1, name: '펭귄' },
  { type: 'villain', points: -20, count: 3, name: '심술쟁이 악당' }
];

const moveLeft = () => { if(state==='IDLE') state = 'MOVE_LEFT' }
const moveRight = () => { if(state==='IDLE') state = 'MOVE_RIGHT' }
const stopMoving = () => { if(state==='MOVE_LEFT' || state==='MOVE_RIGHT') state = 'IDLE' }
const startDrop = () => { if(state==='IDLE') state = 'DOWN' }
const closeGameModal = () => { isGameSuccess.value = false; state = 'IDLE'; }

// [핵심 수정] 스마트한 인형 배치 알고리즘 (스카이라인 쌓기 & 뭉침 방지)
function initDolls() {
  const newDolls = [];
  const placedDolls = []; // 배치된 인형 추적용
  
  // 1. 모든 인형 설정을 하나의 리스트로 만들고 섞기 (골고루 분포되게)
  let allConfigs = [];
  dollConfig.forEach(cfg => {
    for(let i=0; i<cfg.count; i++) allConfigs.push({...cfg});
  });
  // Fisher-Yates Shuffle
  for (let i = allConfigs.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [allConfigs[i], allConfigs[j]] = [allConfigs[j], allConfigs[i]];
  }

  // 2. 하나씩 물리적으로 쌓아 올리기
  allConfigs.forEach(config => {
    let x, y, row;
    let placed = false;
    let attempts = 0;

    // 적절한 위치를 찾을 때까지 몇 번 시도 (뭉침 방지)
    while(!placed && attempts < 10) {
      x = 40 + (Math.random() * 270); // 랜덤 X
      let maxYUnderneath = -5; // 내 아래 가장 높은 인형의 Y좌표 (바닥 기준 -5)

      // 이미 배치된 인형들을 확인하며 내 아래에 있는지 검사
      placedDolls.forEach(pd => {
        // X축으로 겹치는지 확인 (인형 중심 기준 약 40px 이내)
        if(Math.abs(pd.x - x) < 40) {
          maxYUnderneath = Math.max(maxYUnderneath, pd.y);
        }
      });

      // 내 Y좌표는 아래 인형 높이 + 인형 키(42) + 약간의 랜덤 오차
      y = maxYUnderneath + 42 + (Math.random() * 5);
      // 대략적인 층수 계산 (높을수록 row가 큼)
      row = Math.floor(y / 40);

      // 너무 높게(3층 이상) 쌓이지 않도록 제한하여 옆으로 퍼지게 유도
      if(row < 3) placed = true;
      attempts++;
    }
    
    // 시도 횟수를 넘겨도 자리가 없으면 강제 배치 (거의 발생 안 함)
    if(!placed) { row = 2; y = (row * 42) + (Math.random()*5); }

    const dollData = {
      id: Math.random(),
      type: config.type, points: config.points, name: config.name,
      x: x,
      y: y,
      row: row,
      zIndex: 100 + row, // 높이 쌓일수록(row가 클수록) 시각적으로 앞으로(위로) 오게 함
      rotate: Math.random() * 40 - 20
    };
    newDolls.push(dollData);
    placedDolls.push(dollData);
  });

  dolls.value = newDolls;
}

function update() {
  if (state === 'MOVE_LEFT' && clawX.value > 20) clawX.value -= 3.5
  if (state === 'MOVE_RIGHT' && clawX.value < 280) clawX.value += 3.5
  if (state === 'DOWN') {
    clawY.value += 4.5
    const hitDoll = checkCollision();
    if (hitDoll) {
      grabbedDoll = hitDoll;
      state = 'UP';
    } else if (clawY.value > 320) { 
      state = 'UP';
    }
  } else if (state === 'UP') {
    clawY.value -= 4.5
    if (grabbedDoll) {
      grabbedDoll.y = 360 - (clawY.value + 45) 
      grabbedDoll.x = clawX.value + 5
    }
    if (clawY.value <= 30) state = 'RETURN'
  } else if (state === 'RETURN') {
    clawX.value -= 3.5
    if (grabbedDoll) grabbedDoll.x = clawX.value + 5
    if (clawX.value <= 40) {
      if (grabbedDoll) {
        lastPoints.value = grabbedDoll.points;
        totalScore.value += grabbedDoll.points;
        successDollName.value = grabbedDoll.name;
        grabbedDollType.value = grabbedDoll.type;
        isGameSuccess.value = true;
        dolls.value = dolls.value.filter(d => d.id !== grabbedDoll.id);
        grabbedDoll = null;
      } else { state = 'IDLE' }
    }
  }
  requestAnimationFrame(update)
}

function checkCollision() {
  let found = null;
  dolls.value.forEach(d => {
    const dx = Math.abs(d.x - (clawX.value + 5));
    const dy = clawY.value - (310 - d.y); 
    if (dx < 35 && dy > 0 && dy < 15) {
      // 높이 있는(row가 큰) 인형 우선
      if (!found || d.row > found.row) found = d;
    }
  });
  return found;
}

onMounted(() => { initDolls(); update(); });
</script>

<style scoped>
.story-container, .card, .title, label, button, .loading-text, .score-value, .point-text, .doll-name-tag, .cute-retry-btn {
  font-family: 'Nunito', 'Jua', sans-serif !important;
}

input::placeholder, textarea::placeholder {
  font-family: 'Nunito', 'Jua', sans-serif !important;
  font-weight: 700 !important;
  color: #BBBBBB !important;
  opacity: 1 !important;
  font-size: 16px;
}

.story-container {
  display: flex; justify-content: center; align-items: center;
  min-height: 80vh; padding: 20px;
  background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
}

.card {
  background: white; padding: 40px; border-radius: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 600px; text-align: center;
}

.title { color: #FF6B6B; font-size: 2.2rem; margin-bottom: 10px; font-weight: 900; }
.subtitle { color: #888; margin-bottom: 30px; font-weight: 600; }
.form-group { margin-bottom: 30px; text-align: left; }
.form-group label { display: block; font-weight: 800; margin-bottom: 12px; color: #333; font-size: 1.1rem; }

/* 장르 버튼 */
.genre-row { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px; }
.genre-btn { 
  display: flex; flex-direction: column; align-items: center; justify-content: center; 
  min-width: 90px; height: 95px; border: 2px solid #E5E5E5; border-radius: 20px; 
  background: white; cursor: pointer; transition: 0.2s; color: #666;
}
.genre-btn.active { border-color: #1CB0F6; background: #E0F2FE; color: #1CB0F6; box-shadow: 0 4px 10px rgba(28, 176, 246, 0.2); }
.genre-icon { font-size: 2.4rem !important; margin-bottom: 5px; }
.genre-text { font-size: 1rem; font-weight: 800; }

.mini-input { width: 100%; padding: 10px; border: 2px solid #E5E5E5; border-radius: 12px; margin-top: 10px; outline: none; }
.story-input { width: 100%; height: 100px; padding: 15px; border: 3px solid #E5E5E5; border-radius: 20px; resize: none; outline: none; font-size: 1rem; }

.toggle-group { display: flex; gap: 15px; }
.toggle-btn { flex: 1; padding: 15px; border-radius: 15px; border: 2px solid #E5E5E5; background: white; cursor: pointer; font-weight: 700; font-size: 1.1rem; }
.toggle-btn.active { border-color: #FF6B6B; background: #F0FFF4; color: #FF6B6B; font-weight: 800; }

.btn-primary { background-color: #FF6B6B; color: white; border: none; border-radius: 18px; font-weight: bold; cursor: pointer; }
.full-width { width: 100%; margin-top: 20px; font-size: 1.25rem; padding: 18px; }

/* 미니게임 로딩 오버레이 */
.loading-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  z-index: 99999; background: rgba(255, 255, 255, 0.96);
  display: flex; flex-direction: column; justify-content: center; align-items: center;
}

.game-header { width: 360px; margin-bottom: 10px; display: flex; justify-content: flex-end; }
.score-board-outer {
  background: #4E342E; color: #FFD54F; padding: 10px 20px; border-radius: 20px 20px 5px 5px;
  text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2); border: 4px solid #333; border-bottom: none;
}
.score-label { display: block; font-size: 0.75rem; color: #E5E5E5; font-weight: bold; }
.score-value { font-size: 1.8rem; font-weight: 900; }

.machine { 
  width: 360px; height: 500px; background-color: #A2E3FA; 
  border: 10px solid #4E342E; position: relative; border-radius: 20px; overflow: hidden; 
  box-shadow: 0 20px 50px rgba(0,0,0,0.15);
}
.rail { width: 100%; height: 10px; background: #333; position: absolute; top: 25px; opacity: 0.2; }
.claw-container { position: absolute; top: 0; width: 60px; z-index: 500; }
.claw-string { width: 4px; background: #555; margin: 0 auto; }
.claw-head { width: 44px; height: 20px; background: #ddd; margin: 0 auto; border-radius: 5px; border: 2px solid #333; position: relative; }
.arm { position: absolute; width: 8px; height: 25px; background: #bbb; bottom: -18px; border: 2px solid #333; border-radius: 4px; }
.arm.left { left: 2px; transform: rotate(15deg); }
.arm.right { right: 2px; transform: rotate(-15deg); }

.doll-display { position: absolute; bottom: 120px; width: 100%; height: 300px; pointer-events: none; }
.doll { width: 50px; height: 50px; border: 2px solid #333; box-sizing: border-box; }
.doll::before, .doll::after { content: ''; position: absolute; }
/* 🐧 펭귄 CSS 수정됨 */
.doll.penguin { background: #42A5F5; border-radius: 24px 24px 12px 12px; }
.doll.penguin::before { width: 32px; height: 34px; background: white; border-radius: 50%; bottom: 2px; left: 7px; border: 2px solid #eee; }
.doll.penguin::after { width: 4px; height: 4px; background: #333; border-radius: 50%; top: 14px; left: 16px; box-shadow: 12px 0 0 #333, 6px 4px 0 2px #FF9800; }
/* 나머지 동물 CSS 유지 */
.doll.bear { background: #8D6E63; border-radius: 15px; }
.doll.bear::before { width: 14px; height: 14px; background: #8D6E63; border-radius: 50%; top: -8px; left: 0px; box-shadow: 32px 0 0 #8D6E63; border: 2px solid #333; z-index: -1; }
.doll.bear::after { width: 4px; height: 4px; background: #333; border-radius: 50%; top: 15px; left: 12px; box-shadow: 20px 0 0 #333, 10px 8px 0 #333; }
.doll.rabbit { background: #FFFFFF; border-radius: 12px; }
.doll.rabbit::before { width: 10px; height: 25px; background: #FFF; border-radius: 10px; top: -18px; left: 8px; box-shadow: 22px 0 0 #FFF; border: 2px solid #333; z-index: -1; }
.doll.rabbit::after { width: 4px; height: 4px; background: #333; border-radius: 50%; top: 18px; left: 14px; box-shadow: 16px 0 0 #333, -4px 5px 0 #FFB7C5, 20px 5px 0 #FFB7C5; }
.doll.villain { background: #333; border-radius: 50%; }
.doll.villain::before { width: 14px; height: 14px; background: #FF5252; top: -10px; left: 18px; border-radius: 3px; transform: rotate(45deg); border: 2px solid #333; }

.controls { position: absolute; bottom: 0; width: 100%; height: 120px; background-color: #29B6F6; display: flex; justify-content: space-around; align-items: center; border-top: 5px solid rgba(0,0,0,0.1); }
.ctrl-btn { width: 65px; height: 65px; border-radius: 50%; border: none; background: white; font-size: 26px; cursor: pointer; box-shadow: 0 5px #01579B; display: flex; justify-content: center; align-items: center; }
.ctrl-btn.down { width: 85px; height: 85px; background: #FF5252; color: white; box-shadow: 0 5px #B71C1C; font-size: 16px; font-weight: bold; }

.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: flex; justify-content: center; align-items: center; z-index: 100000; }
.modal-content { 
  background: white; padding: 40px; border-radius: 40px; text-align: center; 
  border: 8px solid #FFD54F; width: 90%; max-width: 450px; 
  animation: bounceIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
@keyframes bounceIn { from { transform: scale(0.5); } to { transform: scale(1); } }

.modal-title { font-size: 2rem; color: #333; margin-bottom: 20px; font-weight: 900; }
.points-wrapper { margin-bottom: 25px; }
.doll-name-tag { background: #F0F0F0; padding: 5px 15px; border-radius: 20px; font-weight: bold; color: #666; margin-bottom: 10px; display: inline-block; }
.point-text { font-size: 2.5rem; font-weight: 900; margin: 0; }
.point-text.plus { color: #58CC02; text-shadow: 2px 2px #E0F2FE; }
.point-text.minus { color: #FF5252; }

#result-doll-display { height: 150px; display: flex; justify-content: center; align-items: center; margin-bottom: 30px; }

.cute-retry-btn {
  background: #FF6B6B; color: white; border: none; padding: 18px 40px; 
  font-size: 1.4rem; font-weight: 800; border-radius: 50px; cursor: pointer;
  box-shadow: 0 8px 0 #FA5252; transition: 0.1s; width: 100%;
}
.cute-retry-btn:active { transform: translateY(4px); box-shadow: 0 4px 0 #FA5252; }

.loading-content { text-align: center; margin-top: 25px; }
.spinner { margin: 0 auto; width: 45px; height: 45px; border: 6px solid #f3f3f3; border-top: 6px solid #FF6B6B; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>