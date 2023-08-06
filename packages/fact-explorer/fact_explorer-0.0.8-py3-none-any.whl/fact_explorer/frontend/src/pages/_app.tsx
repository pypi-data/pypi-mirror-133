import '../styles/globals.css';
import type { AppProps } from 'next/app';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { ErrorBoundary } from '../components/error-boundary';

// register monaco extensions once, but only on browser side
if (process.browser) import('../utils/init-monaco');

function MyApp({ Component, pageProps }: AppProps) {
  const router = useRouter();
  return (
    <div className="container mx-auto py-4 ">
      <header className="grid grid-flow-col gap-1 justify-between">
        <div className="grid grid-flow-col gap-1 items-center">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/favicon.png"
            width="50"
            height="14"
            alt="Fact Explorer Logo"
          />
          <strong>Fact Explorer</strong>
        </div>

        <div className="grid grid-flow-col gap-5 items-center">
          <Link href="/">
            <a
              className={
                router.pathname === '/' ? 'underline underline-offset-2' : ''
              }
            >
              Last Minutes
            </a>
          </Link>
          <span className="text-gray-200">|</span>
          <Link href="/search">
            <a
              className={
                router.pathname === '/search'
                  ? 'underline underline-offset-2'
                  : ''
              }
            >
              Search
            </a>
          </Link>
          <span className="text-gray-200">|</span>
          <a href="/docs" target="_blank">
            API Docs
          </a>
        </div>
      </header>

      <main className="container mx-auto py-4">
        <ErrorBoundary>
          <Component {...pageProps} />
        </ErrorBoundary>
      </main>
    </div>
  );
}

export default MyApp;
