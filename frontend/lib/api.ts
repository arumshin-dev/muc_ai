/**
 * API 클라이언트 (에러 처리 포함)
 * 루트 .env의 NEXT_PUBLIC_API_BASE_URL을 자동으로 사용
 */

export class ApiError extends Error {
    constructor(
      message: string,
      public statusCode: number,
      public detail?: string
    ) {
      super(message)
      this.name = 'ApiError'
    }
}

class ApiClient {
    private baseUrl: string
    
    constructor() {
      // .env의 NEXT_PUBLIC_API_BASE_URL을 자동으로 읽음
      this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
      
      // 개발 모드에서만 로그
      if (process.env.NODE_ENV === 'development') {
        console.log('🔗 API Base URL:', this.baseUrl)
      }
    }
    
    /**
     * POST 요청
     */
    async post<T>(endpoint: string, data: any): Promise<T> {
      const url = `${this.baseUrl}${endpoint}`
      
      if (process.env.NODE_ENV === 'development') {
        console.log('📤 POST:', url, data)
      }
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      })
      
      if (!response.ok) {
      const errorData = await response.json().catch(() => ({ 
        detail: '알 수 없는 오류' 
      }))
      
      // 상태 코드와 함께 에러 던지기
      throw new ApiError(
        errorData.detail || '요청 실패',
        response.status,
        errorData.detail
      )
      }
      
      const result = await response.json()
      
      if (process.env.NODE_ENV === 'development') {
        console.log('✅ Response:', result)
      }
      
      return result
    }
    
    /**
     * GET 요청
     */
    async get<T>(endpoint: string): Promise<T> {
      const url = `${this.baseUrl}${endpoint}`
      
      if (process.env.NODE_ENV === 'development') {
        console.log('📥 GET:', url)
      }
      
      const response = await fetch(url)
      
      if (!response.ok) {
      const errorData = await response.json().catch(() => ({ 
        detail: '요청 실패' 
      }))
      
      throw new ApiError(
        errorData.detail || '요청 실패',
        response.status,
        errorData.detail
      )
      }
      
      const result = await response.json()
      
      if (process.env.NODE_ENV === 'development') {
        console.log('✅ Response:', result)
      }
      
      return result
    }
  }
  
  // 싱글톤 인스턴스 export
  export const apiClient = new ApiClient()
  