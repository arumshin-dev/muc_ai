'use client'

import { useState } from 'react'

interface AdCopyResultProps {
    copies: string[]
    provider: string
    model: string
}

export default function AdCopyResult({ copies, provider, model }: AdCopyResultProps) {
    const [copiedIndex, setCopiedIndex] = useState<number | null>(null)

    const copyToClipboard = async (text: string, index: number) => {
        try {
            await navigator.clipboard.writeText(text)
            setCopiedIndex(index)
            setTimeout(() => setCopiedIndex(null), 2000)
        } catch (err) {
            console.error('Failed to copy:', err)
        }
    }

    return (
        <div className="ad-copy-result">
            <div className="result-header">
                <h3>생성된 광고 문구</h3>
                <div className="ai-info">
                    <span className="provider-badge">{provider}</span>
                    <span className="model-badge">{model}</span>
                </div>
            </div>

            <div className="copies-list">
                {copies.map((copy, index) => (
                    <div key={index} className="copy-item">
                        <div className="copy-number">{index + 1}</div>
                        <div className="copy-text">{copy}</div>
                        <button
                            onClick={() => copyToClipboard(copy, index)}
                            className="copy-button"
                        >
                            {copiedIndex === index ? '✓ 복사됨' : '복사'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}
