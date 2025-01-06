import React from 'react';
import { 
  Save, 
  Brain,
  Book,
  Sun,
  Moon,
  Wrench,
  Settings,
  ArrowRight
} from 'lucide-react';

import { categories } from './data';
import PowerUpConfig from '../PowerUpConfig';
import ExportConfig from '../ExportConfig';
import InstallationWizard from '../InstallationWizard';
import { useClaudeConfig } from '../../hooks/useClaudeConfig';
import { Button, Card } from '../../shared/components';

const ConfigWizard = () => {
  const {
    activeSection,
    activePowerUp,
    selectedPowerUps,
    styles,
    selectPowerUp,
    setActiveSection,
    saveConfiguration,
    startInstallation
  } = useClaudeConfig();

  const renderHome = () => (
    <div className="space-y-8 py-12">
      <div className="text-center space-y-4">
        <h2 className={`text-3xl font-bold ${styles.heading}`}>Welcome to Claude Configuration</h2>
        <p className={styles.subheading}>Choose how you'd like to get started</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto mt-8">
        <Card
          onClick={() => setActiveSection('setup')}
          className="p-8 text-center"
        >
          <Wrench className={`w-12 h-12 ${styles.icon} mx-auto mb-4`} />
          <h3 className={`text-xl font-semibold ${styles.heading} mb-2`}>Initial Setup</h3>
          <p className={styles.text}>First time setup? Start here to install and configure Claude Desktop</p>
          <Button 
            variant="primary"
            className="mt-4 w-full"
            icon={ArrowRight}
          >
            Start Setup
          </Button>
        </Card>

        <Card
          onClick={() => setActiveSection('quick-start')}
          className="p-8 text-center"
        >
          <Settings className={`w-12 h-12 ${styles.icon} mx-auto mb-4`} />
          <h3 className={`text-xl font-semibold ${styles.heading} mb-2`}>Configure Power-ups</h3>
          <p className={styles.text}>Already installed? Customize and manage your Claude power-ups</p>
          <Button 
            variant="primary"
            className="mt-4 w-full"
            icon={ArrowRight}
          >
            Configure
          </Button>
        </Card>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeSection) {
      case 'home':
        return renderHome();
      case 'setup':
        return <InstallationWizard />;
      case 'quick-start':
      case 'power-ups':
        return (
          <div className="space-y-8">
            {Object.entries(categories).map(([categoryName, category]) => (
              <div key={categoryName} className="space-y-4">
                <div className="flex items-center space-x-3">
                  <category.icon className={styles.icon} />
                  <h2 className={`text-xl font-semibold ${styles.heading}`}>{categoryName}</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {category.items.map((tool) => (
                    <Card
                      key={tool.id}
                      onClick={() => selectPowerUp(tool)}
                      selected={selectedPowerUps.includes(tool.id)}
                    >
                      <div className="flex items-center space-x-3">
                        <category.icon className={styles.icon} />
                        <div>
                          <div className="flex items-center">
                            <h3 className={styles.heading}>{tool.name}</h3>
                            {tool.official ? (
                              <span className={styles.badgeOfficial}>Official</span>
                            ) : (
                              <span className={styles.badgeCommunity}>Community</span>
                            )}
                          </div>
                          <p className={`${styles.text} mt-1`}>{tool.description}</p>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            ))}
          </div>
        );
      case 'advanced':
        return activePowerUp ? <PowerUpConfig powerUp={activePowerUp} /> : null;
      default:
        return null;
    }
  };

  return (
    <div className={styles.container}>
      {/* Header */}
      <div className="p-6 border-b border-concept-brown-light flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <img 
            src={process.env.PUBLIC_URL + '/Icon_ConceptV_VCircle_White.png'} 
            alt="ConceptV"
            className="w-8 h-8" 
          />
          <div>
            <h1 className="text-2xl font-bold text-concept-yellow-sepia">Claude Power-Up Station</h1>
            <p className="mt-1 text-concept-yellow-light/80">Enhance Claude with powerful integrations and capabilities</p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          {activeSection !== 'home' && (
            <Button 
              variant="secondary"
              onClick={() => setActiveSection('home')}
            >
              Back to Home
            </Button>
          )}
          <Button 
            variant="icon"
            onClick={() => saveConfiguration()}
            icon={Save}
          />
        </div>
      </div>

      {/* Content */}
      <div className="min-h-[600px]">
        {renderContent()}
      </div>

      {/* Footer */}
      <div className="mt-6 flex justify-between items-center p-6 border-t border-concept-brown-dark/20">
        <div className="flex items-center space-x-2">
          <Book className={styles.iconSecondary} />
          <a href="https://modelcontextprotocol.io/docs" 
             className={`text-sm ${styles.buttonSecondary}`}>
            View Documentation
          </a>
        </div>
        <div className="flex space-x-4">
          <Button variant="secondary">
            Cancel
          </Button>
          <Button 
            variant="primary"
            icon={Save}
            onClick={saveConfiguration}
          >
            Save Configuration
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ConfigWizard;