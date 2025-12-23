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
import TodayWordView from '@/views/learning/TodayWordView.vue'
import MyPageView from '@/views/mypage/MyPageView.vue'
import ProfileEditView from '@/components/profile/ProfileEditView.vue'
import IndividualSettingsView from '@/components/profile/IndividualSettingsView.vue'
import UserTotalStory from '@/views/mypage/UserTotalStory.vue'
import TodayGrammarView from '@/views/learning/TodayGrammarView.vue'
import TodayPronunciationView from '@/views/learning/TodayPronunciationView.vue'
import OnboardingView from '@/views/learning/OnboardingView.vue'

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
      path: '/community/create',
      name: 'community-create',
      component: () => import('@/components/community/CommunityCreate.vue')
    },
    {
      path: '/community/:id',
      name: 'community-detail',
      component: () => import('@/components/community/CommunityDetail.vue')
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
      path: '/learning/today/word',
      name: 'today-word',
      component: TodayWordView
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
    // 전체 동화 보기
    {
      path: '/mypage/stories',
      name: 'user-total-stories',
      component: UserTotalStory
    },
    {
      path: '/learning/today/grammar',
      name: 'today-grammar',
      component: TodayGrammarView
    },
    {
      path: '/learning/today/pronunciation',
      name: 'today-pronunciation',
      component: TodayPronunciationView
    },
    {
    path: '/onboarding',
    name: 'onboarding',
    component: OnboardingView,
    meta: { requiresAuth: true } // 로그인 필요
},
  ],
})

export default router
