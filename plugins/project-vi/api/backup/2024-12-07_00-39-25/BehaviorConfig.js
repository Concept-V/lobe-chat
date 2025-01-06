import React from 'react';
import { Settings, Zap, Bell, Clock } from 'lucide-react';

const BehaviorConfig = ({ config, onChange }) => {
  const startupOptions = [
    {
      id: 'minimized',
      name: 'Start Minimized',
      description: 'Launch in system tray'
    },
    {
      id: 'normal',
      name: 'Normal Window',
      description: 'Launch as regular window'
    },
    {
      id: 'restore',
      name: 'Restore Previous',
      description: 'Remember last window state'
    }
  ];

  const performanceProfiles = [
    {
      id: 'balanced',
      name: 'Balanced',
      description: 'Optimal performance and resource usage',
      settings: {
        cacheSize: '512MB',
        backgroundProcessing: true,
        prefetch: 'moderate'
      }
    },
    {
      id: 'performance',
      name: 'High Performance',
      description: 'Maximum responsiveness',
      settings: {
        cacheSize: '1GB',
        backgroundProcessing: true,
        prefetch: 'aggressive'
      }
    },
    {
      id: 'efficiency',
      name: 'Power Efficient',
      description: 'Minimal resource usage',
      settings: {
        cacheSize: '256MB',
        backgroundProcessing: false,
        prefetch: 'minimal'
      }
    }
  ];

  return (
    <div className="space-y-8">
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Startup Behavior</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {startupOptions.map((option) => (
            <div
              key={option.id}
              onClick={() => onChange('startupMode', option.id)}
              className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                config.startupMode === option.id 
                  ? 'border-purple-500 bg-purple-50' 
                  : 'hover:border-purple-300'
              }`}
            >
              <h4 className="font-medium text-gray-900">{option.name}</h4>
              <p className="text-sm text-gray-500 mt-1">{option.description}</p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Performance Profile</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {performanceProfiles.map((profile) => (
            <div
              key={profile.id}
              onClick={() => onChange('performanceProfile', profile.id)}
              className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                config.performanceProfile === profile.id 
                  ? 'border-purple-500 bg-purple-50' 
                  : 'hover:border-purple-300'
              }`}
            >
              <div className="flex items-center space-x-3 mb-3">
                <Zap className="w-5 h-5 text-purple-600" />
                <div>
                  <h4 className="font-medium text-gray-900">{profile.name}</h4>
                  <p className="text-sm text-gray-500">{profile.description}</p>
                </div>
              </div>
              {config.performanceProfile === profile.id && (
                <div className="mt-2 pt-2 border-t border-purple-200">
                  <ul className="text-xs text-purple-700 space-y-1">
                    <li>• Cache: {profile.settings.cacheSize}</li>
                    <li>• Background: {profile.settings.backgroundProcessing ? 'Enabled' : 'Disabled'}</li>
                    <li>• Prefetch: {profile.settings.prefetch}</li>
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Notifications</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">System Notifications</h4>
              <p className="text-sm text-gray-500">Show desktop notifications</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={config.systemNotifications || false}
                onChange={(e) => onChange('systemNotifications', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">Sound Effects</h4>
              <p className="text-sm text-gray-500">Play notification sounds</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={config.soundEffects || false}
                onChange={(e) => onChange('soundEffects', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
            </label>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">System Integration</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">Start with Windows</h4>
              <p className="text-sm text-gray-500">Launch on system startup</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={config.autoStart || false}
                onChange={(e) => onChange('autoStart', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">System Tray</h4>
              <p className="text-sm text-gray-500">Show in system tray when minimized</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={config.systemTray || false}
                onChange={(e) => onChange('systemTray', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BehaviorConfig;