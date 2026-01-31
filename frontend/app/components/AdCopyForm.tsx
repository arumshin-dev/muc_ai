'use client'

import { useState, useEffect } from 'react'

export interface AIProvider {
    name: string
    models: string[]
    default_model: string
    free?: boolean
}

interface AdCopyFormProps {
    onSubmit: (data: FormData) => void
    loading: boolean
    availableProviders: AIProvider[]
    fixedProvider?: string
    fixedModel?: string
}

export interface FormData {
    product_name: string
    category: string
    target_audience: string
    key_features: string
    tone: string
    ai_provider: string
    ai_model: string
}

export default function AdCopyForm({
    onSubmit,
    loading,
    availableProviders,
    fixedProvider,
    fixedModel
}: AdCopyFormProps) {
    const [formData, setFormData] = useState<FormData>({
        product_name: '',
        category: '',
        target_audience: '',
        key_features: '',
        tone: 'friendly',
        ai_provider: '',
        ai_model: ''
    })

    // 프로바이더가 변경될 때 기본 모델 설정을 위해
    const [selectedProvider, setSelectedProvider] = useState<AIProvider | null>(null)

    // availableProviders가 로드되면 기본값 설정
    useEffect(() => {
        if (availableProviders.length > 0) {
            let providerToSelect: AIProvider | undefined;

            if (fixedProvider) {
                providerToSelect = availableProviders.find(p => p.name === fixedProvider);
            }

            if (!providerToSelect && !formData.ai_provider) {
                providerToSelect = availableProviders.find(p => p.name === 'gemini') || availableProviders[0];
            }

            if (providerToSelect) {
                setSelectedProvider(providerToSelect);
                setFormData((prev: FormData) => ({
                    ...prev,
                    ai_provider: providerToSelect!.name,
                    ai_model: fixedModel || providerToSelect!.default_model
                }));
            }
        }
    }, [availableProviders, fixedProvider, fixedModel]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit(formData)
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target

        if (name === 'ai_provider') {
            const provider = availableProviders.find(p => p.name === value) || null
            setSelectedProvider(provider)
            setFormData(prev => ({
                ...prev,
                ai_provider: value,
                ai_model: provider ? provider.default_model : ''
            }))
        } else {
            setFormData((prev: FormData) => ({
                ...prev,
                [name]: value
            }))
        }
    }

    return (
        <form onSubmit={handleSubmit} className="ad-copy-form">
            <div className="form-group select-group">
                <div className="select-item">
                    <label htmlFor="ai_provider">AI 제공자</label>
                    <select
                        id="ai_provider"
                        name="ai_provider"
                        value={formData.ai_provider}
                        onChange={handleChange}
                        disabled={loading || !!fixedProvider}
                    >
                        {availableProviders.map(p => (
                            <option key={p.name} value={p.name}>
                                {p.name.toUpperCase()} {p.free ? '(무료)' : ''}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="select-item">
                    <label htmlFor="ai_model">AI 모델</label>
                    <select
                        id="ai_model"
                        name="ai_model"
                        value={formData.ai_model}
                        onChange={handleChange}
                        disabled={loading || !selectedProvider || !!fixedModel}
                    >
                        {selectedProvider?.models.map(m => (
                            <option key={m} value={m}>
                                {m}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="form-group">
                <label htmlFor="product_name">제품명 *</label>
                <input
                    type="text"
                    id="product_name"
                    name="product_name"
                    value={formData.product_name}
                    onChange={handleChange}
                    required
                    placeholder="예: 수제 햄버거"
                    disabled={loading}
                />
            </div>

            <div className="form-group">
                <label htmlFor="category">카테고리 *</label>
                <input
                    type="text"
                    id="category"
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    required
                    placeholder="예: 음식점"
                    disabled={loading}
                />
            </div>

            <div className="form-group">
                <label htmlFor="target_audience">타겟 고객 *</label>
                <input
                    type="text"
                    id="target_audience"
                    name="target_audience"
                    value={formData.target_audience}
                    onChange={handleChange}
                    required
                    placeholder="예: 20-30대 직장인"
                    disabled={loading}
                />
            </div>

            <div className="form-group">
                <label htmlFor="key_features">핵심 특징 *</label>
                <textarea
                    id="key_features"
                    name="key_features"
                    value={formData.key_features}
                    onChange={handleChange}
                    required
                    placeholder="예: 100% 국내산 소고기, 수제 패티, 신선한 야채"
                    rows={4}
                    disabled={loading}
                />
            </div>

            <div className="form-group">
                <label htmlFor="tone">톤 *</label>
                <select
                    id="tone"
                    name="tone"
                    value={formData.tone}
                    onChange={handleChange}
                    required
                    disabled={loading}
                >
                    <option value="friendly">친근한</option>
                    <option value="professional">전문적인</option>
                    <option value="humorous">유머러스한</option>
                </select>
            </div>

            <button type="submit" className="submit-button" disabled={loading}>
                {loading ? '생성 중...' : '광고 문구 생성하기'}
            </button>
        </form>
    )
}
