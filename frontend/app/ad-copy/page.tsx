'use client'

import { useEffect, useState } from 'react'
import AdCopyForm, { FormData, AIProvider } from '../components/AdCopyForm'
import AdCopyResult from '../components/AdCopyResult'
import LoadingSpinner from '../components/LoadingSpinner'

interface AdCopyResponse {
    id: number
    generated_copies: string[]
    ai_provider: string
    ai_model: string
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function AdCopyPage() {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<AdCopyResponse | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [providers, setProviders] = useState<AIProvider[]>([])

    useEffect(() => {
        const fetchProviders = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/providers`)
                if (response.ok) {
                    const data = await response.json()
                    setProviders(data.providers)
                }
            } catch (err) {
                console.error('Failed to fetch providers:', err)
            }
        }
        fetchProviders()
    }, [])

    const handleSubmit = async (formData: FormData) => {
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            console.log('Generating ad copy with data:', formData)
            
            const response = await fetch(`${API_BASE_URL}/api/ad-copy/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })

            if (!response.ok) {
                const errorData = await response.json()
                const errorMessage = errorData.detail || '광고 문구 생성에 실패했습니다'
                
                // 상태 코드별 처리
                if (response.status === 429) {
                    // API 사용량 초과 (Gemini 무료 크레딧 소진 등)
                    throw new Error(
                        `⚠️ ${errorMessage}\n\n다른 AI 모델을 선택해주세요.`
                    )
                } else if (response.status === 403) {
                    // 권한 없음 (Gemma 등 제한된 모델)
                    throw new Error(
                        `🔒 ${errorMessage}\n\nLlama 계열 모델을 선택해주세요.`
                    )
                } else if (response.status === 504) {
                    // 타임아웃 (모델 로딩 중)
                    throw new Error(
                        `⏳ ${errorMessage}\n\n잠시 후 다시 시도해주세요.`
                    )
                } else if (response.status === 400) {
                    // 잘못된 요청
                    throw new Error(`❌ ${errorMessage}`)
                } else {
                    // 기타 서버 오류
                    throw new Error(
                        `❌ 서버 오류 (${response.status}): ${errorMessage}\n\n다른 모델을 시도하거나 잠시 후 다시 시도해주세요.`
                    )
                }
            }

            const data: AdCopyResponse = await response.json()
            console.log('Success:', data)
            setResult(data)
            
        } catch (err) {
            console.error('Error generating ad copy:', err)
            
            if (err instanceof Error) {
                setError(err.message)
            } else if (typeof err === 'string') {
                setError(err)
            } else {
                setError('알 수 없는 오류가 발생했습니다. 네트워크 연결을 확인해주세요.')
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="ad-copy-page">
            <div className="page-header">
                <h1>광고 문구 생성</h1>
                <p>AI를 활용하여 매력적인 광고 문구를 자동으로 생성하세요</p>
                <div className="mt-4">
                    <a href="/text-ai" className="text-blue-600 hover:underline">
                        모델별 테스트 페이지로 이동하기 →
                    </a>
                </div>
            </div>

            <div className="page-content">
                <div className="form-section">
                    <AdCopyForm 
                        onSubmit={handleSubmit} 
                        loading={loading} 
                        availableProviders={providers} 
                    />
                </div>

                <div className="result-section">
                    {loading && <LoadingSpinner />}

                    {error && (
                        <div className="error-message">
                            <h3>⚠️ 오류 발생</h3>
                            <p style={{ whiteSpace: 'pre-line' }}>{error}</p>
                            <div className="mt-4 text-sm text-gray-600">
                                <p>💡 문제 해결 방법:</p>
                                <ul className="list-disc ml-6 mt-2">
                                    <li>다른 AI 제공자나 모델을 선택해보세요</li>
                                    <li>Gemini 무료 크레딧이 소진된 경우 OpenAI나 HuggingFace를 사용하세요</li>
                                    <li>HuggingFace 사용 시 Llama-3.2-3B 모델을 권장합니다</li>
                                </ul>
                            </div>
                        </div>
                    )}

                    {result && !loading && (
                        <AdCopyResult
                            copies={result.generated_copies}
                            provider={result.ai_provider}
                            model={result.ai_model}
                        />
                    )}

                    {!loading && !error && !result && (
                        <div className="placeholder">
                            <p>👈 왼쪽 폼을 작성하고 광고 문구를 생성해보세요!</p>
                        </div>
                    )}
                </div>
            </div>
        </main>
    )
}
