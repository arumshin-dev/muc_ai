"use client";

import { useState } from 'react';
import styles from './gpt4/page.module.css'; // GPT-4 페이지의 스타일을 재사용합니다.
import Link from 'next/link';

// API 응답 결과의 타입을 정의합니다.
interface GPT5BlogResult {
    title: string;
    content: string;
    hashtags: string[];
    topic: string;
    style: string;
    length: string;
    word_count: number;
    model_used: string;
}

export default function BlogAIPage() {
    const [topic, setTopic] = useState('');
    const [style, setStyle] = useState('일반');
    const [length, setLength] = useState('중간');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<GPT5BlogResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    // 안전하게 변환
    const hashtags = Array.isArray(result?.hashtags)
    ? result.hashtags
    : typeof result?.hashtags === 'string'
        ? result.hashtags.split(' ').map(tag => tag.trim()).filter(Boolean)
        : [];
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!topic.trim()) {
            alert('주제를 입력해주세요.');
            return;
        }
        
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            // ⭐️ 새로 만든 GPT-5 API 엔드포인트를 호출합니다.
            const apiUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/generate-gpt5-blog`;
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic, style, length }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => null);
                throw new Error(errorData?.detail || `서버 오류: ${response.status}`);
            }

            const data: GPT5BlogResult = await response.json();
            setResult(data);

        } catch (err: any) {
            setError(err.message || '알 수 없는 오류가 발생했습니다.');
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setTopic('');
        setStyle('일반');
        setLength('중간');
        setResult(null);
        setError(null);
    };

    const handleCopy = () => {
        if (!result) return;
        const textToCopy = `${result.title}\n\n${result.content.replace(/<br>/g, '\n')}`;
        navigator.clipboard.writeText(textToCopy).then(() => {
            alert('블로그 글이 클립보드에 복사되었습니다!');
        }).catch(err => {
            alert('복사에 실패했습니다: ' + err);
        });
    };

    return (
        <div className={styles.pageContainer}>
            <main className={styles.container}>
                <div className={styles.pageHeader}>
                    <h1>🚀 GPT-5 블로그 AI</h1>
                    <p>최신 GPT-5 모델로 자연스럽고 창의적인 블로그 글을 생성합니다.</p>
                    {/* <nav className={styles.navLinks}>
                        <Link href="/blog" className={styles.activeLink}>블로그 AI (GPT-5)</Link>
                        <Link href="/blog/gpt4">블로그 AI (GPT-4)</Link>
                    </nav> */}
                </div>

                <div className={styles.blogContainer}>
                    <div className={styles.formSection}>
                        <h2>정보 입력</h2>
                        <form onSubmit={handleSubmit}>
                            <div className={styles.formGroup}>
                                <label htmlFor="topic">주제 *</label>
                                <input
                                    type="text"
                                    id="topic"
                                    value={topic}
                                    onChange={(e) => setTopic(e.target.value)}
                                    placeholder="예: 인공지능, 딥러닝, 양자컴퓨팅"
                                    required
                                />
                            </div>
                            <div className={styles.formGroup}>
                                <label htmlFor="style">글 스타일</label>
                                <select id="style" value={style} onChange={(e) => setStyle(e.target.value)}>
                                    <option value="일반">일반</option>
                                    <option value="전문">전문</option>
                                    <option value="기술">기술</option>
                                    <option value="캐주얼">캐주얼</option>
                                    <option value="마케팅">마케팅</option>
                                </select>
                            </div>
                            <div className={styles.formGroup}>
                                <label htmlFor="length">글 길이</label>
                                <select id="length" value={length} onChange={(e) => setLength(e.target.value)}>
                                    <option value="짧음">짧음</option>
                                    <option value="중간">중간</option>
                                    <option value="김">김</option>
                                </select>
                            </div>
                            <button type="submit" className={styles.btnPrimary} disabled={loading}>
                                {loading ? (<>
                                        <div className={styles.loadingSpinner}></div>
                                        <span>생성 중...</span>
                                    </>
                                ) : '🚀 GPT-5로 글 생성하기'}
                            </button>
                        </form>
                    </div>

                    <div className={styles.resultSection}>
                        <h2>생성된 글</h2>
                        {loading && <div className={styles.loadingSpinner}></div>}
                        {error && <div className={styles.errorState}>{error}</div>}
                        
                        {result && (
                            <div id="result-container">
                                <div className={styles.resultHeader}>
                                    <h3 id="result-title">{result.title}</h3>
                                    <div className={styles.resultMeta}>
                                        <span>주제: {result.topic}</span>
                                        <span>모델: {result.model_used}</span>
                                        <span>분량: {result.length}</span>
                                        <span>글자수: {result.word_count}</span>
                                    </div>
                                </div>
                                <div className={styles.contentSection}>
                                    <div dangerouslySetInnerHTML={{ __html: result.content }} className={styles.blogContent} />
                                </div>
                                <div className={styles.hashtagsSection}>
                                    <h4>🏷️ 해시태그</h4>
                                    <div className={styles.hashtags}>

                                        {hashtags.length > 0 ? (
                                            hashtags.map((tag, index) => (
                                            <span key={index} className={styles.hashtag}>{tag}</span>
                                            ))
                                        ) : (
                                            <span className={styles.noHashtag}>해시태그 없음</span>
                                        )}

                                    </div>

                                </div>
                                <div className={styles.actions}>
                                    <button onClick={handleCopy} className={styles.btnSecondary}>📋 복사하기</button>
                                    <button onClick={handleReset} className={styles.btnSecondary}>🔄 새 글쓰기</button>
                                </div>
                            </div>
                        )}

                        {!result && !loading && !error && (
                            <div className={styles.emptyState}>
                                <h3>생성된 글이 여기에 표시됩니다.</h3>
                                <p>주제를 입력하고 스타일과 길이를 선택한 후, 생성하기 버튼을 누르세요.</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
