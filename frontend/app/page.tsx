'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const [githubUrl, setGithubUrl] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!githubUrl.trim()) {
      setError('Please enter a GitHub issue URL');
      return;
    }

    setError(null);

    // Store the URL
    localStorage.setItem('pendingGithubUrl', githubUrl);
    // Small delay to ensure localStorage is set
    await new Promise(resolve => setTimeout(resolve, 50));
    router.push('/issues');
  };

  return (
    <div className="relative min-h-screen">
      {/* Black background layer (100% opacity) */}
      <div className="absolute inset-0 bg-black z-0" />

      {/* Background image layer (90% opacity) */}
      <div
        className="absolute inset-0 z-9"
        style={{
          backgroundImage: 'url("/purpleBackground.png")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          opacity: 0.9,
        }}
      />

      {/* Main Content */}
      <main className="flex flex-col items-center justify-center min-h-screen px-6 text-center">
        {/* Logo Circle with exact specifications */}
        <div className="relative mb-10">
          <div className="glass-circle relative flex items-center justify-center">
            {/* Logo placeholder - easy to replace with an image */}
            <div className="logo-container flex items-center justify-center w-full h-full">
              <img src="/logo.png" alt="Logo" className="w-auto h-auto max-w-[80%] max-h-[80%] object-contain" />
            </div>
          </div>
        </div>

        {/* Description Text */}
        <p className="text-white/80 text-lg leading-relaxed max-w-4xl mb-10 font-light z-10">
          Analyze GitHub issues with AI-powered insights. Paste a GitHub issue URL below to get detailed analysis and relevant files.
        </p>

        {/* Error Display */}
        {error && (
          <div className="max-w-2xl mx-auto mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg text-red-200 relative z-10">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Search Input with exact specifications */}
        <form onSubmit={handleSubmit} className="relative mb-10">
          <div className="glass-search relative flex items-center">
            <div className="absolute left-6 flex items-center pointer-events-none z-10">
              <svg
                className="w-6 h-6 text-gray-300"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <input
              type="text"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              placeholder="Paste your GitHub issue URL here"
              className="w-full h-full pl-16 pr-6 text-white placeholder-gray-300 bg-transparent border-none outline-none relative z-10"
              style={{ fontSize: '18px' }}
            />
          </div>
          <button
            type="submit"
            className="mt-4 px-8 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded-full transition-colors duration-200"
          >
            Analyze Issue
          </button>
        </form>

      </main>
    </div>
  );
}