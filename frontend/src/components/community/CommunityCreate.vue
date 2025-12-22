<template>
    <div class="create-container">
        <button class="back-btn" @click="goBack">
            <i class="fas fa-arrow-left"></i> 뒤로 가기
        </button>
        <div class="form-card">
            <h1 class="page-title">새로운 이야기 작성 ✍️</h1>
            
            <div class="form-group">
                <label>제목</label>
                <input 
                    v-model="title" 
                    type="text" 
                    placeholder="재미있는 제목을 지어주세요!"
                    class="input-field"
                >
            </div>

            <div class="form-group">
                <label>내용</label>
                <textarea 
                    v-model="content" 
                    placeholder="어떤 이야기를 나누고 싶나요?"
                    class="textarea-field"
                    rows="10"
                ></textarea>
            </div>

            <div class="button-group">
                <button class="cancel-btn" @click="goBack">취소</button>
                <button class="submit-btn" @click="submitPost" :disabled="!isValid">등록하기</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/api/index.js'

const router = useRouter()
const title = ref('')
const content = ref('')

const isValid = computed(() => {
    return title.value.trim().length > 0 && content.value.trim().length > 0
})

const goBack = () => {
    router.back()
}

const submitPost = async () => {
    if (!isValid.value) return

    try {
        await axios.post('/api/community/posts/', {
            title: title.value,
            content: content.value
        })
        alert('이야기가 등록되었습니다! 🎉')
        router.push('/community')
    } catch (error) {
        console.error('게시글 작성 실패:', error)
        alert('등록에 실패했어요 😢')
    }
}
</script>

<style scoped>
.create-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 20px;
}

.form-card {
    background: white;
    padding: 40px;
    border-radius: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.page-title {
    font-size: 2rem;
    color: #3C3C3C;
    margin-bottom: 30px;
    text-align: center;
    font-family: 'Jua', sans-serif;
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    font-size: 1.1rem;
    font-weight: 700;
    color: #555;
    margin-bottom: 10px;
}

.input-field, .textarea-field {
    width: 100%;
    padding: 15px;
    border: 2px solid #E5E5E5;
    border-radius: 15px;
    font-size: 1rem;
    font-family: 'Nunito', sans-serif;
    transition: all 0.3s;
    outline: none;
}

.input-field:focus, .textarea-field:focus {
    border-color: #58CC02;
    box-shadow: 0 0 0 4px rgba(88, 204, 2, 0.1);
}

.textarea-field {
    resize: vertical;
    min-height: 200px;
}

.button-group {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 40px;
}

.cancel-btn, .submit-btn {
    padding: 12px 30px;
    border-radius: 15px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-family: 'Jua', sans-serif;
}

.cancel-btn {
    background: #F7F7F7;
    color: #888;
}

.cancel-btn:hover {
    background: #E5E5E5;
}

.submit-btn {
    background: #58CC02;
    color: white;
    box-shadow: 0 4px 0 #46A302;
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 0 #46A302;
}

.submit-btn:active {
    transform: translateY(0);
    box-shadow: 0 0 0 #46A302;
}

.submit-btn:disabled {
    background: #CCC;
    box-shadow: none;
    cursor: not-allowed;
    transform: none;
}

.back-btn {
    background: white;
    border: 2px solid #E5E5E5;
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: 700;
    color: #888;
    cursor: pointer;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
    font-family: 'Nunito', sans-serif;
}

.back-btn:hover {
    background: #F7F7F7;
    color: #555;
    transform: translateX(-5px);
}
</style>
