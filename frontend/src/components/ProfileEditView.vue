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
            <span class="current-emoji">✨</span>
            <div class="edit-badge">📸</div>
          </div>
          <p class="email-info">{{ editForm.email }}</p>
        </div>

        <form @submit.prevent="updateProfileHandler">
          <div class="form-grid">
            <div class="form-group">
              <label for="nickname">새로운 닉네임</label>
              <div class="input-wrapper">
                <input type="text" id="nickname" v-model="editForm.nickname" placeholder="닉네임을 입력하세요">
                <i class="fas fa-user input-icon"></i>
              </div>
            </div>

            <div class="form-group">
              <label for="age">아이 나이</label>
              <div class="input-wrapper">
                <select id="age" v-model="editForm.age">
                  <option v-for="n in 8" :key="n" :value="n + 2">{{ n + 2 }}세</option>
                </select>
                <i class="fas fa-birthday-cake input-icon"></i>
              </div>
            </div>

            <div class="form-group full-width">
              <label for="level">현재 학습 레벨</label>
              <div class="input-wrapper">
                <select id="level" v-model="editForm.level">
                  <option v-for="l in 10" :key="l" :value="l">Lv.{{ l }}</option>
                </select>
                <i class="fas fa-layer-group input-icon"></i>
              </div>
            </div>
          </div>

          <div class="btn-group">
            <button type="button" class="btn btn-secondary" @click="router.back()">취소</button>
            <button type="submit" class="btn btn-primary">변경사항 저장 💾</button>
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
  age: 0,
  level: 0
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
// const updateProfileHandler = async () => {
//   if (!editForm.nickname) return alert("닉네임을 입력해주세요!")
  
//   try {
//     // [수정] 여기도 마찬가지로 헤더 없이 깔끔하게 호출합니다.
//     await axios.patch('/api/accounts/profile/update/', {
//       nickname: editForm.nickname,
//       age: editForm.age,
//       level: editForm.level
//     })
    
//     store.nickname = editForm.nickname
//     alert("정보가 성공적으로 수정되었습니다! ✨")
//     router.push({ name: 'mypage' })
//   } catch (err) {
//     console.error("수정 실패:", err)
//     alert("정보 수정에 실패했습니다.")
//   }
// }
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
.btn-secondary:active { transform: translateY(3px); box-shadow: 0 3px 0 #CCC; }

@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
  .full-width { grid-column: span 1; }
}
</style>