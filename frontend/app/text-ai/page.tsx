'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { apiClient } from '@/lib/api'
import { AIProvider } from '../components/AdCopyForm'
import LoadingSpinner from '../components/LoadingSpinner'

export default function TextAILandingPage() {
    const [providers, setProviders] = useState<AIProvider[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchProviders = async () => {
            try {
                const data = await apiClient.get<any>('/api/providers')
                setProviders(data.providers)
            } catch (err) {
                console.error('Failed to fetch providers:', err)
            } finally {
                setLoading(false)
            }
        }
        fetchProviders()
    }, [])

    if (loading) return <div className="page-center"><LoadingSpinner /></div>

    return (
        <main className="text-ai-page p-8">
            <div className="page-header mb-8 text-center">
                <h1 className="text-3xl font-bold mb-2">AI 모델별 테스트</h1>
                <p className="text-gray-600">각 모델별로 광고 문구 생성 성능을 테스트해보세요.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                {providers.map(provider => (
                    <div key={provider.name} className="provider-card border rounded-lg p-6 shadow-sm bg-white">
                        <h2 className="text-xl font-semibold mb-4 border-b pb-2 uppercase tracking-wider">
                            {provider.name} {provider.free && <span className="text-sm font-normal text-green-500 ml-2">(무료)</span>}
                        </h2>
                        <ul className="space-y-2">
                            {provider.models.map(model => (
                                <li key={model}>
                                    <Link
                                        href={`/text-ai/${encodeURIComponent(model)}`}
                                        className="block p-3 rounded-md hover:bg-blue-50 hover:text-blue-600 transition-colors border border-transparent hover:border-blue-200"
                                    >
                                        {model}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>

            <div className="mt-12 text-center">
                <Link
                    href="/ad-copy"
                    className="inline-block px-6 py-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
                >
                    기존 광고 문구 생성으로 돌아가기
                </Link>
            </div>

            <style jsx>{`
                .text-ai-page {
                    min-height: 100vh;
                    background-color: #f8fafc;
                }
                .provider-card h2 {
                    color: #1e293b;
                }
            `}</style>
        </main>
    )
}
