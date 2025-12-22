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
        <div v-else class="placeholder-img">
          🎨 그림을 불러오는 중...
        </div>
      </div>
      
      <div class="story-content">
        <h1 class="story-title">{{ story.title }}</h1>
        
        <div class="text-box">
          <span class="page-indicator">Page {{ pageIndex + 1 }} / {{ pages.length }}</span>

          <p class="english-text">
            {{ currentPage.content }}
          </p>
          
          </div>

        <div class="action-buttons">
          <button class="btn-icon" @click="playAudio" :disabled="isLoadingAudio">
            <span v-if="isLoadingAudio">⏳ 생성 중...</span>
            <span v-else-if="isPlaying">⏹ 멈추기</span>
            <span v-else>🔊 듣기</span>
          </button>

          <button 
            v-if="pageIndex > 0" 
            class="btn-icon nav-btn" 
            @click="prevPage"
          >
            👈 이전
          </button>

          <button 
            v-if="pageIndex < pages.length - 1" 
            class="btn-icon nav-btn" 
            @click="nextPage"
          >
            다음 👉
          </button>

          <button 
            v-if="pageIndex === pages.length - 1" 
            @click="goQuiz" 
            class="btn btn-primary"
          >
            퀴즈 풀러 가기 🎯
          </button>
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
const store = useCounterStore()

const storyId = route.params.id
const story = ref(null)
const pages = ref([])
const isLoading = ref(true)
const pageIndex = ref(0) 

// 오디오 관련 상태 변수 추가
const isPlaying = ref(false)
const isLoadingAudio = ref(false)
let audioObj = null

const currentPage = computed(() => {
  if (pages.value.length === 0) return {}
  return pages.value[pageIndex.value]
})

onMounted(async () => {
  try {
    const storyRes = await api.get(`/api/stories/${storyId}/`)
    story.value = storyRes.data

    const pagesRes = await api.get(`/api/stories/${storyId}/pages/`)
    pages.value = pagesRes.data.sort((a, b) => a.page_number - b.page_number)

  } catch (error) {
    console.error('동화 로딩 실패:', error)
    alert('동화를 불러오지 못했어요 😭')
    router.push('/')
  } finally {
    isLoading.value = false
  }
})

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

// [핵심] 오디오 재생/정지 통합 함수
const playAudio = async () => {
  // 이미 재생 중이면 멈춤
  if (isPlaying.value) {
    stopAudio()
    return
  }

  // 현재 페이지의 텍스트가 없으면 중단
  const textToRead = currentPage.value.content
  if (!textToRead) return

  try {
    isLoadingAudio.value = true
    
    // Nginx를 통해 AI 컨테이너로 요청 (/ai/generate-tts)
    const response = await axios.post('/ai/generate-tts', {
      text: textToRead,
      voice_name: "Aoede" // 따뜻한 목소리
    })

    // Base64 오디오 재생
    const base64Audio = response.data.audio_data
    const audioSrc = `data:audio/wav;base64,${base64Audio}`
    
    audioObj = new Audio(audioSrc)
    audioObj.onended = () => {
      isPlaying.value = false
    }
    
    audioObj.play()
    isPlaying.value = true

  } catch (error) {
    console.error("TTS 요청 실패:", error)
    alert('선생님 목소리를 불러오지 못했어요. (서버 연결 확인 필요)')
  } finally {
    isLoadingAudio.value = false
  }
}

// 오디오 정지 헬퍼 함수
const stopAudio = () => {
  if (audioObj) {
    audioObj.pause()
    audioObj.currentTime = 0
    audioObj = null
  }
  isPlaying.value = false
}

// 컴포넌트 나갈 때 오디오 정리
onUnmounted(() => {
  stopAudio()
})

const goQuiz = () => {
  router.push(`/story/${storyId}/quiz`)
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
</style>