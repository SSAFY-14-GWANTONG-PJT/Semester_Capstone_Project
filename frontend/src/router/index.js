import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StoryCreateView from '../views/story/StoryCreateView.vue'
import StoryLoadingView from '../views/story/StoryLoadingView.vue'
import StoryQuizView from '../views/story/StoryQuizView.vue'
import StoryReadView from '../views/story/StoryReadView.vue'
import LoginView from '@/views/login/LoginView.vue'
import SignUpView from '@/views/signup/SignUpView.vue'
import CommunityRoot from '@/views/community/CommunityRoot.vue'
import TodayLearningView from '@/views/learning/TodayLearningView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/story/create',
      name: 'story-create',
      component: StoryCreateView
    },
    {
      path: '/story/loading',
      name: 'story-loading',
      component: StoryLoadingView
    },
    {
      path: '/story/read/:id', // id를 받아서 조회
      name: 'story-read',
      component: StoryReadView
    },
    {
      path: '/story/:id/quiz',
      name: 'StoryQuiz',
      component: StoryQuizView
    },
    
    // 로그인 페이지 추가
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    // 회원가입 페이지 추가
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    // 커뮤니티 페이지 추가
    {
      path: '/community',
      name: 'community',
      component: CommunityRoot
    },
    {
      path: '/learning/today',
      name: 'today-learning',
      component: TodayLearningView
    },
  ],
})

export default router
