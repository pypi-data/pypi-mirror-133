import { useCallback, useEffect, useRef, useState } from 'react';

export function useFetch<T>() {
  const [state, setState] = useState<{ loading: boolean; data: T | null }>({
    loading: false,
    data: null,
  });

  const [error, setError] = useState<unknown>(null);

  const abortRef = useRef<AbortController>();
  const pendingAbortRef = useRef<AbortController>();

  useEffect(() => {
    if (error === null) return;
    throw error;
  }, [error]);

  useEffect(() => {
    return () => abortRef.current?.abort();
  }, []);

  const execute = useCallback(
    async (input: RequestInfo, init: RequestInit = {}) => {
      const controller = new AbortController();
      const signal = controller.signal;

      if (abortRef.current) {
        abortRef.current.abort();
        pendingAbortRef.current = abortRef.current;
      }
      abortRef.current = controller;

      setState((state) => ({ ...state, loading: true }));
      try {
        const res = await fetch(input, { signal, ...init });
        if (res.ok) {
          const data = await res.json();
          abortRef.current = undefined;
          setState(() => ({ data, loading: false }));
        } else {
          throw await res.json();
        }
      } catch (err) {
        if (err instanceof DOMException && err.name === 'AbortError') {
          if (pendingAbortRef.current) {
            // do nothing as this request was aborted, because of a newer one
            pendingAbortRef.current = undefined;
          } else {
            abortRef.current = undefined;
            setState((state) => ({ ...state, loading: false }));
          }
        } else {
          abortRef.current = undefined;
          setState((state) => ({ ...state, loading: false }));
          setError(err);
        }
      }
    },
    []
  );

  return { ...state, execute };
}
