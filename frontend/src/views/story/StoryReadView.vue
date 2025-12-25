<template>
<div class="read-container" v-if="!isLoading && story && pages.length > 0">
    <div class="book-card">
      <div class="story-image">
        <img 
          v-if="currentPage.image_data" 
          :src="`data:image/png;base64,${currentPage.image_data}`" 
          alt="삽화"
          class="real-image"
        />
        <div v-else class="placeholder-img">🎨 그림을 불러오는 중...</div>
      </div>
      
      <div class="story-content">
        <h1 class="story-title">{{ story.title }}</h1>
        
        <div class="text-box">
          <span class="page-indicator">Page {{ pageIndex + 1 }} / {{ pages.length }}</span>

          <p class="english-text" v-html="highlightContent(isKoreanMode ? currentPage.content_ko : currentPage.content_en)">
          </p>
          
          <button class="btn-translate" @click="isKoreanMode = !isKoreanMode">
            {{ isKoreanMode ? '🔤 English Mode' : '🇰🇷 한글로 읽기' }}
          </button>
        </div>

        <div class="action-buttons">
          <button class="btn-icon" @click="playAudio" :disabled="!currentPage.audio_en">
            <span v-if="!currentPage.audio_en">⏳ 목소리 준비 중...</span>
            <span v-else-if="isPlaying">⏹ 멈추기</span>
            <span v-else>🔊 듣기</span>
          </button>

          <button v-if="pageIndex > 0" class="btn-icon nav-btn" @click="prevPage">👈 이전</button>
          <button v-if="pageIndex < pages.length - 1" class="btn-icon nav-btn" @click="nextPage">다음 👉</button>
          <button v-if="pageIndex === pages.length - 1" @click="goQuiz" class="btn btn-primary">퀴즈 풀러 가기 🎯</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="loading-container">
    <p>📖 동화책을 펼치는 중이에요...</p>
  </div>

  <div v-if="story && story.author_email !== store.email" class="like-container">
  <button @click="toggleLike" :class="['like-button', { 'active': story.is_liked }]">
    <i :class="[story.is_liked ? 'fas' : 'far', 'fa-heart']"></i>
    <span>좋아요 {{ story.like_count }}</span>
  </button>
</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue' // watch, onUnmounted 추가
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios' // 일반 axios 사용 (Nginx /ai 경로 호출 위해)
import api from '@/api/index.js' // 기존 백엔드 호출용
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()

const storyId = route.params.id
const story = ref(null)
const pages = ref([])
const isLoading = ref(true)
const pageIndex = ref(0) 
const isKoreanMode = ref(false) // 번역 모드 상태

// 오디오 관련 상태 변수 추가
const isPlaying = ref(false)
let audioObj = null

const currentPage = computed(() => {
  if (pages.value.length === 0) return {}
  return pages.value[pageIndex.value]
})

// [추가] 퀴즈 미리 생성 함수
const prefetchQuiz = async () => {
  try {
    console.log("🤖 퀴즈 데이터를 백그라운드에서 생성 중...");
    // num_questions는 기본값 3개 (필요시 조정)
    await api.post(`/api/stories/${storyId}/questions/`, { num_questions: 3 });
    console.log("✅ 퀴즈 생성 완료 (대기열 등록됨)");
  } catch (error) {
    // 백그라운드 작업이므로 에러가 나도 사용자에게 알림을 띄우지 않고 콘솔에만 남김
    console.warn("퀴즈 미리 생성 실패 (사용자가 퀴즈 버튼 누를 때 다시 시도됩니다):", error);
  }
}

const loadStory = async () => {
  try {
    const storyRes = await api.get(`/api/stories/${storyId}/`)
    story.value = storyRes.data

    const pagesRes = await api.get(`/api/stories/${storyId}/pages/`)
    pages.value = pagesRes.data.sort((a, b) => a.page_number - b.page_number)
    
    // 동화 로딩이 성공하면, 즉시 퀴즈 생성을 요청합니다.
    prefetchQuiz();

  } catch (error) {
    console.error('동화 로딩 실패:', error)
    alert('동화를 불러오지 못했어요 😭')
    router.push('/')
  } finally {
    isLoading.value = false
  }
}

// 동화 내용 중 ** ** or * * 사이 하이라이트
const highlightContent = (text) => {
  if (!text) return '';
  // 정규식 설명: (\*\*|\*) -> ** 또는 * 로 시작하고, (.*?) -> 내용을 잡고, \1 -> 시작했던 것과 같은 기호로 끝남
  return text.replace(/(\*\*|\*)(.*?)\1/g, '<span class="highlight-word">$2</span>');
}

// 페이지 넘길 때 오디오 끄기
watch(pageIndex, () => {
  stopAudio()
})

// 페이지 이동 함수
const nextPage = () => {
  if (pageIndex.value < pages.value.length - 1) pageIndex.value++
}
const prevPage = () => {
  if (pageIndex.value > 0) pageIndex.value--
}

const playAudio = () => {
  if (isPlaying.value) { stopAudio(); return }
  if (!currentPage.value.audio_en) return

  const audioSrc = `data:audio/wav;base64,${currentPage.value.audio_en}`
  audioObj = new Audio(audioSrc)
  audioObj.onended = () => { isPlaying.value = false }
  audioObj.play()
  isPlaying.value = true
}

// 오디오 정지 헬퍼 함수
const stopAudio = () => {
  if (audioObj) { audioObj.pause(); audioObj.currentTime = 0; audioObj = null }
  isPlaying.value = false
}
// 컴포넌트 나갈 때 오디오 정리
onUnmounted(() => {
  stopAudio()
})

const goQuiz = () => {
  router.push(`/story/${storyId}/quiz`)
}


onMounted(async () => {
  await loadStory();
  
  for (let i = 0; i < pages.value.length; i++) {
    const page = pages.value[i];
    if (!page.audio_en) {
      console.log(`${i + 1}페이지 음성 생성 시작...`);
      await fetchAudioForPage(page.id, i);
      
      // AI 서버의 안정성을 위해 요청 사이에 1초의 간격을 둡니다.
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
});

const fetchAudioForPage = async (pageId, index) => {
  try {
    const res = await api.post(`/api/stories/page/${pageId}/tts/`)
    if (res.data.audio_en) {
      pages.value[index].audio_en = res.data.audio_en
    }
  } catch (err) {
    console.error(`${index + 1}페이지 오디오 생성 실패:`, err)
  }
}

// 좋아요 기능
const toggleLike = async () => {
  try {
    const res = await api.post(`/api/stories/${storyId}/like/`)
    // 서버 응답값으로 실시간 반영
    story.value.is_liked = res.data.is_liked
    story.value.like_count = res.data.like_count
  } catch (err) {
    console.error('좋아요 실패:', err)
  }
}
</script>

<style scoped>
.read-container { padding: 40px 20px; max-width: 100%; margin: 0 auto; min-height: 80vh; display: flex; align-items: center; }
.loading-container { text-align: center; font-size: 1.5rem; margin-top: 100px; font-weight: bold; color: #888; }

.book-card {
  width: 100%;
  background: white; border-radius: 40px; overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.1); display: flex; flex-direction: column;
  border: 4px solid #fff;
}

.story-image { 
  height: 350px; 
  background: #E0F2FE; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  overflow: hidden;
}

.real-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.5s ease;
}
.real-image:hover { transform: scale(1.05); }

.placeholder-img { font-size: 1.2rem; color: #1cb0f6; opacity: 0.7; font-weight: bold;}

.story-content { padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }
.story-title { font-size: 2.2rem; color: #333; margin-bottom: 20px; text-align: center; font-weight: 900; word-break: keep-all; }

.text-box { 
  background: #FFF9E5; padding: 30px; border-radius: 20px; margin-bottom: 30px;
  border: 3px dashed #FFD700;
  position: relative;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.page-indicator {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 0.8rem;
  color: #aaa;
  font-weight: bold;
}

.english-text { font-size: 1.4rem; margin-bottom: 15px; line-height: 1.6; color: #444; font-family: 'Nunito', sans-serif; }
.korean-text { color: #888; font-size: 1rem; margin-top: 10px; }

.action-buttons { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.btn-icon {
  background: #f0f0f0; border: none; padding: 12px 20px; border-radius: 50px;
  font-weight: bold; cursor: pointer; font-size: 1rem; color: #555;
  transition: all 0.2s;
}
.btn-icon:hover { background: #e0e0e0; transform: translateY(-2px); }

.nav-btn { background: #E0F2FE; color: #0099FF; }
.nav-btn:hover { background: #B3E5FC; }

.btn-primary {
  background-color: #FF6B6B; color: white; border: none; padding: 12px 25px;
  border-radius: 50px; font-weight: bold; cursor: pointer; font-size: 1.1rem;
  box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3);
  transition: transform 0.2s;
}
.btn-primary:hover { transform: translateY(-3px); background-color: #FA5252; }

:deep(.highlight-word) {
  background-color: #fffcf7;
  border: 2px solid #dfaa78;
  border-radius: 8px;
  padding: 0 6px;
  margin: 0 2px;
  font-weight: 800;
  color: #e97a31;
  box-shadow: 2px 2px 0px rgba(255, 230, 156, 0.5);
  display: inline-block;
}

@media (min-width: 768px) {
  .book-card { flex-direction: row; min-height: 500px; }
  .story-image { flex: 1; height: auto; }
  .story-content { flex: 1; overflow-y: auto; }
}

.btn-translate {
  margin-top: 15px;
  padding: 8px 15px;
  background: #fff;
  border: 2px solid #FFD700;
  border-radius: 15px;
  cursor: pointer;
  font-weight: bold;
  color: #555;
  transition: all 0.2s;
}

.like-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
  padding-bottom: 50px;
}
.like-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 25px;
  border-radius: 50px;
  border: 2px solid #FF6B6B;
  background: white;
  color: #FF6B6B;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
}
.like-button.active {
  background: #FF6B6B;
  color: white;
}
.like-button:hover {
  transform: scale(1.05);
}
</style>