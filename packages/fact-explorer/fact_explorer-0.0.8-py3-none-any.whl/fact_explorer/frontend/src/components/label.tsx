import { FC } from 'react';

export const Label: FC<{ htmlFor?: string; onClick?: () => void }> = ({
  children,
  htmlFor,
  onClick,
}) => {
  return (
    <label
      htmlFor={htmlFor}
      onClick={onClick}
      className="block font-medium text-gray-700"
    >
      {children}
    </label>
  );
};
