'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navigation() {
    const pathname = usePathname()

    const navItems = [
        { name: '홈', path: '/' },
        { name: '광고 문구 생성', path: '/ad-copy' },
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
