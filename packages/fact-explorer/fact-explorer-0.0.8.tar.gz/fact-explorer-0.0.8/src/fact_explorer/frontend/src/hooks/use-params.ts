import { useRouter } from 'next/router';
import * as queryString from 'query-string';
import { useMemo } from 'react';

export function useParams<T extends object>(initialValues: T) {
  const router = useRouter();
  const query = router.asPath.split('?')[1];

  const params = useMemo(() => {
    const parsedValues = queryString.parse(query, {
      parseBooleans: true,
      parseNumbers: true,
    });
    const params = {} as T;
    Object.keys(initialValues).forEach((key) => {
      params[key as keyof T] =
        (parsedValues[key] as any) ?? initialValues[key as keyof T];
    });
    return params;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query]);

  return params;
}
