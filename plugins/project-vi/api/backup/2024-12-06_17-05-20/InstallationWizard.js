import React, { useState } from 'react';
import { Brain, Briefcase, Code, ArrowRight, ArrowLeft, Check } from 'lucide-react';
import { useTheme } from '../../theme/ThemeContext';
import { useConfig } from '../../shared/contexts/ConfigContext';
import { useLogging } from '../../shared/contexts/LoggingContext';
import { installationPresets } from '../../shared/configs/presets';
import { Button, Card, StepIndicator } from '../../shared/components';

const InstallationWizard = () => {
  const { styles } = useTheme();
  const { updateConfig } = useConfig();
  const { log } = useLogging();
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [installProgress, setInstallProgress] = useState(null);

  const steps = [
    {
      id: 'profile',
      title: 'Choose Profile',
      description: 'Select your installation profile'
    },
    {
      id: 'customize',
      title: 'Customize',
      description: 'Adjust your settings'
    },
    {
      id: 'install',
      title: 'Install',
      description: 'Complete installation'
    }
  ];

  const getIconComponent = (iconName) => {
    switch (iconName) {
      case 'Brain': return Brain;
      case 'Briefcase': return Briefcase;
      case 'Code': return Code;
      default: return Brain;
    }
  };

  const handleProfileSelect = (profileId) => {
    setSelectedProfile(profileId);
    log.info('Profile selected', { profileId });
  };

  const handleInstall = async () => {
    const profile = installationPresets.profiles[selectedProfile];
    log.info('Starting installation', { profile });
    
    try {
      // Update global config with profile settings
      updateConfig('features', profile.features);
      
      // Install required MCP servers
      for (const server of profile.servers) {
        setInstallProgress(`Installing ${server}...`);
        // TODO: Implement actual installation using mcp-get
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulated installation
      }

      setInstallProgress('Configuration complete!');
      log.info('Installation completed successfully');
    } catch (error) {
      log.error('Installation failed', { error });
      setInstallProgress('Installation failed. Please try again.');
    }
  };

  const renderProfileSelection = () => (
    <div className="space-y-6">
      <div className={`${styles.card} bg-concept-brown-dark/10`}>
        <h3 className={styles.heading}>Choose Your Setup Profile</h3>
        <p className={styles.subheading}>
          Select a profile that matches your needs. You can customize it in the next step.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {Object.values(installationPresets.profiles).map(profile => {
          const IconComponent = getIconComponent(profile.icon);
          return (
            <Card
              key={profile.id}
              selected={selectedProfile === profile.id}
              onClick={() => handleProfileSelect(profile.id)}
              className="cursor-pointer"
            >
              <div className="flex items-center space-x-3 mb-3">
                <IconComponent className={styles.icon} />
                <h4 className={styles.heading}>{profile.name}</h4>
              </div>
              <p className={styles.text}>{profile.description}</p>
              
              {selectedProfile === profile.id && (
                <div className="mt-3 pt-3 border-t border-concept-brown-light/20">
                  <ul className={`space-y-1 ${styles.text}`}>
                    {profile.servers.map(server => (
                      <li key={server} className="flex items-center space-x-2">
                        <Check className="w-4 h-4 text-concept-yellow" />
                        <span>{server}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );

  const renderCustomization = () => (
    <div className="space-y-6">
      {selectedProfile && (
        <div className="space-y-4">
          <h3 className={styles.heading}>Customize Your Installation</h3>
          <p className={styles.subheading}>
            Review and adjust the settings for your {installationPresets.profiles[selectedProfile].name}
          </p>

          {/* Memory Configuration */}
          <Card className="space-y-4">
            <h4 className={styles.heading}>Memory System</h4>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(installationPresets.memoryConfigs.standard).map(([key, value]) => (
                <div key={key}>
                  <label className={`block ${styles.text} mb-1`}>{key}</label>
                  <input
                    type="text"
                    value={value}
                    className={styles.input}
                    readOnly
                  />
                </div>
              ))}
            </div>
          </Card>

          {/* File System Configuration */}
          <Card className="space-y-4">
            <h4 className={styles.heading}>File System</h4>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(installationPresets.filesystemConfigs.basic).map(([key, value]) => (
                <div key={key}>
                  <label className={`block ${styles.text} mb-1`}>{key}</label>
                  <input
                    type="text"
                    value={Array.isArray(value) ? value.join(', ') : value.toString()}
                    className={styles.input}
                    readOnly
                  />
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );

  const renderInstallation = () => (
    <div className="space-y-6">
      <div className={`${styles.card} bg-concept-brown-dark/10`}>
        <h3 className={styles.heading}>Installation Progress</h3>
        <p className={styles.subheading}>
          {installProgress || 'Ready to install. Click "Install" to begin.'}
        </p>
      </div>

      {!installProgress && (
        <Button
          variant="primary"
          onClick={handleInstall}
          className="w-full"
        >
          Install
        </Button>
      )}

      {installProgress && installProgress.includes('complete') && (
        <div className={`${styles.card} bg-concept-yellow/10`}>
          <div className="flex items-center space-x-3">
            <Check className="w-6 h-6 text-concept-yellow" />
            <p className={styles.heading}>Installation Complete!</p>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="space-y-8">
      <StepIndicator
        steps={steps}
        currentStep={currentStep}
        onStepClick={(step) => {
          if (step < currentStep) setCurrentStep(step);
        }}
      />

      <div className="min-h-[400px]">
        {currentStep === 0 && renderProfileSelection()}
        {currentStep === 1 && renderCustomization()}
        {currentStep === 2 && renderInstallation()}
      </div>

      <div className="flex justify-between pt-6 border-t border-concept-brown-dark/20">
        <Button
          variant="secondary"
          onClick={() => setCurrentStep(prev => prev - 1)}
          disabled={currentStep === 0}
          icon={ArrowLeft}
        >
          Back
        </Button>

        <Button
          variant="primary"
          onClick={() => setCurrentStep(prev => prev + 1)}
          disabled={currentStep === 2 || !selectedProfile}
          icon={ArrowRight}
        >
          Continue
        </Button>
      </div>
    </div>
  );
};

export default InstallationWizard;