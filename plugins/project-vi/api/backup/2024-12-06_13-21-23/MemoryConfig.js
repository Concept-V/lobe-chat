import React, { useState } from 'react';
import { Settings, Save as SaveIcon } from 'lucide-react';  // Import SaveIcon
import { useTheme } from '../../shared/contexts';
import { withTheme } from '../../shared/hoc/withTheme';
import { Card, Button } from '../../shared/components';
import BasicSetup from './components/BasicSetup';
import AdvancedSettings from './components/AdvancedSettings';
import StorageManagement from './components/StorageManagement';
import KnowledgeGraph from './components/KnowledgeGraph';

// Dev components
import BasicSetupDev from './components/dev/BasicSetupDev';
import AdvancedSettingsDev from './components/dev/AdvancedSettingsDev';
import StorageManagementDev from './components/dev/StorageManagementDev';
import KnowledgeGraphDev from './components/dev/KnowledgeGraphDev';
import MonitoringPanelDev from './components/dev/MonitoringPanelDev';

const MemoryConfig = ({ devMode = false }) => {
  const { styles } = useTheme();
  const [config, setConfig] = useState({
    profile: 'balanced',
    mode: 'standard',
    memory: {
      storageType: 'persistent',
      compressionLevel: 'balanced',
      indexingStrategy: 'hybrid'
    }
  });

  const handleConfigChange = (key, value) => {
    setConfig(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const renderContent = () => {
    if (devMode) {
      return (
        <>
          <BasicSetupDev config={config} onChange={handleConfigChange} />
          <AdvancedSettingsDev config={config} onChange={handleConfigChange} />
          <StorageManagementDev config={config} onChange={handleConfigChange} />
          <KnowledgeGraphDev config={config} onChange={handleConfigChange} />
          <MonitoringPanelDev config={config} onChange={handleConfigChange} />
        </>
      );
    }

    return (
      <>
        <BasicSetup config={config} onChange={handleConfigChange} />
        <AdvancedSettings config={config} onChange={handleConfigChange} />
        <StorageManagement config={config} onChange={handleConfigChange} />
        <KnowledgeGraph config={config} onChange={handleConfigChange} />
      </>
    );
  };

  return (
    <div className="space-y-6 p-6">
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Settings className={styles.icon} />
            <h2 className={`text-xl font-medium ${styles.heading}`}>Memory Configuration</h2>
          </div>
          <Button variant="primary" icon={SaveIcon}>Save Changes</Button>
        </div>
        {renderContent()}
      </Card>
    </div>
  );
};

export default withTheme(MemoryConfig);