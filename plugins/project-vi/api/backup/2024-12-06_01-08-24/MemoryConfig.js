import React, { useState } from 'react';
import { Brain, ArrowRight, ArrowLeft, Save, Check } from 'lucide-react';
import { useTheme } from '../../theme/ThemeContext';
import BasicSetup from './components/BasicSetup';
import ContextConfig from './components/ContextConfig';
import PrivacySettings from './components/PrivacySettings';
import RetentionConfig from './components/RetentionConfig';
import MemoryDevConfig from './components/dev/MemoryDevConfig';
import DevModeToggle from '../shared/DevModeToggle';

const MemoryConfig = () => {
  const { styles } = useTheme();
  const [isDevMode, setIsDevMode] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [config, setConfig] = useState({
    // Basic Setup
    memoryProfile: 'casual',
    
    // Context Configuration
    contextDepth: 5,
    contextCategories: ['conversational', 'technical'],
    
    // Privacy Settings
    privacyLevel: 'standard',
    dataPreferences: {
      personal: 'ask',
      professional: 'remember',
      sensitive: 'forget'
    },
    
    // Retention Configuration
    retentionPeriod: 'medium',
    retentionTypes: ['preferences', 'context', 'technical']
  });

  const steps = [
    { 
      id: 'basic',
      title: 'Basic Setup',
      description: 'Choose your starting configuration',
      component: BasicSetup
    },
    {
      id: 'context',
      title: 'Context Configuration',
      description: 'Define how Claude understands context',
      component: ContextConfig
    },
    {
      id: 'privacy',
      title: 'Privacy Settings',
      description: 'Control how information is handled',
      component: PrivacySettings
    },
    {
      id: 'retention',
      title: 'Memory Retention',
      description: 'Configure how long Claude remembers',
      component: RetentionConfig
    }
  ];

  const handleConfigChange = (key, value) => {
    setConfig(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className={styles.container}>
      {/* Header with Dev Mode Toggle */}
      <div className={`p-6 ${styles.section} flex justify-between items-center`}>
        <div className="flex items-center space-x-3">
          <Brain className={styles.icon} />
          <div>
            <h2 className={styles.heading}>Memory System Configuration</h2>
            <p className={styles.subheading}>Configure how Claude remembers and maintains context</p>
          </div>
        </div>
        <DevModeToggle isDevMode={isDevMode} onToggle={() => setIsDevMode(!isDevMode)} />
      </div>

      {isDevMode ? (
        <MemoryDevConfig config={config} onChange={handleConfigChange} />
      ) : (
        <>
          {/* Progress Indicator */}
          <div className={`border-b ${styles.section} p-4`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2 text-sm text-concept-yellow-light/60">
                <span>Step {currentStep + 1} of {steps.length}</span>
                <div className="w-24 h-2 bg-concept-brown-dark/20 rounded-full">
                  <div 
                    className="h-full bg-concept-yellow rounded-full transition-all duration-300"
                    style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                  />
                </div>
              </div>
            </div>
            
            <div className="flex justify-between">
              {steps.map((step, index) => (
                <div 
                  key={step.id}
                  className={`flex-1 ${index !== steps.length - 1 ? 'border-r border-concept-brown-dark/20' : ''} px-4`}
                >
                  <div className={`text-sm font-medium ${
                    index === currentStep ? styles.icon : 
                    index < currentStep ? 'text-concept-yellow' : 
                    styles.text
                  }`}>
                    {index < currentStep ? (
                      <div className="flex items-center space-x-1">
                        <Check className="w-4 h-4" />
                        <span>{step.title}</span>
                      </div>
                    ) : (
                      step.title
                    )}
                  </div>
                  <p className={styles.text}>{step.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Current Step Content */}
          <div className="p-6 min-h-[400px]">
            {React.createElement(steps[currentStep].component, {
              config,
              onChange: handleConfigChange
            })}
          </div>

          {/* Navigation */}
          <div className={`flex justify-between items-center p-6 ${styles.divider}`}>
            <button
              onClick={() => setCurrentStep(prev => prev - 1)}
              disabled={currentStep === 0}
              className={`flex items-center space-x-2 ${
                currentStep === 0
                  ? 'opacity-50 cursor-not-allowed'
                  : styles.buttonSecondary
              }`}
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>

            {currentStep === steps.length - 1 ? (
              <button 
                onClick={() => console.log('Saving configuration:', config)}
                className={`flex items-center space-x-2 ${styles.buttonPrimary}`}
              >
                <Save className="w-4 h-4" />
                <span>Save Configuration</span>
              </button>
            ) : (
              <button
                onClick={() => setCurrentStep(prev => prev + 1)}
                className={`flex items-center space-x-2 ${styles.buttonPrimary}`}
              >
                <span>Next</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default MemoryConfig;