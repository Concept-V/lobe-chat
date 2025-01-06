import React from 'react';
import { Settings } from 'lucide-react';
import { useTheme } from '../../theme/ThemeContext';
import MemoryConfig from '../MemoryConfig';
import FileSystemConfig from '../FileSystemConfig';
import DesktopConfig from '../DesktopConfig';

const PowerUpConfig = ({ powerUp }) => {
  const { styles } = useTheme();

  const renderConfig = () => {
    switch (powerUp.id) {
      case 'memory':
        return <MemoryConfig />;
      case 'filesystem':
        return <FileSystemConfig />;
      case 'desktop':
        return <DesktopConfig />;
      default:
        return (
          <div className={`${styles.card} ${styles.cardHover} bg-concept-brown-dark/10`}>
            <p className={styles.text}>
              Configuration options for {powerUp.name} will appear here.
            </p>
          </div>
        );
    }
  };

  return (
    <div className={styles.container}>
      <div className={`flex items-center space-x-2 mb-4 p-4 ${styles.section}`}>
        <Settings className={styles.icon} />
        <h3 className={styles.heading}>{powerUp.name} Configuration</h3>
      </div>
      
      <div className="p-4">
        {renderConfig()}
      </div>
    </div>
  );
};

export default PowerUpConfig;