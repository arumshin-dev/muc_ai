'use client'

import { useState } from 'react'
import { apiClient, ApiError } from '@/lib/api'
import { API_ENDPOINTS } from '@/lib/config'
import LoadingSpinner from '../components/LoadingSpinner'

export default function ProductReviewPage() {
    const [loading, setLoading] = useState(false)
    const [review, setReview] = useState<string | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [productName, setProductName] = useState<string>('')
    const [sentiment, setSentiment] = useState<string>('good')
    const [pros, setPros] = useState<string>('')
    const [cons, setCons] = useState<string>('')
    const [length, setLength] = useState<number>(500)
    const [language, setLanguage] = useState<string>('ko')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setReview(null)

        try {
            const data = await apiClient.post<{ review: string }>(
                API_ENDPOINTS.productReview.generate,
                {
                    product_name: productName,
                    sentiment: sentiment,
                    pros: pros,
                    cons: cons,
                    length: length,
                    language: language,
                }
            )
            setReview(data.review)
            
        } catch (err) {
            console.error('Error generating product review:', err)
            
            if (err instanceof ApiError) {
                const errorMessage = err.detail || err.message
                setError(`❌ 오류 (${err.statusCode}): ${errorMessage}`)
            } else if (err instanceof Error) {
                setError(`❌ 오류: ${err.message}`)
            } else {
                setError('❌ 알 수 없는 오류가 발생했습니다. 네트워크 연결을 확인해주세요.')
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="product-review-page">
            <div className="page-header">
                <h1>제품 리뷰 생성</h1>
                <p>AI를 활용하여 쇼핑몰 제품 리뷰를 생성합니다.</p>
            </div>

            <div className="page-content">
                <div className="form-section">
                    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                        <div>
                            <label htmlFor="productName" className="block text-sm font-medium text-gray-700">
                                제품명
                            </label>
                            <input
                                type="text"
                                id="productName"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={productName}
                                onChange={(e) => setProductName(e.target.value)}
                                placeholder="예: 아이폰 15 프로"
                                required
                            />
                        </div>

                        <div>
                            <label htmlFor="sentiment" className="block text-sm font-medium text-gray-700">
                                전반적인 평가
                            </label>
                            <select
                                id="sentiment"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={sentiment}
                                onChange={(e) => setSentiment(e.target.value)}
                            >
                                <option value="good">좋다 (긍정)</option>
                                <option value="bad">나쁘다 (부정)</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="pros" className="block text-sm font-medium text-gray-700">
                                장점 (쉼표로 구분)
                            </label>
                            <input
                                type="text"
                                id="pros"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={pros}
                                onChange={(e) => setPros(e.target.value)}
                                placeholder="예: 빠른 성능, 고급스러운 디자인"
                            />
                        </div>

                        <div>
                            <label htmlFor="cons" className="block text-sm font-medium text-gray-700">
                                단점 (쉼표로 구분)
                            </label>
                            <input
                                type="text"
                                id="cons"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={cons}
                                onChange={(e) => setCons(e.target.value)}
                                placeholder="예: 비싼 가격, 무거운 무게"
                            />
                        </div>

                        <div>
                            <label htmlFor="length" className="block text-sm font-medium text-gray-700">
                                길이 (글자 수)
                            </label>
                            <select
                                id="length"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={length}
                                onChange={(e) => setLength(parseInt(e.target.value))}
                            >
                                <option value={50}>50자</option>
                                <option value={500}>500자</option>
                                <option value={1000}>1000자</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="language" className="block text-sm font-medium text-gray-700">
                                언어
                            </label>
                            <select
                                id="language"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={language}
                                onChange={(e) => setLanguage(e.target.value)}
                            >
                                <option value="ko">한국어</option>
                                <option value="en">영어</option>
                            </select>
                        </div>

                        <button
                            type="submit"
                            className={`inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white ${
                                loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
                            }`}
                            disabled={loading}
                        >
                            {loading ? (
                                <>
                                    <LoadingSpinner />
                                    <span>리뷰 생성 중...</span>
                                </>
                            ) : (
                                '리뷰 생성'
                            )}
                        </button>
                    </form>
                </div>

                <div className="result-section mt-8">
                    {loading && <LoadingSpinner />}

                    {error && (
                        <div className="error-message text-red-600">
                            <h3>⚠️ 오류 발생</h3>
                            <p>{error}</p>
                        </div>
                    )}

                    {review && !loading && (
                        <div className="review-result border p-4 rounded-md bg-gray-50">
                            <h3 className="text-lg font-medium mb-2">생성된 리뷰:</h3>
                            <p style={{ whiteSpace: 'pre-line' }}>{review}</p>
                        </div>
                    )}

                    {!loading && !error && !review && (
                        <div className="placeholder text-gray-500">
                            <p>👆 제품 정보를 입력하고 리뷰를 생성해보세요!</p>
                        </div>
                    )}
                </div>
            </div>
        </main>
    )
}
