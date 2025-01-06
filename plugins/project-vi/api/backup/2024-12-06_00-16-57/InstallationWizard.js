import React, { useState } from 'react';
import { useTheme } from '../../theme/ThemeContext';
import { installationService } from '../../services/installationService';
import { 
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  ArrowLeft,
  Terminal,
  Download,
  Server,
  Settings,
  Copy
} from 'lucide-react';

const InstallationWizard = () => {
  const { styles } = useTheme();
  const [currentStep, setCurrentStep] = useState(0);
  const [config, setConfig] = useState({
    selectedServers: [],
    installationType: 'guided',
    computerUse: true
  });
  const [systemCheck, setSystemCheck] = useState(null);

  const steps = [
    {
      id: 'welcome',
      title: 'Welcome',
      description: 'Choose your installation method'
    },
    {
      id: 'system-check',
      title: 'System Check',
      description: 'Verify system requirements'
    },
    {
      id: 'select-components',
      title: 'Select Components',
      description: 'Choose what to install'
    },
    {
      id: 'configuration',
      title: 'Configuration',
      description: 'Configure installation options'
    },
    {
      id: 'review',
      title: 'Review & Install',
      description: 'Review and start installation'
    }
  ];

  const renderWelcome = () => (
    <div className="space-y-6">
      <div className={`${styles.card} p-6`}>
        <h3 className={`text-xl font-semibold ${styles.heading} mb-4`}>Choose Installation Method</h3>
        <div className="space-y-4">
          <button
            onClick={() => {
              setConfig(prev => ({ ...prev, installationType: 'guided' }));
              setCurrentStep(1);
            }}
            className={`${styles.card} ${styles.cardHover} p-4 w-full text-left flex items-center space-x-4`}
          >
            <Terminal className={styles.icon} />
            <div>
              <h4 className={styles.heading}>Guided Installation</h4>
              <p className={styles.text}>Step-by-step installation with Claude's assistance</p>
            </div>
          </button>

          <button
            onClick={() => {
              setConfig(prev => ({ ...prev, installationType: 'script' }));
              setCurrentStep(1);
            }}
            className={`${styles.card} ${styles.cardHover} p-4 w-full text-left flex items-center space-x-4`}
          >
            <Download className={styles.icon} />
            <div>
              <h4 className={styles.heading}>Download Installation Script</h4>
              <p className={styles.text}>Get a PowerShell script to run manually</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );

  const renderSystemCheck = () => (
    <div className="space-y-6">
      <div className={`${styles.card} p-6`}>
        <h3 className={`text-xl font-semibold ${styles.heading} mb-4`}>System Requirements Check</h3>
        <div className="space-y-4">
          {Object.entries(installationService.getBaseDependencies().system).map(([category, requirements]) => (
            <div key={category} className={`${styles.card} p-4`}>
              <h4 className={`${styles.heading} mb-2`}>{category.charAt(0).toUpperCase() + category.slice(1)} Requirements</h4>
              <ul className="space-y-2">
                {Object.entries(requirements).map(([key, value]) => (
                  <li key={key} className="flex items-center space-x-2">
                    <CheckCircle2 className="w-5 h-5 text-green-500" />
                    <span className={styles.text}>
                      {key}: {Array.isArray(value) ? value.join(', ') : value}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderSelectComponents = () => (
    <div className="space-y-6">
      <div className={`${styles.card} p-6`}>
        <h3 className={`text-xl font-semibold ${styles.heading} mb-4`}>Select Components to Install</h3>
        <div className="space-y-4">
          {Object.entries(installationService.getMCPDependencies(['memory', 'filesystem', 'github', 'postgresql'])).map(([server, deps]) => (
            <div key={server} className={`${styles.card} p-4`}>
              <label className="flex items-center space-x-4">
                <input
                  type="checkbox"
                  checked={config.selectedServers.includes(server)}
                  onChange={(e) => {
                    setConfig(prev => ({
                      ...prev,
                      selectedServers: e.target.checked
                        ? [...prev.selectedServers, server]
                        : prev.selectedServers.filter(s => s !== server)
                    }));
                  }}
                  className={styles.checkbox}
                />
                <Server className={styles.icon} />
                <div>
                  <h4 className={styles.heading}>{server.charAt(0).toUpperCase() + server.slice(1)} MCP Server</h4>
                  <p className={styles.text}>Packages: {deps.packages.join(', ')}</p>
                </div>
              </label>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderConfiguration = () => (
    <div className="space-y-6">
      <div className={`${styles.card} p-6`}>
        <h3 className={`text-xl font-semibold ${styles.heading} mb-4`}>Configuration Options</h3>
        <div className="space-y-4">
          <div className={`${styles.card} p-4`}>
            <label className="flex items-center space-x-4">
              <input
                type="checkbox"
                checked={config.computerUse}
                onChange={(e) => setConfig(prev => ({ ...prev, computerUse: e.target.checked }))}
                className={styles.checkbox}
              />
              <Settings className={styles.icon} />
              <div>
                <h4 className={styles.heading}>Use Computer Control</h4>
                <p className={styles.text}>Allow Claude to perform installation steps</p>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
  );

  const renderReview = () => {
    const script = config.computerUse
      ? installationService.generateComputerUseInstructions(config)
      : installationService.generateInstallationScript(config);

    return (
      <div className="space-y-6">
        <div className={`${styles.card} p-6`}>
          <h3 className={`text-xl font-semibold ${styles.heading} mb-4`}>Review Installation Plan</h3>
          <div className="space-y-4">
            <div className={`${styles.card} bg-dark p-4`}>
              <div className="flex justify-between items-center mb-4">
                <h4 className={styles.heading}>Installation Script</h4>
                <button
                  onClick={() => navigator.clipboard.writeText(script)}
                  className={styles.buttonSecondary}
                >
                  <Copy className="w-4 h-4" />
                  <span>Copy</span>
                </button>
              </div>
              <pre className={`${styles.text} whitespace-pre-wrap`}>
                {script}
              </pre>
            </div>

            {config.computerUse && (
              <div className={`${styles.card} p-4 border-concept-yellow`}>
                <div className="flex items-start space-x-3">
                  <AlertCircle className="w-5 h-5 text-concept-yellow flex-shrink-0 mt-1" />
                  <div>
                    <h4 className={`${styles.heading} text-concept-yellow`}>Computer Control Enabled</h4>
                    <p className={styles.text}>
                      Claude will execute these steps using Computer Control.
                      You'll be asked to confirm each step before it's executed.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return renderWelcome();
      case 1:
        return renderSystemCheck();
      case 2:
        return renderSelectComponents();
      case 3:
        return renderConfiguration();
      case 4:
        return renderReview();
      default:
        return null;
    }
  };

  return (
    <div className={styles.container}>
      {/* Progress */}
      <div className={`${styles.section} p-4`}>
        <div className="flex justify-between mb-4">
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
                {step.title}
              </div>
              <p className={styles.text}>{step.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {renderStep()}
      </div>

      {/* Navigation */}
      <div className={`${styles.section} p-4 flex justify-between`}>
        <button
          onClick={() => setCurrentStep(prev => prev - 1)}
          disabled={currentStep === 0}
          className={`${styles.buttonSecondary} ${currentStep === 0 ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Previous</span>
        </button>

        <button
          onClick={() => {
            if (currentStep === steps.length - 1) {
              // Start installation
              console.log('Starting installation with config:', config);
            } else {
              setCurrentStep(prev => prev + 1);
            }
          }}
          className={styles.buttonPrimary}
        >
          <span>{currentStep === steps.length - 1 ? 'Start Installation' : 'Next'}</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default InstallationWizard;