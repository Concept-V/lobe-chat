import React from 'react';
import { useTheme } from '../contexts';

const Button = ({ 
  children, 
  variant = 'primary', 
  icon: Icon,
  className = '',
  ...props 
}) => {
  const { styles } = useTheme();

  const getVariantStyles = () => {
    switch (variant) {
      case 'primary':
        return styles.buttonPrimary;
      case 'secondary':
        return styles.buttonSecondary;
      case 'icon':
        return 'p-2 rounded-full hover:bg-concept-brown-dark/20';
      default:
        return styles.buttonPrimary;
    }
  };

  return (
    <button
      className={`${getVariantStyles()} ${className} flex items-center space-x-2`}
      {...props}
    >
      {Icon && <Icon className={variant === 'icon' ? 'w-5 h-5' : 'w-4 h-4'} />}
      {children && <span>{children}</span>}
    </button>
  );
};

export default Button;