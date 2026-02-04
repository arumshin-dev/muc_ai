/**
 * API 클라이언트 (에러 처리 포함)
 * 루트 .env의 NEXT_PUBLIC_API_BASE_URL을 자동으로 사용
 */

// process 타입 에러 방지용 (Next.js 환경에서는 브라우저에서도 사용 가능)
declare const process: any;

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
    this.baseUrl = (typeof process !== 'undefined' && process.env.NEXT_PUBLIC_API_BASE_URL) || 'http://localhost:8000'

    if (typeof process !== 'undefined' && process.env.NODE_ENV === 'development') {
      console.log('🔗 API Base URL:', this.baseUrl)
    }
  }

  /**
   * POST 요청
   */
  async post<T>(endpoint: string, data: any, options: { responseType?: 'json' | 'blob' | 'text' } = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    if (typeof process !== 'undefined' && process.env.NODE_ENV === 'development') {
      console.log('🚀 [V2] POST:', url, data, 'Options:', options)
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

      throw new ApiError(
        errorData.detail || '요청 실패',
        response.status,
        errorData.detail
      )
    }

    let result: any
    if (options.responseType === 'blob') {
      console.log('📦 Processing response as blob')
      result = await response.blob()
    } else if (options.responseType === 'text') {
      result = await response.text()
    } else {
      console.log('📦 Processing response as json')
      result = await response.json()
    }

    if (typeof process !== 'undefined' && process.env.NODE_ENV === 'development' && options.responseType !== 'blob') {
      console.log('✅ Response:', result)
    }

    return result as T
  }

  /**
   * GET 요청
   */
  async get<T>(endpoint: string, options: { responseType?: 'json' | 'blob' | 'text' } = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    if (typeof process !== 'undefined' && process.env.NODE_ENV === 'development') {
      console.log('📥 GET:', url, 'Options:', options)
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

    let result: any
    if (options.responseType === 'blob') {
      result = await response.blob()
    } else if (options.responseType === 'text') {
      result = await response.text()
    } else {
      result = await response.json()
    }

    if (typeof process !== 'undefined' && process.env.NODE_ENV === 'development' && options.responseType !== 'blob') {
      console.log('✅ Response:', result)
    }

    return result as T
  }
}

// 싱글톤 인스턴스 export
export const apiClient = new ApiClient()
