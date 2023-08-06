import { useCallback, useMemo, useState } from 'react';

export function useSubmit() {
  const [wiggle, setWiggle] = useState<'animate-wiggle' | ''>('');

  const props = useMemo(
    () => ({
      type: 'submit' as const,
      className: `${wiggle} border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 p-2`,
      onAnimationEnd: () => setWiggle(''),
    }),
    [wiggle]
  );

  const onError = useCallback(() => setWiggle('animate-wiggle'), []);

  return { props, onError };
}
