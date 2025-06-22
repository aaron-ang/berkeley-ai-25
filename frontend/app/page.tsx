export default function Home() {
  return (
    <div 
      className="min-h-screen relative"
      style={{
        background: 'radial-gradient(ellipse at center, #6B46C1 0%, #3B82F6 100%)',
        backgroundSize: '100% 100%'
      }}
    >
      {/* Navigation */}
      <nav className="absolute top-0 left-0 right-0 p-6 z-10">
        <div className="flex justify-between items-center">
          <h1 className="text-white text-lg font-medium">Landing Page</h1>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex flex-col items-center justify-center min-h-screen px-6 text-center">
        {/* Logo Circle with exact specifications */}
        <div className="relative mb-16">
          <div className="glass-circle relative flex items-center justify-center">
            {/* Logo placeholder - easy to replace with an image */}
            <div className="logo-container flex items-center justify-center w-full h-full">
              <span className="text-white text-2xl font-light">logo goes here</span>
              {/* To replace with an image later, simply replace the span above with:
                  <img src="/your-logo.png" alt="Logo" className="w-auto h-auto max-w-[80%] max-h-[80%] object-contain" />
              */}
            </div>
          </div>
        </div>

        {/* Description Text */}
        <p className="text-white/80 text-lg leading-relaxed max-w-4xl mb-16 font-light">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
          ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
          ullamco laboris nisi ut aliquip ex ea commodo consequat.
        </p>

        {/* Search Input with exact specifications */}
        <div className="relative">
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
              placeholder="Paste your issue link here"
              className="w-full h-full pl-16 pr-6 text-white placeholder-gray-300 bg-transparent border-none outline-none relative z-10"
              style={{ fontSize: '16px' }}
            />
          </div>
        </div>
      </main>
    </div>
  )
}