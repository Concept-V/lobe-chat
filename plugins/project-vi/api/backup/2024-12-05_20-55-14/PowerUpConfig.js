import React from 'react';
import { Settings, Save } from 'lucide-react';

const PowerUpConfig = ({ powerUp }) => {
  return (
    <div className="border rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Settings className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-medium">{powerUp.name} Configuration</h3>
        </div>
        <button className="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center space-x-2">
          <Save className="w-4 h-4" />
          <span>Save</span>
        </button>
      </div>
      
      <div className="space-y-4">
        {/* Dynamic configuration fields will go here */}
        <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
          <p className="text-sm text-yellow-800">
            Configuration options for {powerUp.name} will appear here.
          </p>
        </div>
      </div>
    </div>
  );
};

export default PowerUpConfig;