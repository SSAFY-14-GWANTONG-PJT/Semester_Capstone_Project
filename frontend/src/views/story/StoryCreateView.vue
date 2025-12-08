<template>
    <div class="story-container">
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
  
        <button @click="createStory" class="btn btn-primary full-width">
          이야기 만들기 🚀
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  // 상태 관리
  const selectedGenre = ref('')
  const customGenre = ref('') // 직접 입력값
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
  
  // 장르 선택 시 직접 입력창 초기화 (선택 버튼 우선)
  const selectGenre = (val) => {
    selectedGenre.value = val
    customGenre.value = '' 
  }
  
  const createStory = () => {
    // 장르값 결정 (직접 입력이 있으면 그것을, 없으면 버튼 선택값을 사용)
    const finalGenre = customGenre.value || selectedGenre.value
  
    if (!finalGenre) return alert('장르를 선택하거나 직접 입력해주세요! 🎭')
    if (!userPrompt.value) return alert('동화에 넣고 싶은 내용을 적어주세요! 📝')
    
    console.log({
      genre: finalGenre,
      prompt: userPrompt.value,
      includeWord: includeWord.value
    })
  
    // 로딩 화면으로 이동
    router.push('/story/loading')
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
    padding-bottom: 10px; /* 스크롤바 공간 확보 및 여백 */
    margin-bottom: 10px;
    /* 스크롤바 숨기기 (선택사항) */
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
    min-width: min-content; /* 내용물만큼 늘어나게 */
  }
  
  .genre-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 80px; /* 버튼 최소 너비 */
    height: 80px;
    border: 2px solid #E5E5E5;
    border-radius: 20px;
    background: white;
    cursor: pointer;
    transition: all 0.2s;
    color: #666;
    flex-shrink: 0; /* 줄어들지 않도록 고정 */
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
  
  .full-width { width: 100%; margin-top: 20px; font-size: 1.2rem; }
  </style>