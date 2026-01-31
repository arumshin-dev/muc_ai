import './globals.css'
import type { Metadata } from 'next'
import './globals.css'
import Navigation from './components/Navigation'

export const metadata: Metadata = {
    title: 'MUC AI - 소상공인 광고 콘텐츠 생성',
    description: '생성형 AI를 활용한 광고 문구 자동 생성 서비스',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="ko">
            <body>
                <Navigation />
                {children}
            </body>
        </html>
    )
}
