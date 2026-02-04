// frontend/lib/config.ts (새로 만들기)
/**
 * API 엔드포인트 중앙 관리
 */
export const API_ENDPOINTS = {
    adCopy: {
      providers: '/api/ad-copy/providers',
      generate: '/api/ad-copy/generate',
      history: '/api/ad-copy/history',
      getById: (id: number) => `/api/ad-copy/${id}`,
    },
    text: {
      providers: '/api/text/providers',
      generate: '/api/text/generate',
    },
    image: {
      providers: '/api/image/providers',
      generate: '/api/image/generate',
    },
    // 나중에 추가할 엔드포인트
    vision: {
      providers: '/api/vision/providers',
      analyze: '/api/vision/analyze',
    },
  } as const;
  
  // 타입 추출 (선택사항)
  export type ApiEndpoints = typeof API_ENDPOINTS;
  