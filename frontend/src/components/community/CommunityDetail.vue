<template>
    <div class="detail-container" v-if="post">
        <button class="back-btn" @click="goBack">
            <i class="fas fa-arrow-left"></i> 목록으로
        </button>

        <!-- 게시글 본문 -->
        <article class="post-card">
            <div class="post-header">
                <div class="header-top">
                    <span class="genre-badge">자유</span>
                    <div class="post-meta">
                        <span class="date">{{ formatDate(post.created_at) }}</span>
                    </div>
                </div>

                <div v-if="isEditingPost" class="edit-title-wrapper">
                    <input 
                        v-model="editingTitle" 
                        class="edit-title-input" 
                        placeholder="제목을 입력하세요"
                    />
                </div>
                <h1 v-else class="post-title">{{ post.title }}</h1>

                <div class="author-info">
                    <div class="avatar">U</div>
                    <span class="nickname">{{ post.user_nickname }}</span>
                </div>
            </div>

            <div v-if="isEditingPost" class="edit-content-wrapper">
                <textarea 
                    v-model="editingPostContent" 
                    class="edit-post-textarea"
                    placeholder="내용을 입력하세요"
                ></textarea>
            </div>
            <div v-else class="post-content">
                {{ post.content }}
            </div>

            <div class="post-actions">
                <button 
                    v-if="store.email !== post.user_email"
                    class="action-btn like-btn" 
                    :class="{ active: liked }" 
                    @click="toggleLike"
                >
                    <i class="fas fa-heart"></i>
                    <span>좋아요 {{ likeCount }}</span>
                </button>

                <div v-else class="owner-actions">
                    <template v-if="isEditingPost">
                        <button class="action-btn save-btn" @click="updatePost">
                            <i class="fas fa-check"></i> 저장하기
                        </button>
                        <button class="action-btn cancel-btn" @click="cancelEditPost">
                            <i class="fas fa-times"></i> 취소
                        </button>
                    </template>
                    <template v-else>
                        <button class="action-btn edit-btn" @click="startEditPost">
                            <i class="fas fa-pen"></i> 수정하기
                        </button>
                        <button class="action-btn delete-btn" @click="deletePost">
                            <i class="fas fa-trash"></i> 삭제하기
                        </button>
                    </template>
                </div>
            </div>
        </article>

        <!-- 댓글 섹션 -->
        <section class="comments-section">
            <h3>댓글 {{ comments.length }}개</h3>
            
            <!-- 댓글 작성 -->
            <div class="comment-form">
                <textarea 
                    v-model="newComment" 
                    placeholder="따뜻한 댓글을 남겨주세요!"
                    @keydown.enter.prevent="submitComment"
                ></textarea>
                <button @click="submitComment" :disabled="!newComment.trim()">등록</button>
            </div>

            <!-- 댓글 목록 -->
            <div class="comment-list">
                <div v-for="comment in comments" :key="comment.id" class="comment-item">
                    <div class="comment-avatar">U</div>
                    <div class="comment-body">
                        <div class="comment-meta">
                            <!-- 작성자 닉네임 표시 (현재는 store.nickname이 아니라 comment.user를 보여줘야 함, 
                                 하지만 백엔드에서 닉네임을 안주므로 일단 User ID로 표시하거나 
                                 본인인 경우 '나'라고 표시) -->
                            <span class="nickname">
                                {{  comment.user_nickname }}
                            </span>
                            <span class="date">{{ formatDate(comment.created_at) }}</span>
                        </div>
                        
                        <!-- 수정 모드 -->
                        <div v-if="editingCommentId === comment.id" class="edit-mode">
                            <textarea v-model="editingContent" class="edit-textarea"></textarea>
                            <div class="edit-actions">
                                <button class="save-btn" @click="updateComment(comment.id)">저장</button>
                                <button class="cancel-btn-mini" @click="cancelEdit">취소</button>
                            </div>
                        </div>

                        <!-- 일반 모드 -->
                        <div v-else>
                            <p class="comment-text">{{ comment.content }}</p>
                            <div class="comment-options" v-if="comment.user_email === store.email && editingCommentId !== comment.id">
                            <button class="opt-btn edit" @click="startEdit(comment)" title="수정">
                                <i class="fas fa-pen"></i> 수정
                            </button>
                            <button class="opt-btn delete" @click="deleteComment(comment.id)" title="삭제">
                                <i class="fas fa-trash"></i> 삭제
                            </button>
                            </div>
                        </div>
                       
                    </div>
                </div>
            </div>
        </section>
    </div>
    <div v-else class="loading">
        <i class="fas fa-spinner fa-spin"></i> 로딩중...
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/api/index.js'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()

const post = ref(null)
const comments = ref([])
const newComment = ref('')
const liked = ref(false)
const likeCount = ref(0)

// 게시글 수정
const isEditingPost = ref(false)
const editingTitle = ref('')
const editingPostContent = ref('')

const startEditPost = () => {
    isEditingPost.value = true
    editingTitle.value = post.value.title
    editingPostContent.value = post.value.content
}

const cancelEditPost = () => {
    isEditingPost.value = false
    editingTitle.value = ''
    editingPostContent.value = ''
}

const updatePost = async () => {
    if (!editingTitle.value.trim() || !editingPostContent.value.trim()) {
        alert('제목과 내용을 모두 입력해주세요.')
        return
    }

    try {
        const res = await axios.put(`/api/community/posts/${postId}/`, {
            title: editingTitle.value,
            content: editingPostContent.value
        })
        
        // 데이터 갱신 및 모드 전환
        post.value.title = res.data.title
        post.value.content = res.data.content
        isEditingPost.value = false
        
        alert('게시글이 성공적으로 수정되었습니다! ✨')
    } catch (error) {
        console.error('게시글 수정 실패:', error)
        alert('수정 중 오류가 발생했습니다.')
    }
}


// 댓글 수정 상태
const editingCommentId = ref(null) 
const editingContent = ref('')

const postId = route.params.id

const goBack = () => {
    router.push('/community')
}

const fetchPost = async () => {
    try {
        const res = await axios.get(`/api/community/posts/${postId}/`)
        post.value = res.data
        likeCount.value = res.data.like_count || 0
        liked.value = res.data.is_liked || false
    } catch (error) {
        console.error('게시글 로드 실패:', error)
    }
}

const fetchComments = async () => {
    try {
        const res = await axios.get(`/api/community/posts/${postId}/comments/`)
        comments.value = res.data
        console.log(comments.value)
    } catch (error) {
        console.error('댓글 로드 실패:', error)
    }
}

const submitComment = async () => {
    if (!newComment.value.trim()) return

    try {
        await axios.post(`/api/community/posts/${postId}/comments/`, {
            content: newComment.value
        })
        newComment.value = ''
        fetchComments() // 댓글 목록 갱신
    } catch (error) {
        console.error('댓글 작성 실패:', error)
        alert('댓글 등록에 실패했어요.')
    }
}


// 게시글 삭제
const deletePost = async () => {
    if (!confirm('정말 이 게시글을 삭제하시겠습니까?\n삭제된 글은 복구할 수 없어요! 😢')) return

    try {
        // 백엔드 URL 규격에 맞춰 DELETE 요청 (이미 작성하신 post_detail 뷰가 처리)
        await axios.delete(`/api/community/posts/${postId}/`)
        alert('게시글이 삭제되었습니다.')
        router.push('/community') // 삭제 후 목록으로 이동
    } catch (error) {
        console.error('게시글 삭제 실패:', error)
        if (error.response?.status === 403) {
            alert('삭제 권한이 없습니다.')
        } else {
            alert('삭제 중 오류가 발생했습니다.')
        }
    }
}

// 댓글 수정 시작
const startEdit = (comment) => {
    editingCommentId.value = comment.id
    editingContent.value = comment.content
}

// 댓글 수정 취소
const cancelEdit = () => {
    editingCommentId.value = null
    editingContent.value = ''
}

// 댓글 수정 저장
const updateComment = async (commentId) => {
    if (!editingContent.value.trim()) return

    try {
        await axios.put(`/api/community/comments/${commentId}/`, {
            content: editingContent.value
        })
        editingCommentId.value = null
        fetchComments()
    } catch (error) {
        console.error('댓글 수정 실패:', error)
        alert('댓글 수정에 실패했어요.')
    }
}

// 댓글 삭제
const deleteComment = async (commentId) => {
    if(!confirm('정말 삭제하시겠습니까?')) return

    try {
        await axios.delete(`/api/community/comments/${commentId}/`)
        fetchComments()
    } catch (error) {
        console.error('댓글 삭제 실패:', error)
        alert('댓글 삭제에 실패했어요.')
    }
}

const toggleLike = async () => {
    try {
        const res = await axios.post(`/api/community/posts/${postId}/like/`)
        liked.value = res.data.liked
        likeCount.value = res.data.like_count
    } catch (error) {
        console.error('좋아요 실패:', error)
    }
}

const formatDate = (dateStr) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
    fetchPost()
    fetchComments()
})
</script>

<style scoped>
.detail-container {
    max-width: 800px;
    margin: 40px auto;
    padding: 0 20px;
}

.post-card {
    background: white;
    border-radius: 25px;
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}

.post-header {
    border-bottom: 2px solid #F7F7F7;
    padding-bottom: 20px;
    margin-bottom: 30px;
}

.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.genre-badge {
    background: #E5F6FF;
    color: #1CB0F6;
    padding: 5px 12px;
    border-radius: 15px;
    font-weight: 800;
    font-size: 0.9rem;
}

.date {
    color: #999;
    font-size: 0.9rem;
}

.post-title {
    font-size: 2rem;
    color: #3C3C3C;
    margin-bottom: 20px;
    line-height: 1.3;
}

.author-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.avatar {
    width: 35px;
    height: 35px;
    background: #E5E5E5;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: #777;
}

.nickname {
    font-weight: 700;
    color: #555;
}

.post-content {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #333;
    margin-bottom: 40px;
    white-space: pre-wrap;
}

.post-actions {
    display: flex;
    justify-content: center;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 20px;
    border: 2px solid #E5E5E5;
    background: white;
    color: #777;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
}

.action-btn:hover {
    background: #F7F7F7;
}

.like-btn.active {
    border-color: #FF6B9D;
    color: #FF6B9D;
    background: #FFF0F5;
}

.like-btn i {
    font-size: 1.2rem;
}

/* 댓글 섹션 */
.comments-section {
    background: white;
    border-radius: 25px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.comments-section h3 {
    margin-bottom: 20px;
    color: #3C3C3C;
}

.comment-form {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
}

.comment-form textarea {
    flex: 1;
    padding: 15px;
    border: 2px solid #E5E5E5;
    border-radius: 15px;
    resize: none;
    height: 60px;
    font-family: 'Nunito', sans-serif;
    outline: none;
    transition: border-color 0.2s;
}

.comment-form textarea:focus {
    border-color: #1CB0F6;
}

.comment-form button {
    padding: 0 25px;
    border-radius: 15px;
    background: #1CB0F6;
    color: white;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
}

.comment-form button:hover {
    background: #1899D6;
}

.comment-form button:disabled {
    background: #DDD;
    cursor: not-allowed;
}

.comment-item {
    display: flex;
    gap: 15px;
    padding: 20px 0;
    border-bottom: 1px solid #F0F0F0;
}

.comment-item:last-child {
    border-bottom: none;
}

.comment-avatar {
    width: 40px;
    height: 40px;
    background: #F0F9FF;
    color: #1CB0F6;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    flex-shrink: 0;
}

.comment-body {
    flex: 1;
}

.comment-meta {
    margin-bottom: 5px;
}

.comment-meta .nickname {
    margin-right: 10px;
}

.comment-meta .date {
    font-size: 0.8rem;
}

.comment-text {
    color: #444;
    line-height: 1.5;
    word-break: break-all;      /* 아주 긴 단어도 강제로 줄바꿈합니다 */
    overflow-wrap: break-word; /* 단어가 넘칠 경우 줄바꿈을 허용합니다 */
    white-space: pre-wrap;
}

.loading {
    text-align: center;
    padding: 50px;
    font-size: 1.2rem;
    color: #888;
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

.comment-options {
    display: flex;
    gap: 5px;
    align-items: center;
}

.opt-btn {
    background: none;
    border: none;
    color: #AAA;
    cursor: pointer;
    padding: 5px;
    transition: color 0.2s;
}

.opt-btn:hover {
    color: #555;
}

.opt-btn.delete:hover {
    color: #FF6B6B;
}

.edit-mode {
    width: 100%;
}

.edit-textarea {
    width: 100%;
    padding: 10px;
    border: 2px solid #58CC02;
    border-radius: 10px;
    margin-bottom: 10px;
    font-family: 'Nunito', sans-serif;
    resize: vertical;
}

.edit-actions {
    display: flex;
    gap: 10px;
}

.save-btn {
    background: #58CC02;
    color: white;
    border: none;
    padding: 5px 15px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 700;
}

.cancel-btn-mini {
    background: #F0F0F0;
    color: #888;
    border: none;
    padding: 5px 15px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 700;
}

/* 기존 post-actions 하단에 추가 */
.owner-actions {
    display: flex;
    gap: 12px;
}

/* 수정 버튼 스타일 */
.edit-btn:hover {
    border-color: var(--secondary);
    color: var(--secondary);
    background: #F0F9FF;
}

/* 삭제 버튼 스타일 */
.delete-btn:hover {
    border-color: #FF6B6B;
    color: #FF6B6B;
    background: #FFF5F5;
}

/* 버튼 아이콘 간격 */
.action-btn i {
    font-size: 1rem;
}

/* 반응형: 화면이 작을 때 버튼 배치 */
@media (max-width: 480px) {
    .owner-actions {
        width: 100%;
        flex-direction: column;
    }
    .action-btn {
        width: 100%;
        justify-content: center;
    }
}

/* 제목 수정 입력창 */
.edit-title-input {
    width: 100%;
    font-size: 2rem;
    font-weight: 800;
    color: #3C3C3C;
    border: 3px solid #E5E5E5;
    border-radius: 15px;
    padding: 10px 15px;
    margin-bottom: 20px;
    font-family: 'Nunito', 'Jua', sans-serif;
    outline: none;
}
.edit-title-input:focus {
    border-color: var(--secondary);
}

/* 본문 수정 텍스트 영역 */
.edit-post-textarea {
    width: 100%;
    min-height: 250px;
    font-size: 1.1rem;
    line-height: 1.8;
    color: #333;
    border: 3px solid #E5E5E5;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 30px;
    font-family: inherit;
    resize: vertical;
    outline: none;
}
.edit-post-textarea:focus {
    border-color: var(--secondary);
}

/* 수정 중 버튼들 */
.save-btn {
    background: #58CC02 !important;
    color: white !important;
    border-color: #58CC02 !important;
}
.save-btn:hover {
    background: #46A302 !important;
}

.cancel-btn {
    background: #F7F7F7 !important;
    color: #888 !important;
}
</style>
