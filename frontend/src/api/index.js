import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

axios.interceptors.request.use((config) => {
    const store = useCounterStore();
    if (store.token) {
        // 모든 요청 헤더에 Bearer 토큰 자동 삽입
        config.headers.Authorization = `Bearer ${store.token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
})