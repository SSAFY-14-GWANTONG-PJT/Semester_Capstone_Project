<template>
  <div class="pronunciation-container">
    <header class="page-header-cloud">
      <div class="header-content">
        <h1 class="page-title">알파벳 소리법 🪄</h1>
        <p class="page-subtitle">글자를 누르면 어떻게 말할지 나타나요!</p>
      </div>
      <div class="header-curve"></div>
    </header>

    <main class="content-area">
      <div class="alphabet-grid">
        <div 
          v-for="item in phonicsData" 
          :key="item.letter" 
          class="alphabet-card shadow-pop"
          :class="item.color"
          @click="showPhonics(item)"
        >
          <div class="card-inner">
            <div class="letter-group">
              <span class="letter-big">{{ item.letter }}</span>
              <span class="letter-small">{{ item.letter.toLowerCase() }}</span>
            </div>
            <div class="icon-circle">{{ item.icon }}</div>
            <div class="word-text">{{ item.word }}</div>
          </div>
        </div>
      </div>
    </main>

    <Transition name="modal-pop">
      <div v-if="selectedPhonics" class="modal-overlay" @click="selectedPhonics = null">
        <div class="modal-card" @click.stop>
          <div class="modal-header-band" :class="selectedPhonics.color">
            <span class="modal-letter-main">{{ selectedPhonics.letter }}</span>
            <span class="modal-sound-tag">[{{ selectedPhonics.sound }}]</span>
          </div>
          
          <div class="modal-body-content">
            <div class="magic-instruction">
              <div class="magic-icon">👄</div>
              <div class="magic-text">
                <strong>입 모양 규칙</strong>
                <p>{{ selectedPhonics.mouth }}</p>
              </div>
            </div>
            
            <div class="word-magic-box">
              <div class="word-icon-large">{{ selectedPhonics.icon }}</div>
              <div class="word-info">
                <h3 class="en-word">
                  {{ selectedPhonics.word }} 
                  </h3>
                  <span class="kor-pron">[{{ selectedPhonics.korSound }}]</span>
                <p class="ko-word">{{ selectedPhonics.mean }}</p>
              </div>
            </div>
          </div>

          <div class="modal-footer-buttons">
            <button 
              v-if="!isFirstAlphabet" 
              class="modal-btn modal-prev-btn" 
              @click="goToPreviousPhonics"
            >
              이전 발음
            </button>
            <button 
              class="modal-btn modal-next-btn" 
              @click="goToNextPhonics"
            >
              {{ isLastAlphabet ? '공부 완료' : '다음 발음' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedPhonics = ref(null)

// A부터 Z까지 모든 발음 데이터
const phonicsData = [
  { letter: 'A', sound: 'æ', word: 'Apple', korSound: '애:플', mean: '사과', icon: '🍎', mouth: '입을 옆으로 크게 벌리고 "애" 소리를 내요!', color: 'c-red' },
  { letter: 'B', sound: 'b', word: 'Bear', korSound: '베:어', mean: '곰', icon: '🐻', mouth: '입술을 붙였다가 떼며 "브" 하고 소리 내요!', color: 'c-blue' },
  { letter: 'C', sound: 'k', word: 'Cat', korSound: '캐:트', mean: '고양이', icon: '🐱', mouth: '목구멍에서 "크" 소리가 나게 해요!', color: 'c-green' },
  { letter: 'D', sound: 'd', word: 'Dog', korSound: '도:그', mean: '강아지', icon: '🐶', mouth: '혀끝을 윗니 뒤에 붙였다 떼며 "드"!', color: 'c-yellow' },
  { letter: 'E', sound: 'e', word: 'Egg', korSound: '에:그', mean: '계란', icon: '🥚', mouth: '입을 살짝 벌리고 "에" 하고 소리 내요!', color: 'c-purple' },
  { letter: 'F', sound: 'f', word: 'Fish', korSound: '피:쉬', mean: '물고기', icon: '🐟', mouth: '윗니로 아랫입술을 살짝 물고 바람을 "프"!', color: 'c-pink' },
  { letter: 'G', sound: 'g', word: 'Goat', korSound: '고:트', mean: '염소', icon: '🐐', mouth: '목 뒤쪽에서 "그" 하고 소리 내요!', color: 'c-orange' },
  { letter: 'H', sound: 'h', word: 'Hippo', korSound: '히:포', mean: '하마', icon: '🦛', mouth: '입을 벌리고 따뜻한 숨을 "흐"!', color: 'c-teal' },
  { letter: 'I', sound: 'i', word: 'Iguana', korSound: '이:과나', mean: '이구아나', icon: '🦎', mouth: '입을 옆으로 살짝 당기며 "이"!', color: 'c-red' },
  { letter: 'J', sound: 'j', word: 'Jelly', korSound: '젤:리', mean: '젤리', icon: '🍮', mouth: '입술을 앞으로 내밀고 "쥬"!', color: 'c-blue' },
  { letter: 'K', sound: 'k', word: 'Koala', korSound: '코알:라', mean: '코알라', icon: '🐨', mouth: '목 뒤에서 "크" 소리를 내요!', color: 'c-green' },
  { letter: 'L', sound: 'l', word: 'Lion', korSound: '라이:언', mean: '사자', icon: '🦁', mouth: '혀끝을 윗니 뒤에 딱 붙이고 "을~르"!', color: 'c-yellow' },
  { letter: 'M', sound: 'm', word: 'Monkey', korSound: '멍:키', mean: '원숭이', icon: '🐵', mouth: '입술을 꾹 다물고 코로 "음~"!', color: 'c-purple' },
  { letter: 'N', sound: 'n', word: 'Nose', korSound: '노:우즈', mean: '코', icon: '👃', mouth: '입을 벌리고 혀를 천장에 붙여 "은~"!', color: 'c-pink' },
  { letter: 'O', sound: 'ɑ', word: 'Octopus', korSound: '옥:토퍼스', mean: '문어', icon: '🐙', mouth: '입을 동그랗게 벌리고 "아"!', color: 'c-orange' },
  { letter: 'P', sound: 'p', word: 'Pig', korSound: '피:그', mean: '돼지', icon: '🐷', mouth: '입술을 팡! 터뜨리며 "프"!', color: 'c-teal' },
  { letter: 'Q', sound: 'kw', word: 'Queen', korSound: '퀸:', mean: '여왕', icon: '👸', mouth: '입술을 모았다가 "쿠워"!', color: 'c-red' },
  { letter: 'R', sound: 'r', word: 'Rabbit', korSound: '래:빗', mean: '토끼', icon: '🐰', mouth: '혀를 굴리며 "우어"!', color: 'c-blue' },
  { letter: 'S', sound: 's', word: 'Snake', korSound: '스네이:크', mean: '뱀', icon: '🐍', mouth: '치아 사이로 바람을 "스"!', color: 'c-green' },
  { letter: 'T', sound: 't', word: 'Tiger', korSound: '타이:거', mean: '호랑이', icon: '🐯', mouth: '혀끝을 떼며 "트"!', color: 'c-yellow' },
  { letter: 'U', sound: 'ʌ', word: 'Umbrella', korSound: '엄:브렐라', mean: '우산', icon: '☂️', mouth: '입을 편안하게 벌리고 "어"!', color: 'c-purple' },
  { letter: 'V', sound: 'v', word: 'Van', korSound: '밴:', mean: '자동차', icon: '🚐', mouth: '입술을 떨며 "브으"!', color: 'c-pink' },
  { letter: 'W', sound: 'w', word: 'Whale', korSound: '웨:일', mean: '고래', icon: '🐳', mouth: '입술을 모았다 펼치며 "우어"!', color: 'c-orange' },
  { letter: 'X', sound: 'ks', word: 'X-ray', korSound: '엑스:레이', mean: '엑스레이', icon: '🩻', mouth: '"크" 뒤에 "스"를 붙여 "크스"!', color: 'c-teal' },
  { letter: 'Y', sound: 'j', word: 'Yo-yo', korSound: '요:요', mean: '요요', icon: '🪀', mouth: '"이"를 짧게 하고 "이요"!', color: 'c-red' },
  { letter: 'Z', sound: 'z', word: 'Zebra', korSound: '지:브라', mean: '얼룩말', icon: '🦓', mouth: '꿀벌처럼 징~ "즈으"!', color: 'c-blue' }
]

const showPhonics = (item) => {
  selectedPhonics.value = item
}

const isLastAlphabet = computed(() => {
  if (!selectedPhonics.value) return false
  return selectedPhonics.value.letter === 'Z'
})

const isFirstAlphabet = computed(() => {
  if (!selectedPhonics.value) return false
  return selectedPhonics.value.letter === 'A'
})


// 이전 발음으로 이동 로직 수정
const goToPreviousPhonics = () => {
  const currentIndex = phonicsData.findIndex(item => item.letter === selectedPhonics.value.letter)
  if (currentIndex > 0) {
    selectedPhonics.value = phonicsData[currentIndex - 1]
  }
}

// 다음 발음으로 이동 로직
const goToNextPhonics = () => {
  if (isLastAlphabet.value) {
    selectedPhonics.value = null
    return
  }
  const currentIndex = phonicsData.findIndex(item => item.letter === selectedPhonics.value.letter)
  if (currentIndex !== -1 && currentIndex < phonicsData.length - 1) {
    selectedPhonics.value = phonicsData[currentIndex + 1]
  }
}
</script>

<style scoped>
/* 전체 레이아웃 */
.pronunciation-container {
  min-height: 100vh;
  background-color: #F8FAFC;
  padding-bottom: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 둥근 구름 헤더 */
.page-header-cloud {
  width: 100%;
  background: white;
  padding: 40px;
  position: relative;
  border-radius: 0 0 60px 60px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.header-content { max-width: 600px; margin: 0 auto; }

.back-link {
  position: absolute;
  top: 20px; left: 20px;
  background: #F1F5F9; border: none;
  padding: 8px 16px; border-radius: 20px;
  font-weight: 800; color: #64748B; cursor: pointer;
}

.page-title { font-size: 2.2rem; font-weight: 900; color: #1E293B; margin-bottom: 8px; }
.page-subtitle { color: #3B82F6; font-weight: 800; font-size: 1.1rem; }

/* 알파벳 그리드 */
.content-area {
  width: 100%;
  max-width: 800px;
  padding: 20px;
}

.alphabet-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 15px;
}

.alphabet-card {
  background: white;
  border-radius: 30px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 6px 0 #E2E8F0;
  border: 3px solid transparent;
}

.alphabet-card:hover { transform: translateY(-5px); }
.alphabet-card:active { transform: translateY(3px); box-shadow: none; }

.letter-group { display: flex; align-items: baseline; gap: 4px; }
.letter-big { font-size: 2.2rem; font-weight: 900; }
.letter-small { font-size: 1.1rem; font-weight: 800; opacity: 0.4; }

.icon-circle {
  width: 55px; height: 55px; background: #F8FAFC;
  border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-size: 2rem; margin: 12px auto;
}

.word-text { font-size: 0.9rem; font-weight: 800; color: #64748B; }

/* 컬러 테마 */
.c-red { color: #FF6B81; } .c-blue { color: #60A5FA; } .c-green { color: #34D399; }
.c-yellow { color: #FBBF24; } .c-purple { color: #A78BFA; } .c-pink { color: #F472B6; }
.c-orange { color: #FB923C; } .c-teal { color: #2DD4BF; }

/* 모달: 정중앙 고정 */
.modal-overlay {
  position: fixed;
  inset: 0; /* top, left, right, bottom 0과 동일 */
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-card {
  background: white;
  width: 90%;
  max-width: 400px;
  border-radius: 45px;
  padding: 35px;
  box-shadow: 0 25px 50px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  gap: 20px;
  text-align: center;
}

.modal-header-band {
  padding: 20px; border-radius: 30px; color: white;
  display: flex; justify-content: center; align-items: baseline; gap: 10px;
}
.modal-header-band.c-red { background: #FF6B81; }
.modal-header-band.c-blue { background: #60A5FA; }
.modal-header-band.c-green { background: #34D399; }
.modal-header-band.c-yellow { background: #FBBF24; }
.modal-header-band.c-purple { background: #A78BFA; }
.modal-header-band.c-pink { background: #F472B6; }
.modal-header-band.c-orange { background: #FB923C; }
.modal-header-band.c-teal { background: #2DD4BF; }

.modal-letter-main { font-size: 4.5rem; font-weight: 900; }
.modal-sound-tag { font-size: 1.8rem; font-weight: 800; opacity: 0.9; }

.magic-instruction {
  background: #F0F9FF; padding: 20px; border-radius: 25px;
  display: flex; align-items: center; gap: 15px; text-align: left;
}
.magic-icon { font-size: 2.5rem; }
.magic-text strong { display: block; color: #0369A1; font-size: 1rem; margin-bottom: 4px; }
.magic-text p { margin: 0; font-size: 0.95rem; color: #475569; font-weight: 700; line-height: 1.4; }

.word-magic-box { display: flex; align-items: center; justify-content: center; gap: 20px; margin: 10px 0; }
.word-icon-large { font-size: 4.5rem; }
.en-word { font-size: 1.8rem; font-weight: 900; color: #1E293B; margin: 0; }
.kor-pron { font-size: 1.2rem; color: #FF6B81; font-weight: 800; }
.ko-word { font-size: 1.3rem; color: #64748B; font-weight: 800; margin: 0; }

.modal-footer-buttons {
  display: flex;
  gap: 12px;
  width: 100%;
}

.modal-btn {
  flex-grow: 1; /* 버튼이 하나든 둘이든 꽉 채우도록 설정 */
  border: none;
  padding: 18px;
  border-radius: 20px;
  font-weight: 900;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-prev-btn {
  background: #6cc57b;
  color: white;
  box-shadow: 0 6px 0 #368554;
}

.modal-next-btn {
  background: #3B82F6;
  color: white;
  box-shadow: 0 6px 0 #1D4ED8;
}

.modal-btn:active {
  transform: translateY(4px);
  box-shadow: none;
}

/* 모달 애니메이션 */
.modal-pop-enter-active { animation: pop-in 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.modal-pop-leave-active { animation: pop-in 0.3s reverse; }
@keyframes pop-in {
  0% { transform: scale(0.5); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.slide-fade-enter-active { transition: all 0.3s ease-out; }
.slide-fade-enter-from { transform: translateX(20px); opacity: 0; }
</style>