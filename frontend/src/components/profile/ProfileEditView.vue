<template>
  <div class="edit-page-container">
    <div class="floating-bg">
      <div class="cloud">☁️</div>
      <div class="cloud">☁️</div>
      <div class="star">✨</div>
      <div class="star">🌟</div>
    </div>

    <main class="container">
      <div class="edit-box">
        <div class="edit-header">
          <div class="back-link" @click="router.back()">⬅️ 돌아가기</div>
          <h1>내 정보 수정하기 ✏️</h1>
          <p>더 멋진 모험가로 변신해볼까요?</p>
        </div>

        <div class="avatar-section">
          <div class="avatar-circle">
            <span class="current-emoji">🐤</span>
            <div class="edit-badge">📸</div>
          </div>
          <p class="email-info">현재 모험가 계정 정보</p>
        </div>

        <form @submit.prevent="updateProfileHandler">
          <div class="form-grid">
            <div class="form-group full-width">
              <label for="email">이메일 주소</label>
              <div class="input-wrapper">
                <input type="email" id="email" v-model="editForm.email" placeholder="이메일을 입력하세요">
                <i class="fas fa-envelope input-icon"></i>
              </div>
            </div>

            <div class="form-group full-width">
              <label for="password">새 비밀번호 (변경할 때만 입력)</label>
              <div class="input-wrapper">
                <input type="password" id="password" v-model="editForm.password" placeholder="바꿀 비밀번호를 입력하세요">
                <i class="fas fa-lock input-icon"></i>
              </div>
            </div>

            <div class="form-group full-width">
              <label for="passwordConfirm">새 비밀번호 확인</label>
              <div class="input-wrapper">
                <input type="password" id="passwordConfirm" v-model="editForm.passwordConfirm" placeholder="한 번 더 입력해주세요">
                <i class="fas fa-check-double input-icon"></i>
              </div>
              <p v-if="editForm.password && editForm.password !== editForm.passwordConfirm" class="error-text">
                ❌ 비밀번호가 서로 달라요!
              </p>
            </div>

            <div class="form-group full-width">
              <label for="nickname">새로운 닉네임</label>
              <div class="input-wrapper">
                <input type="text" id="nickname" v-model="editForm.nickname" placeholder="닉네임을 입력하세요">
                <i class="fas fa-user input-icon"></i>
              </div>
            </div>

            <div class="form-group">
              <label for="age">아이 나이 (수정 불가)</label>
              <div class="input-wrapper">
                <select id="age" v-model="editForm.age" disabled class="disabled-input">
                  <option v-for="n in 8" :key="n" :value="n + 2">{{ n + 2 }}세</option>
                </select>
                <i class="fas fa-birthday-cake input-icon"></i>
              </div>
            </div>

            <div class="form-group">
              <label for="level">학습 레벨 (수정 불가)</label>
              <div class="input-wrapper">
                <select id="level" v-model="editForm.level" disabled class="disabled-input">
                  <option v-for="l in 10" :key="l" :value="l">Lv.{{ l }}</option>
                </select>
                <i class="fas fa-layer-group input-icon"></i>
              </div>
            </div>
          </div>

          <div class="btn-group">
            <button type="button" class="btn btn-secondary" @click="router.back()">취소</button>
            <button type="submit" class="btn btn-primary edit">변경사항 저장 💾</button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from '@/api/index.js'

const router = useRouter()
const store = useCounterStore()

const editForm = reactive({
  nickname: '',
  email: '',
  password: '',        
  passwordConfirm: '', 
  age: null,
  level: 0,
})

// 1. 기존 프로필 정보 가져오기
onMounted(async () => {
  try {
    // [수정] 이제 헤더를 직접 넣을 필요가 없습니다! 인터셉터가 알아서 해줍니다.
    const res = await axios.get('/api/accounts/profile/') 
    
    editForm.nickname = res.data.nickname
    editForm.email = res.data.email
    editForm.age = res.data.age
    editForm.level = res.data.level
  } catch (err) {
    console.error("정보를 불러오지 못했습니다.", err)
    // 인터셉터에서 리프레시까지 실패했을 때만 이 블록으로 옵니다.
    alert("로그인이 필요하거나 세션이 완전히 만료되었습니다.")
    router.push('/login')
  }
})

// 2. 프로필 수정 요청 (PUT 또는 PATCH)
const updateProfileHandler = async () => {
  // 1. 비밀번호 일치 여부 확인
  if (editForm.password && editForm.password !== editForm.passwordConfirm) {
    alert("비밀번호 확인이 일치하지 않아요! 🥺")
    return
  }

  try {
    // 2. 서버로 보낼 데이터 준비 (비밀번호가 비어있으면 보내지 않음)
    const payload = {
      nickname: editForm.nickname,
      email: editForm.email,
    }
    if (editForm.password) {
      payload.password = editForm.password
    }

    await axios.patch('/api/accounts/profile/edit/', payload)
    
    store.nickname = editForm.nickname
    alert("성공적으로 수정되었습니다! ✨")
    router.push({ name: 'mypage' })
  } catch (err) {
    alert("수정에 실패했습니다.\n입력하신 정보를 다시 확인해주세요.")
  }
}
</script>

<style scoped>
/* 배경 장식 */
.edit-page-container {
  min-height: 100vh;
  padding: 60px 20px;
  background: linear-gradient(180deg, #FFF9E5 0%, #FFFFFF 100%);
  position: relative;
  overflow: hidden;
}

.floating-bg { position: fixed; width: 100%; height: 100%; pointer-events: none; top: 0; left: 0; }
.cloud { position: absolute; font-size: 50px; opacity: 0.2; }
.cloud:nth-child(1) { top: 10%; left: 5%; }
.cloud:nth-child(2) { top: 20%; right: 10%; }
.star { position: absolute; font-size: 30px; opacity: 0.3; }

/* 메인 박스 */
.edit-box {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  border-radius: 40px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
  border: 4px solid #CE82FF; /* 보라색 테두리 */
  position: relative;
  z-index: 10;
}

.edit-header { text-align: center; margin-bottom: 30px; }
.back-link { 
  display: inline-block; cursor: pointer; color: #999; 
  font-weight: 800; margin-bottom: 15px; transition: 0.2s;
}
.back-link:hover { color: #CE82FF; transform: translateX(-5px); }

.edit-header h1 { font-size: 2rem; font-weight: 900; color: #3C3C3C; }
.edit-header p { color: #888; font-weight: 600; }

/* 아바타 */
.avatar-section { text-align: center; margin-bottom: 30px; }
.avatar-circle {
  width: 110px; height: 110px; background: #F0F9FF;
  border-radius: 40px; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 15px; position: relative; border: 3px dashed #1CB0F6;
}
.current-emoji { font-size: 3.5rem; }
.edit-badge {
  position: absolute; bottom: -5px; right: -5px;
  background: white; border-radius: 50%; width: 35px; height: 35px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1); font-size: 1.2rem;
}
.email-info { color: #AAA; font-weight: 700; font-size: 0.9rem; }

/* 폼 스타일 */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
.full-width { grid-column: span 2; }

.form-group label {
  display: block; margin-bottom: 8px; font-weight: 800; color: #3C3C3C;
}

.input-wrapper { position: relative; }
.input-icon { position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: #CE82FF; }

input, select {
  width: 100%; padding: 12px 12px 12px 45px;
  border: 3px solid #E5E5E5; border-radius: 20px;
  font-family: 'Nunito', sans-serif; font-weight: 700; outline: none; transition: 0.3s;
}

input:focus, select:focus { border-color: #CE82FF; box-shadow: 0 5px 15px rgba(206,130,255,0.15); }

/* 버튼 그룹 */
.btn-group { display: flex; gap: 15px; }
.btn {
  flex: 1; padding: 15px; border-radius: 20px; border: none;
  font-weight: 900; font-size: 1.1rem; cursor: pointer; transition: 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #FF6B9D, #CE82FF);
  color: white; box-shadow: 0 6px 0 #9B5FCC;
}
.btn-primary:active { transform: translateY(3px); box-shadow: 0 3px 0 #9B5FCC; }

.btn-secondary {
  background: #F0F0F0; color: #888; box-shadow: 0 6px 0 #CCC;
}
.btn-secondary:hover {
  /* 1. 위로 살짝 뜨면서 전체적으로 1.02배 커지는 효과 */
  transform: translateY(-3px) scale(1.02);
  
  /* 2. 호버 시 배경색을 기존(#F0F0F0)보다 약간 더 진한 회색으로 변경하여 피드백 강화 */
  background-color: #E8E8E8;
  
  /* 3. 버튼이 떠오른 만큼 입체 그림자 깊이를 9px로 늘리고, 바닥에 부드러운 그림자 추가 */
  box-shadow: 0 9px 0 #CCC, 0 15px 30px rgba(0, 0, 0, 0.1);
  
  /* 부드러운 전환 효과 */
  transition: all 0.2s ease;
}

@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
  .full-width { grid-column: span 1; }
}

.btn-primary:hover {
  /* 1. 크기 확장과 위로 뜨는 효과를 동시에 적용 */
  transform: translateY(-3px) scale(1.02);
  
  /* 2. 기존(#FF6B9D, #CE82FF)보다 더 진하고 선명한 그라데이션 */
  background: linear-gradient(135deg, #E65586, #B366EB); 
  
  /* 3. 버튼색이 진해짐에 따라 그림자 색상도 더 깊게 조정 */
  box-shadow: 0 9px 0 #8A4EBD, 0 15px 30px rgba(179, 102, 235, 0.4);
  
  /* 4. 텍스트는 흰색을 유지하여 가독성 확보 */
  color: white;
  
  transition: all 0.2s ease;
  cursor: pointer;
}

.error-text {
  color: #ff6b6b;
  font-size: 0.85rem;
  font-weight: 700;
  margin-top: 5px;
  margin-left: 10px;
}
</style>