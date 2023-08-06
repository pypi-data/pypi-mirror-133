import { FC } from 'react';

export const Form: FC<{ onSubmit: () => void }> = ({ children, onSubmit }) => {
  return (
    <form className="grid gap-2 p-5" onSubmit={onSubmit} noValidate>
      {children}
    </form>
  );
};
