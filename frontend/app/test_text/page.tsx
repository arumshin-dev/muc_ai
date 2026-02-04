// frontend/app/test_text/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

interface Model {
  id: string;
  name: string;
}

interface Provider {
  id: string;
  name: string;
  models: Model[];
}

export default function TestTextPage() {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [selectedProvider, setSelectedProvider] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [prompt, setPrompt] = useState('Python Factory Pattern을 한줄로 설명해줘');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [responseTime, setResponseTime] = useState(0);

  useEffect(() => {
    // 프로바이더 목록 로드
    const fetchProviders = async () => {
      try {
        const data = await apiClient.get<{ providers: Provider[] }>('/api/text/providers');
        setProviders(data.providers);
        if (data.providers.length > 0) {
          setSelectedProvider(data.providers[0].id);
          setSelectedModel(data.providers[0].models[0].id);
        }
      } catch (err) {
        console.error('Failed to load providers:', err);
      }
    };
    fetchProviders();
  }, []);

  const handleTest = async (provider?: string, model?: string) => {
    setLoading(true);
    setResult('');
    const startTime = Date.now();

    try {
      const data = await apiClient.post<{ text: string }>('/api/text/generate', {
          provider: provider || selectedProvider,
          model: model || selectedModel,
          prompt: prompt
      });

      const endTime = Date.now();
      setResult(data.text);
      setResponseTime(endTime - startTime);
    } catch (error) {
      setResult(`❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const currentProviderData = providers.find(p => p.id === selectedProvider);

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <h1 className="text-3xl font-bold mb-6">🤖 AI 텍스트 생성 테스트</h1>

      {/* 입력 영역 */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <label className="block mb-2 font-semibold">프롬프트:</label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="w-full border rounded p-3 mb-4"
          rows={3}
          placeholder="테스트할 프롬프트를 입력하세요"
        />

        {/* 프로바이더 선택 */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block mb-2 font-semibold">프로바이더:</label>
            <select
              value={selectedProvider}
              onChange={(e) => {
                setSelectedProvider(e.target.value);
                const provider = providers.find(p => p.id === e.target.value);
                if (provider?.models[0]) {
                  setSelectedModel(provider.models[0].id);
                }
              }}
              className="w-full border rounded p-2"
            >
              {providers.map((p, idx) => (
                <option key={`${p.id}-${idx}`} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-2 font-semibold">모델:</label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full border rounded p-2"
            >
              {currentProviderData?.models.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button
          onClick={() => handleTest()}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? '⏳ 생성 중...' : '🚀 테스트 실행'}
        </button>
      </div>

      {/* 결과 영역 */}
      {result && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-xl font-semibold">📝 결과</h3>
            <span className="text-sm text-gray-600">⏱️ {responseTime}ms</span>
          </div>
          <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded">
            {result}
          </pre>
        </div>
      )}

      {/* 빠른 테스트 버튼 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold mb-4">⚡ 빠른 비교 테스트</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {providers.map((provider, idx) =>
            provider.models.map((model, midx) => (
              <button
                key={`${idx}-${midx}`}
                onClick={() => handleTest(provider.id, model.id)}
                disabled={loading}
                className="border-2 border-blue-500 text-blue-600 px-4 py-3 rounded hover:bg-blue-50 disabled:opacity-50 transition"
              >
                <div className="font-semibold text-sm">{provider.name}</div>
                <div className="text-xs text-gray-600">{model.name}</div>
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
