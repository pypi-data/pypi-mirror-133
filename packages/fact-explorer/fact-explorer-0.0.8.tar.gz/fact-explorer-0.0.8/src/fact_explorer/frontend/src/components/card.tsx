import { FC } from 'react';

export const Card: FC = ({ children }) => {
  return (
    <div className={`bg-white rounded-xl shadow-lg divide-y`}>{children}</div>
  );
};
