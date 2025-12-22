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

          <p class="english-text">
            {{ isKoreanMode ? currentPage.content_ko : currentPage.content_en }}
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
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue' // watch, onUnmounted 추가
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios' // 일반 axios 사용 (Nginx /ai 경로 호출 위해)
import api from '@/api/index.js' // 기존 백엔드 호출용
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const router = useRouter()

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

const loadStory = async () => {
  try {
    const storyRes = await api.get(`/api/stories/${storyId}/`)
    story.value = storyRes.data

    const pagesRes = await api.get(`/api/stories/${storyId}/pages/`)
    // DB의 content_ko, content_en 필드명을 확인하세요.
    pages.value = pagesRes.data.sort((a, b) => a.page_number - b.page_number)
  } catch (error) {
    console.error('동화 로딩 실패:', error)
    alert('동화를 불러오지 못했어요 😭')
    router.push('/')
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await loadStory();
  
  // [수정] forEach 대신 for...of를 사용하여 순차적으로 처리
  for (const [index, page] of pages.value.entries()) {
    if (!page.audio_en) {
      // 한 페이지 생성이 완료될 때까지 기다린 후 다음 페이지 요청
      await fetchAudioForPage(page.id, index);
      
      // AI 서버의 부하를 줄이기 위해 요청 사이에 0.5초 정도의 대기 시간을 줍니다.
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  }
});

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
  
  // [수정] forEach 대신 for...of를 사용하여 순차적으로 처리
  // 한 페이지가 완료되어야 다음 페이지로 넘어갑니다.
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
</style>