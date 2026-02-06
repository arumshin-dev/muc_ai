"use client";

import { useState } from 'react';
import styles from './page.module.css';

// API 응답 데이터의 타입을 정의합니다.
interface BlogContent {
    title: string;
    metaDescription: string;
    content: string;
    hashtags: string[];
    wordCount: number;
    model: string;
    style: string;
}

export default function BlogGPT4Page() {
    const [keyword, setKeyword] = useState('');
    const [style, setStyle] = useState('일반');
    const [length, setLength] = useState('중간');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<BlogContent | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [copySuccess, setCopySuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);
        setCopySuccess(false);

        try {
            const apiUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/generate-gpt4-blog`;
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ keyword, style, length, model: 'gpt-4' }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => null);
                throw new Error(errorData?.detail || `서버에서 오류가 발생했습니다: ${response.status}`);
            }

            const data: BlogContent = await response.json();
            setResult(data);

        } catch (err: any) {
            setError(err.message || '알 수 없는 오류가 발생했습니다.');
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setKeyword('');
        setStyle('일반');
        setLength('중간');
        setResult(null);
        setError(null);
        setCopySuccess(false);
    };

    // ⭐️ 클립보드에 복사하는 기능
    const handleCopy = () => {
        if (!result) return;
        setCopySuccess(false);

        // 1. HTML을 순수 텍스트로 변환
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = result.content;
        const plainTextContent = tempDiv.textContent || tempDiv.innerText || "";

        // 2. 제목, 본문, 해시태그를 합쳐서 최종 텍스트 생성
        const hashtagsText = result.hashtags.map(tag => `#${tag}`).join(' ');
        const textToCopy = `${result.title}\n\n${plainTextContent}\n\n${hashtagsText}`;

        // 3. 클립보드에 복사
        navigator.clipboard.writeText(textToCopy).then(() => {
            setCopySuccess(true);
            setTimeout(() => setCopySuccess(false), 2000); // 2초 후 버튼 텍스트 원래대로
        }, (err) => {
            alert('복사에 실패했습니다: ' + err);
        });
    };

    // ⭐️ HTML 파일로 다운로드하는 기능
    const handleDownload = () => {
        if (!result) return;

        // 1. 전체 HTML 문서 내용 구성
        const fullHtml = `
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="description" content="${result.metaDescription}">
                <title>${result.title}</title>
                <style>body { font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; } .hashtags { margin-top: 20px; } .hashtag { display: inline-block; background-color: #f0f0f0; padding: 5px 10px; border-radius: 15px; margin-right: 5px; }</style>
            </head>
            <body>
                <h1>${result.title}</h1>
                <hr />
                ${result.content}
                <div class="hashtags">
                    ${result.hashtags.map(tag => `<span class="hashtag">#${tag}</span>`).join('\n')}
                </div>
            </body>
            </html>
        `;

        // 2. Blob 객체 생성 및 다운로드 링크 생성
        const blob = new Blob([fullHtml], { type: 'text/html;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        const sanitizedTitle = result.title.replace(/[/\\?%*:|"<>]/g, '-'); // 파일명에 부적합한 문자 제거
        link.download = `${sanitizedTitle}.html`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    return (
        <div className={styles.pageContainer}>
            {/* Header는 주석 처리된 상태로 유지 */}

            <main className={styles.container}>
                <div className={styles.pageHeader}>
                    <h1>🤖 GPT-4 블로그 AI</h1>
                    <p>SEO 최적화된 고품질 블로그 글을 생성합니다</p>
                </div>

                <div className={styles.blogContainer}>
                    <div className={styles.formSection}>
                        <h2>📝 블로그 정보 입력</h2>
                        <form id="blog-form" onSubmit={handleSubmit}>
                           {/* 폼 입력 필드들은 변경 없음 */}
                           <div className={styles.formGroup}>
                                <label htmlFor="keyword">키워드 *</label>
                                <input 
                                    type="text" 
                                    id="keyword" 
                                    name="keyword" 
                                    placeholder="예: 인공지능, 마케팅, 프로그래밍" 
                                    required 
                                    value={keyword}
                                    onChange={(e) => setKeyword(e.target.value)}
                                />
                            </div>

                            <div className={styles.formGroup}>
                                <label htmlFor="style">글 스타일</label>
                                <select id="style" name="style" value={style} onChange={(e) => setStyle(e.target.value)}>
                                    <option value="일반">일반 (친근하고 이해하기 쉬운)</option>
                                    <option value="전문">전문 (신뢰성 있는)</option>
                                    <option value="캐주얼">캐주얼 (가볍고 재미있는)</option>
                                    <option value="기술">기술 (상세한)</option>
                                    <option value="마케팅">마케팅 (설득력 있는)</option>
                                </select>
                            </div>

                            <div className={styles.formGroup}>
                                <label htmlFor="length">글 길이</label>
                                <select id="length" name="length" value={length} onChange={(e) => setLength(e.target.value)}>
                                    <option value="짧음">짧음 (300자)</option>
                                    <option value="중간">중간 (600자)</option>
                                    <option value="김">김 (1000자)</option>
                                </select>
                            </div>

                            <button type="submit" className={styles.btnPrimary} disabled={loading}>
                                {loading ? (
                                    <>
                                        <div className={styles.loadingSpinner}></div>
                                        <span>생성 중...</span>
                                    </>
                                ) : (
                                    '✨ GPT-4로 글쓰기'
                                )}
                            </button>
                        </form>
                    </div>

                    <div className={styles.resultSection}>
                        <h2>📄 생성된 블로그 글</h2>
                        {error && <div className={styles.errorState}>{error}</div>}
                        
                        {result && !loading && (
                            <div id="result-container">
                               {/* 글 내용 표시 부분은 변경 없음 */}
                                <div className={styles.resultHeader}>
                                    <h3 id="result-title">{result.title}</h3>
                                    <div className={styles.resultMeta}>
                                        <span className={styles.metaInfo}>📊 단어 수: {result.wordCount}</span>
                                        <span className={styles.metaInfo}>🤖 모델: {result.model}</span>
                                        <span className={styles.metaInfo}>🎨 스타일: {result.style}</span>
                                    </div>
                                </div>
                                <div className={styles.metaSection}>
                                    <h4>🔍 SEO 메타 정보</h4>
                                    <div className={styles.metaDescription}>
                                        <strong>메타 설명:</strong>
                                        <p>{result.metaDescription}</p>
                                    </div>
                                </div>
                                <div className={styles.contentSection}>
                                    <h4>📝 본문 내용</h4>
                                    <div dangerouslySetInnerHTML={{ __html: result.content.replace(/\n/g, '<br />') }} className={styles.blogContent}></div>
                                </div>
                                <div className={styles.hashtagsSection}>
                                    <h4>🏷️ 해시태그</h4>
                                    <div className={styles.hashtags}>
                                        {Array.isArray(result.hashtags) && result.hashtags.map((tag, index) => <span key={index} className={styles.hashtag}>#{tag}</span>)}
                                    </div>
                                </div>
                                <div className={styles.actions}>
                                    {/* ⭐️ 버튼에 onClick 이벤트 핸들러 추가 */}
                                    <button onClick={handleCopy} className={styles.btnSecondary}>
                                        {copySuccess ? '✅ 복사 완료!' : '📋 복사하기'}
                                    </button>
                                    <button onClick={handleDownload} className={styles.btnSecondary}>💾 다운로드</button>
                                    <button onClick={handleReset} className={styles.btnSecondary}>🔄 새 글쓰기</button>
                                </div>
                            </div>
                        )}
                        
                        {!result && !loading && !error && (
                            <div className={styles.emptyState}>
                                <div className={styles.emptyIcon}>📝</div>
                                <h3>아직 생성된 글이 없습니다</h3>
                                <p>위 폼에 정보를 입력하고 'GPT-4로 글쓰기' 버튼을 클릭하세요</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>

            <footer className={styles.footer}>
                <p>&copy; GPT-4 블로그 AI</p>
            </footer>
        </div>
    );
}
