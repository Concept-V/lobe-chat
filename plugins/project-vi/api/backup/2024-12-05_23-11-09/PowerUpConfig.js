import React from 'react';
import { Settings } from 'lucide-react';
import MemoryConfig from '../MemoryConfig';
import FileSystemConfig from '../FileSystemConfig';
import DesktopConfig from '../DesktopConfig';

const PowerUpConfig = ({ powerUp }) => {
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
          <div className="bg-conceptv-bg-alt border border-conceptv-yellow-sepia rounded p-3">
            <p className="text-sm text-conceptv-brown-dark">
              Configuration options for {powerUp.name} will appear here.
            </p>
          </div>
        );
    }
  };

  return (
    <div className="border border-conceptv-brown-light rounded-lg p-4">
      <div className="flex items-center space-x-2 mb-4">
        <Settings className="w-5 h-5 text-conceptv-brown" />
        <h3 className="text-lg font-medium text-conceptv-brown-dark">{powerUp.name} Configuration</h3>
      </div>
      
      <div className="space-y-4">
        {renderConfig()}
      </div>
    </div>
  );
};

export default PowerUpConfig;