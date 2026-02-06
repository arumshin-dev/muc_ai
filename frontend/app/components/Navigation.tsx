'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navigation() {
    const pathname = usePathname()

    const navItems = [
        { name: '홈', path: '/' },
        { name: '테스트 텍스트', path: '/test_text'},
        { name: '광고 문구 생성', path: '/ad-copy' },
        { name: '이미지 생성', path: '/test_image_gen' },
        { name: '블로그 글쓰기gpt5', path: '/blog' },
        { name: '블로그 글쓰기gpt4', path: '/blog/gpt4' },
        { name: '리뷰 생성', path: '/product-review' },
        { name: '리뷰 답글 생성', path: '/review-reply' },

    ]

    return (
        <nav className="navigation">
            <div className="nav-container">
                <Link href="/" className="logo">
                    MUC AI
                </Link>

                <div className="nav-links">
                    {navItems.map((item) => (
                        <Link
                            key={item.path}
                            href={item.path}
                            className={`nav-link ${pathname === item.path ? 'active' : ''}`}
                        >
                            {item.name}
                        </Link>
                    ))}
                </div>
            </div>
        </nav>
    )
}
