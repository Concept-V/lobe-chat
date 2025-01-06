import React from 'react';
import { Settings } from 'lucide-react';
import MemoryConfig from '../MemoryConfig';

const PowerUpConfig = ({ powerUp }) => {
  const renderConfig = () => {
    switch (powerUp.id) {
      case 'memory':
        return <MemoryConfig />;
      default:
        return (
          <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
            <p className="text-sm text-yellow-800">
              Configuration options for {powerUp.name} will appear here.
            </p>
          </div>
        );
    }
  };

  return (
    <div className="border rounded-lg p-4">
      <div className="flex items-center space-x-2 mb-4">
        <Settings className="w-5 h-5 text-blue-600" />
        <h3 className="text-lg font-medium">{powerUp.name} Configuration</h3>
      </div>
      
      <div className="space-y-4">
        {renderConfig()}
      </div>
    </div>
  );
};

export default PowerUpConfig;