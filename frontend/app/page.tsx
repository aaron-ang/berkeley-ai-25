'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { analyzeGitHubIssue } from "../lib/api";

export default function Home() {
  const router = useRouter();
  const [githubUrl, setGithubUrl] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!githubUrl.trim()) {
      setError('Please enter a GitHub issue URL');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const result = await analyzeGitHubIssue(githubUrl);

      // Store the analysis data in localStorage for the issues page
      localStorage.setItem('analysisData', JSON.stringify({
        analysis: result.analysis,
        flattenedFiles: result.flattenedFiles
      }));

      // Navigate to issues page
      router.push('/issues');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      setLoading(false);
    }
  };

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen relative flex items-center justify-center">
        <div className="absolute inset-0 bg-black z-0" />
        <div
          className="absolute inset-0 z-9"
          style={{
            backgroundImage: 'url("/purpleBackground2.png")',
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            opacity: 0.9,
          }}
        />
        <div className="relative z-10 text-center">
          <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-white text-xl">Analyzing GitHub issue...</p>
          <p className="text-white/60 text-sm mt-2">This may take a few moments</p>
        </div>
      </div>
    );
  }

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
            <button
              onClick={() => setError(null)}
              className="ml-4 px-3 py-1 bg-red-600/30 hover:bg-red-600/50 rounded text-sm transition-colors"
            >
              Dismiss
            </button>
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
              disabled={loading}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="mt-4 px-8 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded-full transition-colors duration-200"
          >
            {loading ? 'Analyzing...' : 'Analyze Issue'}
          </button>
        </form>

        <style jsx global>{`
          .glass-circle {
            width: 200px;
            height: 200px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50%;
          }
          
          .glass-search {
            width: 600px;
            height: 80px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 40px;
            position: relative;
          }
        `}</style>
      </main>
    </div>
  );
}