import Head from 'next/head';
import { useRouter } from 'next/router';
import {
  Component,
  ErrorInfo,
  FC,
  ReactNode,
  useEffect,
  useState,
} from 'react';
import { Card } from './card';
import { Title } from './title';

type RealErrorBoundaryProps = {
  children?: ReactNode;
  path: string;
  setErrorPath: (value: string | null) => void;
};

type State = { error: unknown };

class RealErrorBoundary extends Component<RealErrorBoundaryProps, State> {
  state: State = { error: undefined };

  static getDerivedStateFromError(error: unknown) {
    return { error };
  }

  componentDidCatch(error: unknown, errorInfo: ErrorInfo) {
    this.props.setErrorPath(this.props.path);
  }

  render() {
    const { error } = this.state;

    if (error === undefined) return this.props.children;

    return (
      <>
        <Head>
          <title>Unknown Error</title>
        </Head>

        <Title>Unknown Error</Title>

        <Card>
          <p className="p-5">We&apos;re sorry. An unknown error happened.</p>
        </Card>
      </>
    );
  }
}

export const ErrorBoundary: FC = ({ children }) => {
  const [key, setKey] = useState(0);
  const { asPath } = useRouter();
  const [errorPath, setErrorPath] = useState<string | null>(null);

  useEffect(() => {
    if (errorPath !== null) {
      // unmount the error boundary on location change after an error happened to reset error state
      if (errorPath !== asPath) {
        setErrorPath(null);
        setKey((key) => key + 1);
      }
    }
  }, [asPath, errorPath]);

  return (
    <RealErrorBoundary key={key} path={asPath} setErrorPath={setErrorPath}>
      {children}
    </RealErrorBoundary>
  );
};
