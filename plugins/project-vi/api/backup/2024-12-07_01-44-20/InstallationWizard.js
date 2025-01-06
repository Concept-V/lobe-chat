import React, { useState, useEffect } from 'react';
import { Brain, Briefcase, Code, ArrowRight, ArrowLeft, Check } from 'lucide-react';
import { useTheme, useConfig, useLogging } from '../../shared/contexts';
import { installationPresets } from '../../shared/configs/presets';
import { Button, Card, StepIndicator } from '../../shared/components';

// Import our new components
import SystemCheck from './components/SystemCheck';
import IntegrationSetup from './components/IntegrationSetup';
import SecurityConfig from './components/SecurityConfig';
import ValidationCheck from './components/ValidationCheck';
import FinalReview from './components/FinalReview';

const InstallationWizard = () => {
  const { styles } = useTheme();
  const { updateConfig } = useConfig();
  const { log } = useLogging();
  
  // State Management
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [installProgress, setInstallProgress] = useState(null);
  const [stepStates, setStepStates] = useState({
    systemCheck: false,
    profileSelect: false,
    security: false,
    integration: false,
    validation: false
  });
  const [securityConfig, setSecurityConfig] = useState(null);

  // Define installation steps
  const steps = [
    {
      id: 'system',
      title: 'System Check',
      description: 'Verify system requirements'
    },
    {
      id: 'profile',
      title: 'Choose Profile',
      description: 'Select installation profile'
    },
    {
      id: 'security',
      title: 'Security Setup',
      description: 'Configure security settings'
    },
    {
      id: 'integration',
      title: 'Integrations',
      description: 'Set up connections'
    },
    {
      id: 'validation',
      title: 'Validation',
      description: 'Verify configuration'
    },
    {
      id: 'review',
      title: 'Review',
      description: 'Final review and install'
    }
  ];

  useEffect(() => {
    log('info', 'InstallationWizard initialized');
  }, [log]);

  const handleStepComplete = (step, data) => {
    setStepStates(prev => ({
      ...prev,
      [step]: true
    }));

    // Handle step-specific data
    switch (step) {
      case 'profileSelect':
        setSelectedProfile(data);
        break;
      case 'security':
        setSecurityConfig(data);
        break;
      default:
        break;
    }

    // Move to next step if available
    if (currentStep < steps.length - 1) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handleInstall = async () => {
    const profile = installationPresets.profiles[selectedProfile];
    log('info', 'Starting installation', { profile });
    
    try {
      setInstallProgress('Preparing installation...');
      
      // Update global config
      updateConfig('features', profile.features);
      
      // Install required MCP servers
      for (const server of profile.servers) {
        setInstallProgress(`Installing ${server}...`);
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      // Apply security configuration
      setInstallProgress('Applying security settings...');
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Finalize installation
      setInstallProgress('Configuration complete!');
      log('info', 'Installation completed successfully');
    } catch (error) {
      log('error', 'Installation failed', { error });
      setInstallProgress('Installation failed. Please try again.');
    }
  };

  const renderStepContent = () => {
    switch (steps[currentStep].id) {
      case 'system':
        return (
          <SystemCheck
            profile={selectedProfile ? installationPresets.profiles[selectedProfile] : null}
            onComplete={(success) => handleStepComplete('systemCheck', success)}
          />
        );
      
      case 'profile':
        return (
          <div className="space-y-6">
            <div className={`${styles.card} bg-concept-brown-dark/10`}>
              <h3 className={styles.heading}>Choose Your Setup Profile</h3>
              <p className={styles.subheading}>
                Select a profile that matches your needs
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {Object.entries(installationPresets.profiles).map(([id, profile]) => {
                const IconComponent = profile.icon === 'Brain' ? Brain : 
                                    profile.icon === 'Briefcase' ? Briefcase : Code;
                return (
                  <Card
                    key={id}
                    selected={selectedProfile === id}
                    onClick={() => {
                      setSelectedProfile(id);
                      handleStepComplete('profileSelect', id);
                    }}
                    className="cursor-pointer"
                  >
                    <div className="flex items-center space-x-3 mb-3">
                      <IconComponent className={styles.icon} />
                      <div>
                        <h4 className={styles.heading}>{profile.name}</h4>
                        <p className={styles.text}>{profile.description}</p>
                      </div>
                    </div>
                    {selectedProfile === id && (
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
      
      case 'security':
        return (
          <SecurityConfig
            profile={installationPresets.profiles[selectedProfile]}
            onComplete={(config) => handleStepComplete('security', config)}
          />
        );
      
      case 'integration':
        return (
          <IntegrationSetup
            profile={installationPresets.profiles[selectedProfile]}
            onComplete={(success) => handleStepComplete('integration', success)}
          />
        );
      
      case 'validation':
        return (
          <ValidationCheck
            profile={installationPresets.profiles[selectedProfile]}
            securityConfig={securityConfig}
            onComplete={(success) => handleStepComplete('validation', success)}
          />
        );
      
      case 'review':
        return (
          <FinalReview
            profile={installationPresets.profiles[selectedProfile]}
            securityConfig={securityConfig}
            installationSteps={steps}
            onComplete={handleInstall}
          />
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="space-y-8">
      <StepIndicator
        steps={steps}
        currentStep={currentStep}
        onStepClick={(step) => {
          // Only allow going back to completed steps
          const targetStep = steps[step];
          if (stepStates[targetStep.id] && step < currentStep) {
            setCurrentStep(step);
          }
        }}
      />

      <div className="min-h-[400px] p-6 bg-dark-card rounded-lg">
        {renderStepContent()}
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
          disabled={
            currentStep === steps.length - 1 || 
            !stepStates[steps[currentStep].id]
          }
          icon={ArrowRight}
        >
          Continue
        </Button>
      </div>
    </div>
  );
};

export default InstallationWizard;