import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StoryCreateView from '../views/Story/StoryCreateView.vue'
import StoryLoadingView from '../views/Story/StoryLoadingView.vue'
import StoryQuizView from '../views/Story/StoryQuizView.vue'
import StoryReadView from '../views/Story/StoryReadView.vue'
import LoginView from '@/views/Login/LoginView.vue'

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
      path: '/story/quiz/:id',
      name: 'story-quiz',
      component: StoryQuizView
    },
    
    // 로그인 페이지 추가
    {
      path: '/login',
      name: 'login',
      component: LoginView
    }
  ],
})

export default router
