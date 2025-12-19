<template>
  <div class="story-container">
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p class="loading-text">🧚‍♀️ AI 작가님이 동화를 쓰고 있어요...</p>
        <p class="sub-text">잠시만 기다려주세요! (약 30초)</p>
      </div>
    </div>

    <div class="card">
      <h2 class="title">✨ 나만의 동화 만들기</h2>
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
          <span class="small-label">혹시 선택에 없다면 알려주세요! 👉</span>
          <input 
            v-model="customGenre" 
            type="text" 
            class="mini-input" 
            placeholder="직접 입력 (예: 탐정, 모험)"
            @input="selectedGenre = ''" 
          />
        </div>
      </div>

      <div class="form-group">
        <label>동화에 들어갔으면 하는 모든 것! 📝</label>
        <textarea 
          v-model="userPrompt" 
          class="story-input"
          placeholder="ex. 왕자, 공주, 여우, 악당, 마녀, 마법의 성, 숲속마을, 사랑, 전쟁..."
        ></textarea>
      </div>

      <div class="form-group">
        <label>오늘 배울 단어를 넣을까요? 🤔</label>
        <div class="toggle-group">
          <button 
            :class="['toggle-btn', { active: includeWord === true }]"
            @click="includeWord = true"
          >
            🙆‍♀️ 네, 넣어주세요!
          </button>
          <button 
            :class="['toggle-btn', { active: includeWord === false }]"
            @click="includeWord = false"
          >
            🙅‍♂️ 아니요, 괜찮아요!
          </button>
        </div>
      </div>

      <button 
        @click="createStory" 
        class="btn btn-primary full-width"
        :disabled="isLoading"
      >
        {{ isLoading ? '생성 중입니다...' : '이야기 만들기 🚀' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

const router = useRouter()
const store = useCounterStore()

// 상태 관리
const isLoading = ref(false)
const selectedGenre = ref('')
const customGenre = ref('')
const userPrompt = ref('')
const includeWord = ref(true)

// 장르 목록
const genres = [
  { label: '영웅', value: 'hero', icon: '🦸‍♂️' },
  { label: '행복', value: 'happy', icon: '🥰' },
  { label: '슬픔', value: 'sad', icon: '😢' },
  { label: '로맨스', value: 'romance', icon: '💖' },
  { label: '호러', value: 'horror', icon: '👻' },
  { label: '판타지', value: 'fantasy', icon: '🧙‍♂️' },
  { label: 'SF/우주', value: 'sf', icon: '🚀' },
]

// 장르 선택 시 직접 입력창 초기화
const selectGenre = (val) => {
  selectedGenre.value = val
  customGenre.value = '' 
}

// 쉼표로 구분된 키워드를 배열로 변환하는 헬퍼 함수
const parseKeywords = (text) => {
  if (!text) return []
  return text.split(/,| /).map(w => w.trim()).filter(w => w.length > 0)
}

const createStory = async () => {
  // 입력값 검증
  const finalGenre = customGenre.value || selectedGenre.value

  if (!finalGenre) return alert('장르를 선택하거나 직접 입력해주세요!')
  if (!userPrompt.value) return alert('동화에 넣고 싶은 내용을 적어주세요!')
  
  // 백엔드로 보낼 데이터 준비
  const payload = {
    age: 7, // 기본값 (UI에 없으므로)
    story_level: 2, // 기본값 (UI에 없으므로)
    genre: finalGenre,
    keywords: parseKeywords(userPrompt.value),
    // "네"를 선택했다면 study_set_id를 1(임시)로 보냄. 아니면 null
    study_set_id: includeWord.value ? 1 : null, 
    vocab_words: [] // 필요하면 직접 입력받을 수도 있음
  }

  // 로딩 시작
  isLoading.value = true
  
  try {
    console.log('동화 생성 요청:', payload)

    // Axios 요청
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/stories/`, payload, {
      headers: {
        Authorization: `${store.token}` // 스토어의 토큰 사용
      }
    })

    console.log('생성 완료:', response.data)

    // 성공 시 결과 페이지(StoryRead)로 이동
    // (backend에서 id를 반환한다고 가정)
    router.push({ 
      name: 'story-read', 
      params: { id: response.data.id } 
    })

  } catch (error) {
    console.error('동화 생성 실패:', error)
    alert('동화를 만드는 중에 문제가 생겼어요. 잠시 후 다시 시도해주세요! 😥')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.story-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
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
  border: 4px solid transparent;
  transition: transform 0.3s ease;
}

.title { color: var(--primary); font-size: 2rem; margin-bottom: 10px; font-weight: 900; }
.subtitle { color: #888; margin-bottom: 30px; font-weight: 600; }

.form-group { margin-bottom: 30px; text-align: left; }
.form-group label { 
    display: block; 
    font-weight: 800; 
    margin-bottom: 12px; 
    color: var(--text);
    font-size: 1.1rem;
}

/* 1. 장르 버튼 (가로 스크롤 한 줄) */
.genre-scroll-wrapper {
  overflow-x: auto;
  padding-bottom: 10px;
  margin-bottom: 10px;
  scrollbar-width: thin;
  scrollbar-color: #E5E5E5 transparent;
}

.genre-scroll-wrapper::-webkit-scrollbar {
  height: 6px;
}
.genre-scroll-wrapper::-webkit-scrollbar-thumb {
  background-color: #E5E5E5;
  border-radius: 10px;
}

.genre-row {
  display: flex;
  gap: 10px;
  min-width: min-content;
}

.genre-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  height: 80px;
  border: 2px solid #E5E5E5;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  color: #666;
  flex-shrink: 0;
}

.genre-icon { font-size: 1.8rem; margin-bottom: 4px; }
.genre-text { font-size: 0.85rem; font-weight: 700; }

.genre-btn:hover { background: #F7F7F7; transform: translateY(-3px); }

.genre-btn.active {
  border-color: var(--secondary);
  background: #E0F2FE;
  color: var(--secondary);
  box-shadow: 0 4px 10px rgba(28, 176, 246, 0.2);
}

/* 1-2. 직접 입력 박스 (작게) */
.custom-genre-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #F9FAFB;
  padding: 10px 15px;
  border-radius: 15px;
}

.small-label {
  font-size: 0.9rem;
  color: #888;
  font-weight: 600;
  flex-shrink: 0;
}

.mini-input {
  flex: 1;
  padding: 8px 12px;
  border: 2px solid #E5E5E5;
  border-radius: 10px;
  font-size: 0.9rem;
  outline: none;
  font-family: 'Nunito', 'Jua', sans-serif;
}
.mini-input:focus { border-color: var(--purple); background: white; }

/* 2. 텍스트 입력창 */
.story-input {
  width: 100%;
  height: 100px;
  padding: 15px;
  border: 3px solid #E5E5E5;
  border-radius: 20px;
  font-size: 1rem;
  font-family: 'Nunito', 'Jua', sans-serif;
  resize: none;
  outline: none;
  transition: border-color 0.3s;
}

.story-input:focus { border-color: var(--secondary); }
.story-input::placeholder { color: #BBB; font-size: 0.95rem; }

/* 3. 토글 버튼 */
.toggle-group { display: flex; gap: 15px; }

.toggle-btn {
  flex: 1;
  padding: 15px;
  border-radius: 15px;
  border: 2px solid #E5E5E5;
  background: white;
  font-weight: 700;
  color: #888;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.toggle-btn:hover { background: #FAFAFA; }

.toggle-btn.active {
  border-color: var(--primary);
  background: #F0FFF4;
  color: var(--primary-dark);
  box-shadow: 0 4px 10px rgba(88, 204, 2, 0.2);
  font-weight: 800;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  text-align: center;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}
.btn-primary {
  background-color: #FF6B6B; /* 메인 색상 */
  color: white;
}
.btn-primary:hover:not(:disabled) {
  background-color: #FA5252;
  transform: translateY(-2px);
}
.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  transform: none;
}

.full-width { width: 100%; margin-top: 20px; font-size: 1.2rem; padding: 15px; }

/* --- 로딩 오버레이 스타일 --- */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}
.loading-content {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  border: 2px solid #F0F0F0;
}
.loading-text {
  font-size: 1.5rem;
  color: #FF6B6B;
  font-weight: 900;
  margin-top: 20px;
}
.sub-text {
  color: #888;
  margin-top: 10px;
  font-weight: 600;
}
.spinner {
  margin: 0 auto;
  width: 60px;
  height: 60px;
  border: 6px solid #f3f3f3;
  border-top: 6px solid #FF6B6B;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>