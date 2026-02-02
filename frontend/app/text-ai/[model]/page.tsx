'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { apiClient, ApiError } from '@/lib/api'
import AdCopyForm, { FormData, AIProvider } from '../../components/AdCopyForm'
import AdCopyResult from '../../components/AdCopyResult'
import LoadingSpinner from '../../components/LoadingSpinner'

interface AdCopyResponse {
    id: number
    generated_copies: string[]
    ai_provider: string
    ai_model: string
}

export default function TextAIModelPage() {
    const params = useParams()
    const model = decodeURIComponent(params.model as string)  // 👈 decodeURIComponent 추가

    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<AdCopyResponse | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [providers, setProviders] = useState<AIProvider[]>([])

    // 모델명에 따른 프로바이더 추측
    const getProviderForModel = (modelName: string) => {
        if (modelName.startsWith('gpt-')) return 'openai'
        if (modelName.includes('gemini') || modelName.startsWith('models/')) return 'gemini'
        return 'huggingface'
    }

    const provider = getProviderForModel(model)

    useEffect(() => {
        const fetchProviders = async () => {
            try {
                const data = await apiClient.get<any>('/api/providers')
                setProviders(data.providers)
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
            const data = await apiClient.post<AdCopyResponse>(
                '/api/ad-copy/generate',
                {
                    ...formData,
                    strict_mode: true
                }
            )
            setResult(data)
            
        } catch (err) {
            console.error('Error generating ad copy:', err)
            
            if (err instanceof ApiError) {
                const errorMessage = err.detail || err.message
                
                switch (err.statusCode) {
                    case 429:
                        setError(`⚠️ ${errorMessage}\n\n다른 AI 모델을 선택해주세요.`)
                        break
                    case 403:
                        setError(`🔒 ${errorMessage}\n\nLlama 계열 모델을 선택해주세요.`)
                        break
                    case 504:
                        setError(`⏳ ${errorMessage}\n\n잠시 후 다시 시도해주세요.`)
                        break
                    case 400:
                        setError(`❌ ${errorMessage}`)
                        break
                    default:
                        setError(`❌ 서버 오류 (${err.statusCode}): ${errorMessage}\n\n다른 모델을 시도하거나 잠시 후 다시 시도해주세요.`)
                }
            } else if (err instanceof Error) {
                setError(err.message)
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
                <h1>{model} 모델 테스트</h1>
                <p>{model} 모델을 사용하여 광고 문구를 생성해봅니다.</p>
                <div className="mt-4">
                    <a href="/text-ai" className="text-blue-600 hover:underline">
                        ← 모델 목록으로 돌아가기
                    </a>
                </div>
            </div>

            <div className="page-content">
                <div className="form-section">
                    <AdCopyForm
                        onSubmit={handleSubmit}
                        loading={loading}
                        availableProviders={providers}
                        fixedProvider={provider}
                        fixedModel={model}
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
                                    <li>다른 AI 모델을 선택해보세요</li>
                                    <li>HuggingFace 사용 시 Llama-3.2-3B 모델을 권장합니다</li>
                                    <li>모델 로딩에 시간이 걸릴 수 있습니다</li>
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
                            <p>👈 모델 테스트를 위해 왼쪽 폼을 작성해주세요.</p>
                        </div>
                    )}
                </div>
            </div>
        </main>
    )
}
