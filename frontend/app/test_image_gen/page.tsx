'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api';
import { API_ENDPOINTS } from '@/lib/config';

interface ImageProvider {
  name: string;
  models: string[];
  default_model: string;
  free: boolean;
  sizes: string[];
  qualities?: string[];
}

export default function TestImageGenPage() {
  const [providers, setProviders] = useState<ImageProvider[]>([]);
  const [selectedProvider, setSelectedProvider] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [prompt, setPrompt] = useState('A serene landscape with mountains and a lake at sunset');
  const [size, setSize] = useState('1024x1024');
  const [quality, setQuality] = useState('low');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [responseTime, setResponseTime] = useState(0);

  useEffect(() => {
    const fetchProviders = async () => {
      try {
        const data = await apiClient.get<{ providers: ImageProvider[] }>(
          API_ENDPOINTS.image.providers
        );
        setProviders(data.providers);
        if (data.providers.length > 0) {
          setSelectedProvider(data.providers[0].name);
          setSelectedModel(data.providers[0].default_model);
        }
      } catch (err) {
        console.error('Failed to load providers:', err);
      }
    };
    fetchProviders();
  }, []);

  const handleGenerate = async () => {
    setLoading(true);
    setImageUrl('');
    const startTime = Date.now();

    try {
      // 이미지를 Blob으로 받기
      const blob = await apiClient.post(
        API_ENDPOINTS.image.generate,
        {
          provider: selectedProvider,
          model: selectedModel,
          prompt,
          size,
          quality
        },
        { responseType: 'blob' }
      );

      const endTime = Date.now();
      setResponseTime(endTime - startTime);
      
      // Blob을 URL로 변환
      const url = URL.createObjectURL(blob);
      setImageUrl(url);
    } catch (error) {
      console.error('Generation failed:', error);
      alert(`❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const currentProvider = providers.find(p => p.name === selectedProvider);

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <h1 className="text-3xl font-bold mb-6">🎨 AI 이미지 생성 테스트</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 왼쪽: 설정 */}
        <div className="space-y-4">
          <div>
            <label className="block font-semibold mb-2">Provider</label>
            <select
              value={selectedProvider}
              onChange={(e) => {
                setSelectedProvider(e.target.value);
                const provider = providers.find(p => p.name === e.target.value);
                if (provider) setSelectedModel(provider.default_model);
              }}
              className="w-full border rounded p-2"
            >
              {providers.map(p => (
                <option key={p.name} value={p.name}>
                  {p.name} {p.free && '(무료)'}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block font-semibold mb-2">Model</label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full border rounded p-2"
            >
              {currentProvider?.models.map(m => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block font-semibold mb-2">Prompt</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full border rounded p-2 h-24"
              placeholder="Describe the image you want..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold mb-2">Size</label>
              <select
                value={size}
                onChange={(e) => setSize(e.target.value)}
                className="w-full border rounded p-2"
              >
                {currentProvider?.sizes.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            {currentProvider?.qualities && (
              <div>
                <label className="block font-semibold mb-2">Quality</label>
                <select
                  value={quality}
                  onChange={(e) => setQuality(e.target.value)}
                  className="w-full border rounded p-2"
                >
                  {currentProvider.qualities.map(q => (
                    <option key={q} value={q}>{q}</option>
                  ))}
                </select>
              </div>
            )}
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !prompt}
            className="w-full bg-blue-600 text-white py-3 rounded font-semibold hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? '⏳ Generating...' : '✨ Generate Image'}
          </button>

          {responseTime > 0 && (
            <div className="text-sm text-gray-600">
              ⚡ Response time: {(responseTime / 1000).toFixed(2)}s
            </div>
          )}
        </div>

        {/* 오른쪽: 결과 */}
        <div className="border rounded-lg p-4 bg-gray-50 flex items-center justify-center min-h-[500px]">
          {loading ? (
            <div className="text-center">
              <div className="animate-spin text-4xl mb-2">⏳</div>
              <p>Generating image...</p>
            </div>
          ) : imageUrl ? (
            <div>
              <img
                src={imageUrl}
                alt="Generated"
                className="max-w-full rounded-lg shadow-lg"
              />
              <a
                href={imageUrl}
                download="generated_image.png"
                className="block mt-4 text-center bg-green-600 text-white py-2 rounded hover:bg-green-700"
              >
                💾 Download
              </a>
            </div>
          ) : (
            <p className="text-gray-400">이미지가 여기에 표시됩니다</p>
          )}
        </div>
      </div>
    </div>
  );
}
