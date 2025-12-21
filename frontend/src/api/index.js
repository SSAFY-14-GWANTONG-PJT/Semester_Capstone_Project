import axios from 'axios'
import { useCounterStore } from '@/stores/counter'
import router from '@/router'

// 1. 독립된 axios 인스턴스 생성
const instance = axios.create({
  baseURL: 'http://localhost:8000'
})

// 2. [요청 인터셉터] 모든 요청 직전에 실행
instance.interceptors.request.use(
  (config) => {
    const store = useCounterStore()
    // 스토어에 토큰이 있다면 헤더에 담아서 보냅니다.
    if (store.token) {
      config.headers.Authorization = `Bearer ${store.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 3. [응답 인터셉터] 서버 응답을 받았을 때 실행
instance.interceptors.response.use(
  (response) => {
    // 200번대 응답은 그냥 통과
    return response
  },
  async (error) => {
    const { config, response: { status } } = error
    const store = useCounterStore()

    // 401 Unauthorized(토큰 만료) 에러가 발생했을 때
    if (status === 401 && !config._retry) {
      config._retry = true // 무한 재시도 방지를 위한 플래그

      try {
        // [중요] 토큰 갱신은 인터셉터가 없는 기본 axios를 사용합니다.
        const res = await axios.post('http://localhost:8000/api/accounts/token/refresh/', {
          refresh: store.refreshToken
        })

        // 새로운 토큰들을 받아옴
        const newAccessToken = res.data.access
        const newRefreshToken = res.data.refresh // Rotate 설정 시 전달됨

        // Pinia 스토어 업데이트
        store.token = newAccessToken
        if (newRefreshToken) store.refreshToken = newRefreshToken

        // 원래 실패했던 요청의 헤더를 새 토큰으로 교체
        config.headers.Authorization = `Bearer ${newAccessToken}`
        
        // 다시 요청 보내기 (재시도)
        return instance(config)
      } catch (refreshError) {
        // 리프레시 토큰마저 만료된 경우 (진짜 로그아웃)
        console.error("세션이 만료되었습니다. 다시 로그인해주세요.")
        store.logout()
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default instance