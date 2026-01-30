'use client'

import { useEffect, useState } from 'react'

interface Item {
    id: number
    name: string
    description: string | null
}

export default function Home() {
    const [items, setItems] = useState<Item[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        fetchItems()
    }, [])

    const fetchItems = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/items')
            if (!response.ok) {
                throw new Error('Failed to fetch items')
            }
            const data = await response.json()
            setItems(data)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred')
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="container">
            <div className="header">
                <h1>MUC AI</h1>
                <p className="subtitle">FastAPI + Next.js Application</p>
            </div>

            <div className="content">
                <h2>Items from Backend</h2>

                {loading && <p className="loading">Loading...</p>}

                {error && <p className="error">Error: {error}</p>}

                {!loading && !error && (
                    <div className="items-grid">
                        {items.map((item) => (
                            <div key={item.id} className="item-card">
                                <h3>{item.name}</h3>
                                <p>{item.description || 'No description'}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </main>
    )
}
