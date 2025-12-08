import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StoryCreateView from '../views/story/StoryCreateView.vue'
import StoryLoadingView from '../views/story/StoryLoadingView.vue'
import StoryQuizView from '../views/story/StoryQuizView.vue'
import StoryReadView from '../views/story/StoryReadView.vue'

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
    }
  ],
})

export default router
