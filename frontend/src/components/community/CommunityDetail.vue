<template>
    <div class="detail-container" v-if="post">
        <button class="back-btn" @click="goBack">
            <i class="fas fa-arrow-left"></i> 목록으로
        </button>

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

        <section class="comments-section">
            <h3>댓글 {{ comments.length }}개</h3>
            
            <div class="comment-form">
                <textarea 
                    v-model="newComment" 
                    placeholder="따뜻한 댓글을 남겨주세요!"
                    @keydown.enter.prevent="submitComment"
                ></textarea>
                <button @click="submitComment" :disabled="!newComment.trim()">등록</button>
            </div>

            <div class="comment-list">
                <div v-for="comment in comments" :key="comment.id" class="comment-item">
                    <div class="comment-avatar">U</div>
                    <div class="comment-body">
                        <div class="comment-meta">
                            <div class="meta-left">
                                <span class="nickname">{{ comment.user_nickname }}</span>
                                <span class="date">{{ formatDate(comment.created_at) }}</span>
                            </div>

                            <button 
                                class="comment-like-btn" 
                                :class="{ active: comment.is_liked, 'readonly': comment.user_email === store.email }" 
                                @click="comment.user_email !== store.email && toggleCommentLike(comment)"
                            >
                                <i class="fas fa-heart"></i>
                                <span>{{ comment.like_count || 0 }}</span>
                            </button>
                        </div>
                        
                        <div v-if="editingCommentId === comment.id" class="edit-mode">
                            <textarea v-model="editingContent" class="edit-textarea"></textarea>
                            <div class="edit-actions">
                                <button class="save-btn-mini" @click="updateComment(comment.id)">저장</button>
                                <button class="cancel-btn-mini" @click="cancelEdit">취소</button>
                            </div>
                        </div>

                        <div v-else>
                            <p class="comment-text">{{ comment.content }}</p>
                            <div class="comment-footer" v-if="comment.user_email === store.email">
                                <div class="comment-options">
                                    <button class="opt-btn edit" @click="startEdit(comment)">
                                        <i class="fas fa-pen"></i> 수정
                                    </button>
                                    <button class="opt-btn delete" @click="deleteComment(comment.id)">
                                        <i class="fas fa-trash"></i> 삭제
                                    </button>
                                </div>
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
const postId = route.params.id

// 게시글 수정 상태
const isEditingPost = ref(false)
const editingTitle = ref('')
const editingPostContent = ref('')

// 댓글 수정 상태
const editingCommentId = ref(null) 
const editingContent = ref('')

const goBack = () => router.push('/community')

const fetchPost = async () => {
    try {
        const res = await axios.get(`/api/community/posts/${postId}/`)
        post.value = res.data
        likeCount.value = res.data.like_count || 0
        liked.value = res.data.is_liked || false
    } catch (error) { console.error('게시글 로드 실패:', error) }
}

const fetchComments = async () => {
    try {
        const res = await axios.get(`/api/community/posts/${postId}/comments/`)
        comments.value = res.data
    } catch (error) { console.error('댓글 로드 실패:', error) }
}

const submitComment = async () => {
    if (!newComment.value.trim()) return
    try {
        await axios.post(`/api/community/posts/${postId}/comments/`, { content: newComment.value })
        newComment.value = ''
        fetchComments()
    } catch (error) { alert('댓글 등록에 실패했어요.') }
}

const startEditPost = () => {
    isEditingPost.value = true
    editingTitle.value = post.value.title
    editingPostContent.value = post.value.content
}

const cancelEditPost = () => { isEditingPost.value = false }

const updatePost = async () => {
    try {
        const res = await axios.put(`/api/community/posts/${postId}/`, {
            title: editingTitle.value,
            content: editingPostContent.value
        })
        post.value.title = res.data.title
        post.value.content = res.data.content
        isEditingPost.value = false
    } catch (error) { alert('수정 중 오류가 발생했습니다.') }
}

const deletePost = async () => {
    if (!confirm('정말 삭제하시겠습니까?')) return
    try {
        await axios.delete(`/api/community/posts/${postId}/`)
        router.push('/community')
    } catch (error) { alert('삭제 중 오류가 발생했습니다.') }
}

const startEdit = (comment) => {
    editingCommentId.value = comment.id
    editingContent.value = comment.content
}

const cancelEdit = () => { editingCommentId.value = null }

const updateComment = async (commentId) => {
    if (!editingContent.value.trim()) return
    try {
        await axios.put(`/api/community/comments/${commentId}/`, { content: editingContent.value })
        editingCommentId.value = null
        fetchComments()
    } catch (error) { alert('댓글 수정에 실패했어요.') }
}

const deleteComment = async (commentId) => {
    if(!confirm('정말 삭제하시겠습니까?')) return
    try {
        await axios.delete(`/api/community/comments/${commentId}/`)
        fetchComments()
    } catch (error) { alert('댓글 삭제에 실패했어요.') }
}

const toggleLike = async () => {
    try {
        const res = await axios.post(`/api/community/posts/${postId}/like/`)
        liked.value = res.data.liked
        likeCount.value = res.data.like_count
    } catch (error) { console.error('좋아요 실패:', error) }
}

const toggleCommentLike = async (comment) => {
    try {
        const res = await axios.post(`/api/community/comments/${comment.id}/like/`)
        comment.is_liked = res.data.liked
        comment.like_count = res.data.like_count
    } catch (error) { console.error('댓글 좋아요 실패:', error) }
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
.detail-container { max-width: 800px; margin: 40px auto; padding: 0 20px; }
.post-card { background: white; border-radius: 25px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 30px; }
.post-header { border-bottom: 2px solid #F7F7F7; padding-bottom: 20px; margin-bottom: 30px; }
.header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.genre-badge { background: #E5F6FF; color: #1CB0F6; padding: 5px 12px; border-radius: 15px; font-weight: 800; font-size: 0.9rem; }
.date { color: #999; font-size: 0.9rem; }
.post-title { font-size: 2rem; color: #3C3C3C; margin-bottom: 20px; line-height: 1.3; font-weight: 800; }
.author-info { display: flex; align-items: center; gap: 10px; }
.avatar { width: 35px; height: 35px; background: #E5E5E5; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #777; }
.nickname { font-weight: 700; color: #555; }
.post-content { font-size: 1.1rem; line-height: 1.8; color: #333; margin-bottom: 40px; white-space: pre-wrap; }
.post-actions { display: flex; justify-content: center; }
.action-btn { display: flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 20px; border: 2px solid #E5E5E5; background: white; color: #777; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.like-btn.active { border-color: #FF6B9D; color: #FF6B9D; background: #FFF0F5; }

/* 댓글 섹션 */
.comments-section { background: white; border-radius: 25px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
.comment-form { display: flex; gap: 10px; margin-bottom: 30px; }
.comment-form textarea { flex: 1; padding: 15px; border: 2px solid #E5E5E5; border-radius: 15px; resize: none; height: 60px; outline: none; transition: border-color 0.2s; }
.comment-form textarea:focus { border-color: #1CB0F6; }
.comment-form button { padding: 0 25px; border-radius: 15px; background: #1CB0F6; color: white; font-weight: 700; border: none; cursor: pointer; }
.comment-item { display: flex; gap: 15px; padding: 20px 0; border-bottom: 1px solid #F0F0F0; }
.comment-avatar { width: 40px; height: 40px; background: #F0F9FF; color: #1CB0F6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }
.comment-body { flex: 1; }
.comment-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.meta-left { display: flex; align-items: center; gap: 10px; }
.comment-text { color: #444; line-height: 1.5; white-space: pre-wrap; margin-bottom: 10px; }

/* 좋아요 버튼 */
.comment-like-btn { display: flex; align-items: center; gap: 4px; background: none; border: none; cursor: pointer; color: #AAA; font-size: 0.85rem; font-weight: 700; transition: all 0.2s; }
.comment-like-btn:hover:not(.readonly) { color: #FF6B9D; }
.comment-like-btn.active { color: #FF6B9D; }
.comment-like-btn.readonly { cursor: default; opacity: 0.7; }

/* 수정/삭제 옵션 */
.comment-footer { display: flex; }
.comment-options { display: flex; gap: 5px; }
.opt-btn { background: none; border: none; color: #AAA; cursor: pointer; font-size: 0.8rem; }
.opt-btn:hover { color: #555; }

/* 수정 모드 */
.edit-textarea { width: 100%; padding: 10px; border: 2px solid #58CC02; border-radius: 10px; margin-bottom: 10px; resize: vertical; }
.edit-actions { display: flex; gap: 10px; }
.save-btn-mini { background: #58CC02; color: white; border: none; padding: 5px 15px; border-radius: 10px; cursor: pointer; font-weight: 700; }
.cancel-btn-mini { background: #F0F0F0; color: #888; border: none; padding: 5px 15px; border-radius: 10px; cursor: pointer; font-weight: 700; }

.owner-actions { display: flex; gap: 12px; }
.edit-title-input { width: 100%; font-size: 2rem; font-weight: 800; border: 3px solid #E5E5E5; border-radius: 15px; padding: 10px 15px; margin-bottom: 20px; outline: none; }
.edit-post-textarea { width: 100%; min-height: 250px; font-size: 1.1rem; line-height: 1.8; border: 3px solid #E5E5E5; border-radius: 15px; padding: 20px; margin-bottom: 30px; resize: vertical; outline: none; }
.save-btn { background: #58CC02; color: white; border-radius: 20px; padding: 10px 20px; border: none; font-weight: 700; cursor: pointer; }
.back-btn { background: white; border: 2px solid #E5E5E5; padding: 10px 20px; border-radius: 20px; font-weight: 700; color: #888; cursor: pointer; margin-bottom: 20px; display: flex; align-items: center; gap: 8px; }
</style>