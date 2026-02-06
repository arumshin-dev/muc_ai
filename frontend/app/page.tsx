import Link from 'next/link'

export default function Home() {
    return (
        <main className="home-page">
            <div className="hero-section">
                <h1 className="hero-title">
                    <span className="gradient-text">AI 광고 콘텐츠 생성</span>
                </h1>
            </div>

            <div className="features-section">
                <h2>제공 기능</h2>

                <div className="features-grid">
                    <Link href="/ad-copy" className="feature-card active">
                        <div className="feature-icon">✨</div>
                        <h3>문구 생성</h3>
                        <p>짧은 문구를 생성합니다</p>
                        <span className="feature-status available">사용 가능</span>
                    </Link>

                    <Link href="/test_image_gen" className="feature-card active">
                    {/* <div className="feature-card disabled"> */}
                        <div className="feature-icon">🎨</div>
                        <h3>이미지 생성</h3>
                        <p>텍스트 설명으로 이미지를 생성합니다</p>
                        {/* <span className="feature-status">준비 중</span> */}
                        <span className="feature-status available">사용 가능</span>
                    {/* </div> */}
                    </Link>

                    <Link href="/blog/gpt4" className="feature-card active">
                        <div className="feature-icon">📋</div>
                        <h3>블로그 글쓰기</h3>
                        <p>gpt4,gpt5</p>

                        <span className="feature-status">준비 중</span>
                    </Link>
                    {/* <Link href="https://3001-firebase-mucaigit-1769950444332.cluster-xpmcxs2fjnhg6xvn446ubtgpio.cloudworkstations.dev/" className="feature-card active"> */}
                    <div className="feature-card disabled">
                        <div className="feature-icon">📋</div>
                        <h3>test</h3>
                        <Link href="https://3001-firebase-mucaigit-1769950444332.cluster-xpmcxs2fjnhg6xvn446ubtgpio.cloudworkstations.dev/">
                        <p>index.html</p>
                        </Link>
                        {/* <Link href="https://3001-firebase-mucaigit-1769950444332.cluster-xpmcxs2fjnhg6xvn446ubtgpio.cloudworkstations.dev/blog_gpt4.html">
                        <p>blog_gpt4</p>
                        </Link>
                        <Link href="https://3001-firebase-mucaigit-1769950444332.cluster-xpmcxs2fjnhg6xvn446ubtgpio.cloudworkstations.dev/blog_gpt5.html">
                        <p>blog_gpt5</p>
                        </Link> */}
                        <span className="feature-status">준비 중</span>
                    </div>
                    {/* </Link> */}
                </div>
            </div>

        </main>
    )
}
