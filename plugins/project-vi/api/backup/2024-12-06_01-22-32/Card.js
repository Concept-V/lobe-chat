import React from 'react';
import { useTheme } from '../contexts';

const Card = ({ 
  children, 
  selected = false,
  className = '',
  ...props 
}) => {
  const { styles } = useTheme();

  return (
    <div
      className={`
        ${styles.card}
        ${selected ? styles.cardSelected : styles.cardHover}
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;