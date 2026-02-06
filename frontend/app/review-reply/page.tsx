'use client'

import { useState } from 'react'
import { apiClient, ApiError } from '@/lib/api'
import { API_ENDPOINTS } from '@/lib/config'
import LoadingSpinner from '../components/LoadingSpinner'

export default function ReviewReplyPage() {
    const [loading, setLoading] = useState(false)
    const [reply, setReply] = useState<string | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [customerReview, setCustomerReview] = useState<string>('')
    const [selectedTone, setSelectedTone] = useState<string>('neutral')
    const [selectedLanguage, setSelectedLanguage] = useState<string>('ko')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setReply(null)

        try {
            const data = await apiClient.post<{ reply: string }>(
                API_ENDPOINTS.reviewReply.generate,
                {
                    customer_review: customerReview,
                    tone: selectedTone,
                    language: selectedLanguage,
                }
            )
            setReply(data.reply)
            
        } catch (err) {
            console.error('Error generating review reply:', err)
            
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
        <main className="review-reply-page">
            <div className="page-header">
                <h1>리뷰 답글 생성</h1>
                <p>AI를 활용하여 고객 리뷰에 대한 답글을 작성하세요.</p>
            </div>

            <div className="page-content">
                <div className="form-section">
                    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                        <div>
                            <label htmlFor="customerReview" className="block text-sm font-medium text-gray-700">
                                고객 리뷰
                            </label>
                            <textarea
                                id="customerReview"
                                rows={6}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={customerReview}
                                onChange={(e) => setCustomerReview(e.target.value)}
                                placeholder="고객의 리뷰 내용을 여기에 붙여넣으세요."
                                required
                            ></textarea>
                        </div>

                        <div>
                            <label htmlFor="tone" className="block text-sm font-medium text-gray-700">
                                답글 톤
                            </label>
                            <select
                                id="tone"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={selectedTone}
                                onChange={(e) => setSelectedTone(e.target.value)}
                            >
                                <option value="neutral">기본</option>
                                <option value="formal">격식있는</option>
                                <option value="friendly">친근한</option>
                                <option value="apologetic">사과하는</option>
                                <option value="grateful">감사하는</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="language" className="block text-sm font-medium text-gray-700">
                                언어
                            </label>
                            <select
                                id="language"
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
                                value={selectedLanguage}
                                onChange={(e) => setSelectedLanguage(e.target.value)}
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
                                    <span>답글 생성 중...</span>
                                </>
                            ) : (
                                '답글 생성'
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

                    {reply && !loading && (
                        <div className="reply-result border p-4 rounded-md bg-gray-50">
                            <h3 className="text-lg font-medium mb-2">생성된 답글:</h3>
                            <p style={{ whiteSpace: 'pre-line' }}>{reply}</p>
                        </div>
                    )}

                    {!loading && !error && !reply && (
                        <div className="placeholder text-gray-500">
                            <p>👆 고객 리뷰를 입력하고 답글을 생성해보세요!</p>
                        </div>
                    )}
                </div>
            </div>
        </main>
    )
}
