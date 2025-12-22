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
import TodayStudyView from '@/views/learning/TodayStudyView.vue'
import MyPageView from '@/views/mypage/MyPageView.vue'
import ProfileEditView from '@/components/ProfileEditView.vue'
import IndividualSettingsView from '@/components/IndividualSettingsView.vue'

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
    // 마이페이지 추가
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView
    },
    // 오늘의 학습
    {
      path: '/learning/today',
      name: 'today-learning',
      component: TodayLearningView
    },
    {
      path: '/learning/today/study',
      name: 'today-study',
      component: TodayStudyView
    },
    // 프로필 수정
    {
      path: '/profile/edit/',
      name: 'profile-edit',
      component: ProfileEditView
    },
    // 프로필 학습 설정
    {
      path: '/profile/settings/',
      name: 'profile-learning-settings',
      component: IndividualSettingsView
    },
  ],
})

export default router
