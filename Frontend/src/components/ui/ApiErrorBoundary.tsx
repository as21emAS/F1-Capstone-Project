import React from 'react';

interface ApiErrorBoundaryProps {
  children: React.ReactNode;
  fallbackMessage?: string;
}

interface ApiErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ApiErrorBoundary extends React.Component<
  ApiErrorBoundaryProps,
  ApiErrorBoundaryState
> {
  constructor(props: ApiErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ApiErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('[ApiErrorBoundary] Caught error:', error, info);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (!this.state.hasError) {
      return this.props.children;
    }

    const { fallbackMessage = 'Something went wrong.' } = this.props;
    const isDev = import.meta.env.DEV;

    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center px-6">
        <div className="w-full max-w-lg">
          {/* DNF Panel */}
          <div className="relative border border-[#e10600]/30 bg-[#0d0d0d] overflow-hidden">
            {/* Top red accent bar */}
            <div className="h-1 w-full bg-[#e10600]" />

            {/* Checkered flag corner watermark */}
            <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden pointer-events-none">
              <svg viewBox="0 0 64 64" className="w-full h-full">
                {Array.from({ length: 8 }).map((_, row) =>
                  Array.from({ length: 8 }).map((_, col) => (
                    <rect
                      key={`${row}-${col}`}
                      x={col * 8}
                      y={row * 8}
                      width={8}
                      height={8}
                      fill={(row + col) % 2 === 0 ? 'white' : 'transparent'}
                    />
                  ))
                )}
              </svg>
            </div>

            <div className="p-8 flex flex-col gap-6">
              {/* DNF badge */}
              <div className="flex items-center gap-4">
                <div className="flex items-center justify-center w-16 h-16 border-2 border-[#e10600] bg-[#1a0000]">
                  <span className="text-[#e10600] text-xl font-black tracking-tighter font-mono">
                    DNF
                  </span>
                </div>
                <div className="flex flex-col gap-0.5">
                  <span className="text-[10px] text-[#555] tracking-[0.25em] uppercase font-mono">
                    Race Status
                  </span>
                  <span className="text-[#e10600] text-sm tracking-[0.15em] uppercase font-mono font-bold">
                    Did Not Finish
                  </span>
                </div>
              </div>

              {/* Divider with sector styling */}
              <div className="flex items-center gap-2">
                <div className="w-6 h-px bg-[#e10600]" />
                <div className="flex-1 h-px bg-[#1a1a1a]" />
              </div>

              {/* Error message */}
              <div className="flex flex-col gap-2">
                <p className="text-[#aaa] text-sm font-mono leading-relaxed">
                  {fallbackMessage}
                </p>
                <p className="text-[#555] text-xs font-mono">
                  The application encountered an unexpected failure. Check your connection or try reloading.
                </p>
              </div>

              {/* Dev error detail */}
              {isDev && this.state.error && (
                <div className="border border-[#1e1e1e] bg-[#080808] rounded-sm p-3 overflow-auto max-h-32">
                  <span className="text-[9px] text-[#555] tracking-widest uppercase font-mono block mb-1">
                    Dev Mode — Error Detail
                  </span>
                  <code className="text-[#e10600] text-[11px] font-mono whitespace-pre-wrap break-all leading-relaxed">
                    {this.state.error.message}
                    {this.state.error.stack && (
                      <>
                        {'\n\n'}
                        <span className="text-[#444]">{this.state.error.stack}</span>
                      </>
                    )}
                  </code>
                </div>
              )}

              {/* Action row */}
              <div className="flex items-center gap-3 pt-1">
                <button
                  onClick={this.handleRetry}
                  className="flex items-center gap-2 px-5 py-2.5 bg-[#e10600] hover:bg-[#ff1a0f] text-white text-xs font-bold tracking-[0.15em] uppercase font-mono transition-colors duration-150 focus:outline-none focus:ring-1 focus:ring-[#e10600] focus:ring-offset-1 focus:ring-offset-[#0d0d0d]"
                >
                  {/* Retry icon — right arrow */}
                  <svg className="w-3 h-3" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M1 6a5 5 0 1 0 5-5" strokeLinecap="round" />
                    <path d="M1 2v4h4" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  Retry
                </button>

                <a
                  href="/"
                  className="px-5 py-2.5 border border-[#2a2a2a] hover:border-[#444] text-[#555] hover:text-[#aaa] text-xs font-mono tracking-[0.15em] uppercase transition-colors duration-150"
                >
                  Go to Dashboard
                </a>
              </div>
            </div>

            {/* Bottom telemetry strip */}
            <div className="border-t border-[#1a1a1a] px-8 py-2 flex justify-between items-center">
              <span className="text-[9px] text-[#333] tracking-[0.2em] uppercase font-mono">
                Error Boundary
              </span>
              <span className="text-[9px] text-[#333] tracking-[0.2em] uppercase font-mono">
                F1 Race Predictor
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
