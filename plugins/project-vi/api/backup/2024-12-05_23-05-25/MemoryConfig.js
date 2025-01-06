import React, { useState } from 'react';
import { Brain, ArrowRight, ArrowLeft, Save, Check } from 'lucide-react';
import BasicSetup from './components/BasicSetup';
import ContextConfig from './components/ContextConfig';
import PrivacySettings from './components/PrivacySettings';
import RetentionConfig from './components/RetentionConfig';
import MemoryDevConfig from './components/dev/MemoryDevConfig';
import DevModeToggle from '../shared/DevModeToggle';

const MemoryConfig = () => {
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
      description: 'Define how Claude understands and maintains context',
      component: ContextConfig
    },
    {
      id: 'privacy',
      title: 'Privacy Settings',
      description: 'Control how your information is handled',
      component: PrivacySettings
    },
    {
      id: 'retention',
      title: 'Memory Retention',
      description: 'Configure how long Claude remembers information',
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
    <div className="space-y-8">
      {/* Header with Dev Mode Toggle */}
      <div className="flex items-center justify-between border-b border-gray-200 pb-4">
        <div className="flex items-center space-x-3">
          <Brain className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-semibold text-gray-900">Memory System Setup</h2>
        </div>
        <DevModeToggle isDevMode={isDevMode} onToggle={() => setIsDevMode(!isDevMode)} />
      </div>

      {isDevMode ? (
        // Developer Mode Interface
        <MemoryDevConfig config={config} onChange={handleConfigChange} />
      ) : (
        // User Mode Interface
        <>
          {/* Progress Indicator */}
          <div className="border-b border-gray-200 pb-4">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <span>Step {currentStep + 1} of {steps.length}</span>
                <div className="w-24 h-2 bg-gray-200 rounded-full">
                  <div 
                    className="h-full bg-purple-600 rounded-full transition-all duration-300"
                    style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                  />
                </div>
              </div>
            </div>
            
            <div className="flex justify-between">
              {steps.map((step, index) => (
                <div 
                  key={step.id}
                  className={`flex-1 ${index !== steps.length - 1 ? 'border-r border-gray-200' : ''} px-4`}
                >
                  <div className={`text-sm font-medium ${
                    index === currentStep ? 'text-purple-600' : 
                    index < currentStep ? 'text-green-600' : 
                    'text-gray-500'
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
                  <p className="text-xs text-gray-500 mt-1">{step.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Current Step Content */}
          <div className="min-h-[400px]">
            {React.createElement(steps[currentStep].component, {
              config,
              onChange: handleConfigChange
            })}
          </div>

          {/* Navigation */}
          <div className="flex justify-between items-center pt-6 border-t border-gray-200">
            <button
              onClick={() => setCurrentStep(prev => prev - 1)}
              disabled={currentStep === 0}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md ${
                currentStep === 0
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-gray-700 hover:text-gray-900'
              }`}
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>

            {currentStep === steps.length - 1 ? (
              <button 
                onClick={() => console.log('Saving configuration:', config)}
                className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
              >
                <Save className="w-4 h-4" />
                <span>Save Configuration</span>
              </button>
            ) : (
              <button
                onClick={() => setCurrentStep(prev => prev + 1)}
                className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
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