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

export default function AdCopyPage() {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<AdCopyResponse | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [providers, setProviders] = useState<AIProvider[]>([])

    useEffect(() => {
        const fetchProviders = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/providers')
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
        console.log('Generating ad copy with data:', formData);
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await fetch('http://localhost:8000/api/ad-copy/generate', {
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
                const errorData = await response.json();
                console.error('API Error Response:', errorData);
                throw new Error(errorData.detail || '광고 문구 생성에 실패했습니다');
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
                <h1>GPT 광고 문구 생성</h1>
                {/* <p>AI를 활용하여 매력적인 광고 문구를 자동으로 생성하세요</p> */}
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
                        fixedProvider="openai"    // 제공자 고정
                        fixedModel="gpt-5-mini" // 현재 작동 가능한 모델로 고정하여 테스트
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
                            <p>👈 왼쪽 폼을 작성하고 광고 문구를 생성해보세요!</p>
                        </div>
                    )}
                </div>
            </div>
        </main>
    )
}
