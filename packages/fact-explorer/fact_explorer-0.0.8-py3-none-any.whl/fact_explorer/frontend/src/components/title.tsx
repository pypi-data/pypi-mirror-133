import { FC } from 'react';

export const Title: FC = ({ children }) => {
  return (
    <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 pt-10 pb-5">
      {children}
    </h1>
  );
};
