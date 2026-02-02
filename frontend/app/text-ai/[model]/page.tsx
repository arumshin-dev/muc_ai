'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import AdCopyForm, { FormData, AIProvider } from '../../components/AdCopyForm'
import AdCopyResult from '../../components/AdCopyResult'
import LoadingSpinner from '../../components/LoadingSpinner'

interface AdCopyResponse {
    id: number
    generated_copies: string[]
    ai_provider: string
    ai_model: string
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function TextAIModelPage() {
    const params = useParams()
    const model = params.model as string

    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<AdCopyResponse | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [providers, setProviders] = useState<AIProvider[]>([])

    // 모델명에 따른 프로바이더 추측
    const getProviderForModel = (modelName: string) => {
        if (modelName.startsWith('gpt-')) return 'openai'
        if (modelName.startsWith('gemini-')) return 'gemini'
        return 'huggingface' // 기본값
    }

    const provider = getProviderForModel(model)

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
            const response = await fetch(`${API_BASE_URL}/api/ad-copy/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...formData,
                    strict_mode: true
                })
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || '광고 문구 생성에 실패했습니다')
            }

            const data: AdCopyResponse = await response.json()
            setResult(data)
        } catch (err) {
            setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다')
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="ad-copy-page">
            <div className="page-header">
                <h1>{model.toUpperCase()} 모델 테스트</h1>
                <p>{model} 모델을 사용하여 광고 문구를 생성해봅니다.</p>
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
                            <h3>오류 발생</h3>
                            <p>{error}</p>
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
                            <p>모델 테스트를 위해 왼쪽 폼을 작성해주세요.</p>
                        </div>
                    )}
                </div>
            </div>
        </main>
    )
}
