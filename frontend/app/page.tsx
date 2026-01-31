import Link from 'next/link'

export default function Home() {
    return (
        <main className="home-page">
            <div className="hero-section">
                <h1 className="hero-title">
                    소상공인을 위한<br />
                    <span className="gradient-text">AI 광고 콘텐츠 생성</span>
                </h1>
                <p className="hero-subtitle">
                    디자인 역량이나 전문 도구 없이도<br />
                    생성형 AI로 손쉽게 광고 콘텐츠를 제작하세요
                </p>
            </div>

            <div className="features-section">
                <h2>제공 기능</h2>

                <div className="features-grid">
                    <Link href="/ad-copy" className="feature-card active">
                        <div className="feature-icon">✨</div>
                        <h3>광고 문구 생성</h3>
                        <p>AI가 제품 특징을 분석하여 매력적인 광고 문구를 자동으로 생성합니다</p>
                        <span className="feature-status available">사용 가능</span>
                    </Link>

                    <div className="feature-card disabled">
                        <div className="feature-icon">🎨</div>
                        <h3>제품 이미지 생성</h3>
                        <p>제품 설명만으로 전문적인 이미지를 생성합니다</p>
                        <span className="feature-status">준비 중</span>
                    </div>

                    <div className="feature-card disabled">
                        <div className="feature-icon">🖼️</div>
                        <h3>배너 디자인</h3>
                        <p>SNS, 웹사이트용 배너를 자동으로 디자인합니다</p>
                        <span className="feature-status">준비 중</span>
                    </div>

                    <div className="feature-card disabled">
                        <div className="feature-icon">📋</div>
                        <h3>메뉴판 제작</h3>
                        <p>음식점, 카페를 위한 메뉴판을 간편하게 제작합니다</p>
                        <span className="feature-status">준비 중</span>
                    </div>
                </div>
            </div>

            <div className="ai-providers-section">
                <h3>지원하는 AI 모델</h3>
                <div className="providers-list">
                    <div className="provider-badge">OpenAI GPT-5</div>
                    <div className="provider-badge">Groq Llama 3.3 (무료)</div>
                    <div className="provider-badge">Google Gemini (무료)</div>
                </div>
                <p className="providers-note">
                    사용자가 직접 AI 제공자와 모델을 선택할 수 있습니다
                </p>
            </div>
        </main>
    )
}
