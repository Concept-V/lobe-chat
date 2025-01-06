import React, { useState } from 'react';
import { Brain, Settings, Database, Network, Shield } from 'lucide-react';
import { useTheme } from '../../shared/contexts';
import { Card, Button } from '../../shared/components';
import BasicSetup from './components/BasicSetup';
import AdvancedSettings from './components/AdvancedSettings';
import MonitoringPanel from './components/MonitoringPanel';

const MemoryConfig = () => {
  const { styles } = useTheme();
  const [activeView, setActiveView] = useState('basic');
  const [config, setConfig] = useState({
    memoryProfile: null,
    memorySettings: null,
    showAdvanced: false,
    monitoring: {
      enabled: false,
      interval: '1m',
      metrics: ['usage', 'performance', 'health']
    }
  });

  const views = [
    { id: 'basic', name: 'Basic Setup', icon: Brain },
    { id: 'advanced', name: 'Advanced Settings', icon: Settings },
    { id: 'storage', name: 'Storage Management', icon: Database },
    { id: 'graph', name: 'Knowledge Graph', icon: Network },
    { id: 'monitoring', name: 'System Monitor', icon: Shield }
  ];

  const handleConfigChange = (key, value) => {
    setConfig(prev => ({
      ...prev,
      [key]: value
    }));

    // If selecting a memory profile, show advanced settings button
    if (key === 'memoryProfile') {
      setConfig(prev => ({
        ...prev,
        showAdvanced: true
      }));
    }
  };

  const renderContent = () => {
    switch (activeView) {
      case 'basic':
        return <BasicSetup config={config} onChange={handleConfigChange} />;
      case 'advanced':
        return <AdvancedSettings config={config} onChange={handleConfigChange} />;
      case 'monitoring':
        return <MonitoringPanel config={config} onChange={handleConfigChange} />;
      // Add other views as they're implemented
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Brain className={`w-8 h-8 ${styles.icon}`} />
          <div>
            <h2 className={`text-xl font-semibold ${styles.heading}`}>Memory System</h2>
            <p className={styles.text}>Configure Vi's knowledge and memory capabilities</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <Button
            variant="secondary"
            icon={Shield}
            onClick={() => setActiveView('monitoring')}
          >
            Monitor
          </Button>
          {config.memoryProfile && (
            <Button
              variant="primary"
              icon={Settings}
              onClick={() => setActiveView('advanced')}
            >
              Advanced Settings
            </Button>
          )}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex space-x-2 border-b border-concept-brown-dark/20">
        {views.map(view => (
          <Button
            key={view.id}
            variant="nav"
            onClick={() => setActiveView(view.id)}
            className={activeView === view.id ? styles.navButtonActive : styles.navButton}
          >
            <view.icon className="w-4 h-4 mr-2" />
            {view.name}
          </Button>
        ))}
      </div>

      {/* Main Content */}
      <div className="min-h-[400px]">
        {renderContent()}
      </div>

      {/* Status Panel */}
      {config.memoryProfile && (
        <Card className="mt-6 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className={`w-3 h-3 rounded-full ${
                config.monitoring?.enabled ? 'bg-green-500' : 'bg-yellow-500'
              }`} />
              <span className={styles.text}>
                Memory System Status: {config.monitoring?.enabled ? 'Active' : 'Standby'}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span className={`${styles.text} text-sm`}>
                Profile: {config.memoryProfile}
              </span>
              <span className={`${styles.text} text-sm`}>
                Size: {config.memorySettings?.maxSize}
              </span>
              <span className={`${styles.text} text-sm`}>
                Backup: Every {config.memorySettings?.backupInterval}
              </span>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

export default MemoryConfig;