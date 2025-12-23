<template>
  <div class="grammar-container">
    <header class="grammar-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-info">
            <div class="lesson-number">{{ currentType + 1 }} / {{ grammarData.length }}</div>
            <div class="lesson-title">문장 만드는 방법</div>
          </div>
        </div>
        <div class="header-right">
          <div class="star-badge">
            <span class="star-icon">⭐</span>
          </div>
        </div>
      </div>
      
      <div class="progress-wrapper">
        <div class="progress-bar">
          <div 
            class="progress-fill"
            :style="{ width: ((currentType + 1) / grammarData.length) * 100 + '%' }"
          ></div>
        </div>
      </div>
    </header>

    <Transition name="modal-fade">
      <div v-if="showIntro" class="intro-overlay" @click="showIntro = false">
        <div class="intro-card" @click.stop>
          <h2 class="intro-title">왜 문장 규칙을 배울까요?</h2>
          <div class="intro-content">
            <div class="intro-item pink">
              <span class="intro-emoji">💬</span>
              <div class="intro-text">
                <strong>기본적인 언어 규칙</strong>
                <p>내 생각을 친구들에게 더 잘 말할 수 있어요!</p>
              </div>
            </div>
            <div class="intro-item blue">
              <span class="intro-emoji">🎨</span>
              <div class="intro-text">
                <strong>여러 단어의 조합으로 문장 만들기</strong>
                <p>레고처럼 단어를 조립하면 문장이 뚝딱!</p>
              </div>
            </div>
          </div>
          <button class="intro-start-btn" @click="showIntro = false">
            놀이 시작!
          </button>
        </div>
      </div>
    </Transition>

    <main class="grammar-content">
      <Transition name="slide-fade" mode="out-in">
        <div :key="currentType" class="lesson-card">
          <div class="lesson-header">
            <div class="mascot-large">{{ currentData.mascot }}</div>
            <h1 class="lesson-main-title">{{ currentData.title }}</h1>
            <p class="lesson-description">{{ currentData.description }}</p>
          </div>

          <div class="structure-blocks">
            <div 
              v-for="(part, index) in currentData.structure" 
              :key="index"
              class="structure-block"
              :class="[`block-${part.type}`]"
              @click="showDetail(part)"
            >
              <div class="block-top">
                <span class="part-icon">{{ getEmojiIcon(part.icon) }}</span>
              </div>
              <div class="block-bottom">
                <div class="block-label">{{ part.label }}</div>
                <div class="block-name">{{ part.name }}</div>
              </div>
            </div>
          </div>

          <div class="example-section">
            <div class="example-bubble">
              <div class="example-tag">이렇게 말해요!</div>
              <p class="example-en">{{ currentData.exampleEn }}</p>
              <p class="example-ko">{{ currentData.exampleKo }}</p>
            </div>
          </div>
        </div>
      </Transition>

      <div class="navigation-buttons">
        <button class="nav-btn prev" :disabled="currentType === 0" @click="prevType">이전으로</button>
        <button class="nav-btn next" @click="nextType">
          {{ currentType === grammarData.length - 1 ? '이해했어요' : '다음으로' }}
        </button>
      </div>
    </main>

    <Transition name="modal-fade">
      <div v-if="selectedPart" class="modal-overlay" @click="selectedPart = null">
        <div class="modal-card" @click.stop>
          <div class="modal-icon-header" :class="`bg-${selectedPart.type}`">
            {{ getEmojiIcon(selectedPart.icon) }}
          </div>
          <h3 class="modal-title">{{ selectedPart.name }} ({{ selectedPart.label }})</h3>
          <p class="modal-description">{{ selectedPart.desc }}</p>
          <div class="modal-tip">💡 {{ selectedPart.tip }}</div>
          <button class="modal-close-btn" @click="selectedPart = null">알겠어요! 👍</button>
        </div>
      </div>
    </Transition>

    <div v-if="showCelebration" class="celebration-overlay">
      <div class="celebration-emoji">🎉</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentType = ref(0)
const selectedPart = ref(null)
const completedTypes = ref([])
const showCelebration = ref(false)
const showIntro = ref(true)

const grammarData = [
  {
    title: "씩씩하게 달려요!",
    description: "주인공이 혼자서 무엇을 하는지 말해요.",
    exampleEn: "Jane runs fast.",
    exampleKo: "제인이 빠르게 달려요.",
    mascot: "🏃",
    structure: [
      { name: "주인공", label: "S", type: "subject", icon: "user", desc: "이야기의 주인공이에요!", tip: "누구인지 먼저 말해요." },
      { name: "행동", label: "V", type: "verb", icon: "zap", desc: "주인공이 하는 동작이에요!", tip: "달려요, 먹어요처럼 동작을 나타내요." }
    ]
  },
  {
    title: "나는 이런 사람이에요!",
    description: "주인공이 누구인지 설명해줘요.",
    exampleEn: "I am a student.",
    exampleKo: "나는 학생이에요.",
    mascot: "😊",
    structure: [
      { name: "주인공", label: "S", type: "subject", icon: "user", desc: "주인공!", tip: "나, 너처럼 누구인지 말해요." },
      { name: "이다", label: "V", type: "verb", icon: "link", desc: "주인공과 설명을 이어줘요.", tip: "~이에요로 연결해요." },
      { name: "설명", label: "C", type: "complement", icon: "sparkles", desc: "상태나 직업을 알려줘요.", tip: "행복해요처럼 설명해요." }
    ]
  },
  {
    title: "무엇을 좋아해요!",
    description: "좋아하는 대상을 말해요.",
    exampleEn: "I love chocolate.",
    exampleKo: "나는 초콜릿을 좋아해요.",
    mascot: "❤️",
    structure: [
      { name: "주인공", label: "S", type: "subject", icon: "user", desc: "마음을 가진 주인공!", tip: "누구인지 말해요." },
      { name: "행동", label: "V", type: "verb", icon: "heart", desc: "동작이나 마음을 말해요.", tip: "좋아해요처럼 말해요." },
      { name: "대상", label: "O", type: "object", icon: "target", desc: "행동을 받는 대상이에요.", tip: "'~을/를'을 붙여요." }
    ]
  },
  {
    title: "선물을 나눠줘요!",
    description: "누구에게 무엇을 주는지 말해요.",
    exampleEn: "Mom gave me a toy.",
    exampleKo: "엄마가 나에게 선물을 주셨어요.",
    mascot: "🎁",
    structure: [
      { name: "주인공", label: "S", type: "subject", icon: "user", desc: "주는 주인공!", tip: "엄마, 아빠처럼 누구인지 말해요." },
      { name: "주기", label: "V", type: "verb", icon: "gift", desc: "나눠주는 행동이에요.", tip: "줘요, 사줘요처럼 말해요." },
      { name: "받는이", label: "I.O", type: "object-sub", icon: "user-plus", desc: "받는 친구!", tip: "'~에게'를 붙여요." },
      { name: "선물", label: "D.O", type: "object", icon: "gift-box", desc: "진짜 물건!", tip: "장난감을 처럼 말해요." }
    ]
  },
  {
    title: "마법의 변신!",
    description: "대상을 다르게 변화시켜요.",
    exampleEn: "Music makes me happy.",
    exampleKo: "음악이 나를 행복하게 해요.",
    mascot: "✨",
    structure: [
      { name: "주인공", label: "S", type: "subject", icon: "user", desc: "마법을 부리는 주인공!", tip: "변화를 만드는 주인공!" },
      { name: "만들기", label: "V", type: "verb", icon: "wand", desc: "변하게 하는 마법!", tip: "만들어요처럼 말해요." },
      { name: "대상", label: "O", type: "object", icon: "target", desc: "마법에 걸린 친구!", tip: "나를, 친구를처럼 말해요." },
      { name: "변신", label: "O.C", type: "complement", icon: "sparkles", desc: "변신한 모습!", tip: "행복하게처럼 설명해요." }
    ]
  }
]

const currentData = computed(() => grammarData[currentType.value])

const getEmojiIcon = (iconName) => {
  const map = {
    'user': '👦', 'zap': '⚡', 'link': '🔗', 'sparkles': '✨', 'heart': '❤️',
    'target': '🎯', 'gift': '🎁', 'user-plus': '👫', 'gift-box': '🧸', 'wand': '🪄'
  }
  return map[iconName] || '💎'
}

const nextType = () => {
  if (!completedTypes.value.includes(currentType.value)) {
    completedTypes.value.push(currentType.value)
    showCelebration.value = true
    setTimeout(() => { showCelebration.value = false }, 1500)
  }
  if (currentType.value < grammarData.length - 1) {
    currentType.value++
  } else {
    router.push('/learning/today')
  }
}

const prevType = () => { if (currentType.value > 0) currentType.value-- }
const showDetail = (part) => { selectedPart.value = part }
</script>

<style scoped>
.grammar-container {
  min-height: 100vh;
  background-color: #F0F9FF;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 헤더 */
.grammar-header {
  width: 100%;
  background: white;
  padding: 15px 20px;
  border-bottom: 4px solid #E2E8F0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.duo-mascot { font-size: 2rem; }
.lesson-title { font-weight: 900; color: #1E293B; }

.star-badge {
  background: #FFD43B;
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: 900;
  box-shadow: 0 4px 0 #FAB005;
}

.progress-wrapper { max-width: 600px; margin: 10px auto 0; }
.progress-bar { height: 12px; background: #E2E8F0; border-radius: 10px; overflow: hidden; }
.progress-fill { height: 100%; background: #4ADE80; transition: width 0.5s ease; }

/* 모달 레이아웃 수정 핵심 */
.intro-overlay, .modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* 무조건 맨 위 */
}

.intro-title {
    padding-bottom: 20px;
}

.intro-card, .modal-card {
  background: white;
  padding: 30px;
  border-radius: 40px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  text-align: center;
}

.intro-item {
  display: flex; align-items: center; gap: 15px;
  padding: 25px; border-radius: 20px; margin-bottom: 10px; text-align: left;
}
.intro-item.pink { background: #FFF1F2; }
.intro-item.blue { background: #EFF6FF; }
.intro-item strong { display: block; color: #1E293B; }
.intro-item p { margin: 0; font-size: 0.9rem; color: #64748B; }

.intro-start-btn {
    margin-top:10px;
  width: 100%; padding: 15px; background: #4ADE80;
  border: none; border-radius: 20px; color: white;
  font-weight: 900; font-size: 1.1rem; cursor: pointer;
  box-shadow: 0 6px 0 #16A34A;
}

/* 메인 카드 */
.grammar-content { width: 100%; max-width: 500px; padding: 20px; }
.lesson-card {
  background: white; padding: 30px; border-radius: 40px;
  box-shadow: 0 8px 0 #CBD5E1; text-align: center;
}

.mascot-large { font-size: 4rem; margin-bottom: 10px; }
.lesson-main-title { font-size: 1.6rem; font-weight: 900; color: #1E293B; }

.structure-blocks {
  display: flex; justify-content: center; gap: 10px;
  margin: 30px 0; flex-wrap: wrap;
}

.structure-block {
  width: 85px; height: 100px; border-radius: 20px;
  cursor: pointer; position: relative;
  display: flex; flex-direction: column;
}

.block-top { height: 40%; display: flex; justify-content: center; align-items: center; background: rgba(255,255,255,0.2); border-radius: 20px 20px 0 0; }
.block-bottom { height: 60%; display: flex; flex-direction: column; justify-content: center; color: white; }
.block-label { font-size: 1.2rem; font-weight: 900; }
.block-name { font-size: 0.7rem; font-weight: 800; }

.block-subject { background: #60A5FA; box-shadow: 0 5px 0 #2563EB; }
.block-verb { background: #F87171; box-shadow: 0 5px 0 #DC2626; }
.block-complement { background: #FBBF24; box-shadow: 0 5px 0 #D97706; }
.block-object { background: #34D399; box-shadow: 0 5px 0 #059669; }
.block-object-sub { background: #A78BFA; box-shadow: 0 5px 0 #7C3AED; }

.example-bubble {
  background: #F8FAFC; padding: 20px; border-radius: 25px;
  border: 2px dashed #CBD5E1; position: relative; margin-top: 20px;
}
.example-tag { position: absolute; top: -12px; left: 20px; background: #1E293B; color: white; font-size: 0.7rem; padding: 3px 10px; border-radius: 10px; }
.example-en { font-size: 1.5rem; font-weight: 900; color: #1E293B; margin-bottom: 5px; }
.example-ko { color: #64748B; font-weight: 700; }

/* 하단 버튼 */
.navigation-buttons { display: flex; gap: 15px; margin-top: 20px; }
.nav-btn { flex: 1; padding: 15px; border: none; border-radius: 20px; font-weight: 900; cursor: pointer; }
.nav-prev { background: white; color: #94A3B8; box-shadow: 0 5px 0 #E2E8F0; }
.nav-next { background: #3B82F6; color: white; box-shadow: 0 5px 0 #1D4ED8; }

.modal-icon-header { width: 70px; height: 70px; border-radius: 50%; margin: 0 auto 15px; display: flex; justify-content: center; align-items: center; font-size: 2.5rem; color: white; }
.modal-tip { background: #FFFBEB; padding: 10px; border-radius: 15px; margin: 15px 0; font-size: 0.9rem; font-weight: 700; color: #92400E; }
.modal-close-btn { width: 100%; padding: 12px; background: #1E293B; color: white; border: none; border-radius: 15px; font-weight: 800; cursor: pointer; }

/* 애니메이션 */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.slide-fade-enter-active { transition: all 0.3s ease-out; }
.slide-fade-enter-from { transform: translateX(20px); opacity: 0; }

.celebration-overlay { position: fixed; inset: 0; display: flex; justify-content: center; align-items: center; font-size: 8rem; z-index: 10000; animation: celebrate 1.5s forwards; }
@keyframes celebrate { 0% { transform: scale(0); opacity: 0; } 50% { transform: scale(1.2); opacity: 1; } 100% { transform: scale(2); opacity: 0; } }
</style>