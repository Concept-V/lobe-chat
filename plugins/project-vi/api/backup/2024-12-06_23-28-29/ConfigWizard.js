import React, { useState } from 'react';
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
import { useTheme, useLogging } from '../../shared/contexts';
import PowerUpConfig from '../PowerUpConfig';
import ExportConfig from '../ExportConfig';
import InstallationWizard from '../InstallationWizard';
import { Button, Card } from '../../shared/components';

const ConfigWizard = () => {
  const { styles, isDarkMode, toggleDarkMode } = useTheme();
  const { log } = useLogging();
  const [activeSection, setActiveSection] = useState('home');
  const [selectedPowerups, setSelectedPowerups] = useState([]);
  const [activePowerUp, setActivePowerUp] = useState(null);

  const handlePowerUpClick = (tool) => {
    setActivePowerUp(tool);
    setActiveSection('advanced');
    log('info', 'Power-up selected', { tool });
  };

  const renderHome = () => (
    <div className="space-y-8 py-12">
      <div className="text-center space-y-4">
        <h2 className={`text-3xl font-bold ${styles.heading}`}>Vi Configuration Center</h2>
        <p className={styles.subheading}>Configure integrations and tools</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto mt-8">
        {/* Initial Setup Card */}
        <Card 
          onClick={() => {
            setActiveSection('setup');
            log('info', 'Setup wizard started');
          }}
          className="p-8 text-center"
        >
          <Wrench className={`w-12 h-12 ${styles.icon} mx-auto mb-4`} />
          <h3 className={`text-xl font-semibold ${styles.heading} mb-2`}>Initial Setup</h3>
          <p className={styles.text}>First time setup? Start here to install and configure Vi</p>
          <Button 
            variant="primary"
            className="mt-4 w-full"
            icon={ArrowRight}
          >
            Start Setup
          </Button>
        </Card>

        {/* Power-up Configuration Card */}
        <Card 
          onClick={() => {
            setActiveSection('quick-start');
            log('info', 'Power-up configuration started');
          }}
          className="p-8 text-center"
        >
          <Settings className={`w-12 h-12 ${styles.icon} mx-auto mb-4`} />
          <h3 className={`text-xl font-semibold ${styles.heading} mb-2`}>Configure Power-ups</h3>
          <p className={styles.text}>Already installed? Customize and manage your Vi power-ups</p>
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

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark bg-dark' : 'bg-concept-yellow-light'}`}>
      <div className="p-8">
        <div className="max-w-6xl mx-auto bg-dark-card rounded-lg shadow-xl">
          {/* Header */}
          <div className="p-6 border-b border-concept-brown-light flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <img 
                src={process.env.PUBLIC_URL + '/Icon_ConceptV_VCircle_White.png'} 
                alt="Vi"
                className="w-8 h-8" 
              />
              <div>
                <h1 className="text-2xl font-bold text-concept-yellow-sepia">Vi Command Centre</h1>
                <p className="mt-1 text-concept-yellow-light/80">Configuration and Integration Management</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {activeSection !== 'home' && (
                <Button 
                  variant="secondary"
                  onClick={() => {
                    setActiveSection('home');
                    log('info', 'Returned to home');
                  }}
                >
                  Back to Home
                </Button>
              )}
              <Button 
                variant="icon"
                onClick={toggleDarkMode}
                icon={isDarkMode ? Sun : Moon}
              />
            </div>
          </div>

          {/* Content Area */}
          <div className="min-h-[600px]">
            {activeSection === 'home' && renderHome()}
            
            {activeSection === 'setup' && (
              <div className="p-6">
                <InstallationWizard />
              </div>
            )}

            {(activeSection === 'quick-start' || activeSection === 'power-ups' || activeSection === 'advanced') && (
              <>
                {/* Navigation */}
                <div className="flex border-b border-concept-brown-dark/20">
                  {['quick-start', 'power-ups', 'advanced'].map((section) => (
                    <Button
                      key={section}
                      variant="nav"
                      onClick={() => {
                        setActiveSection(section);
                        log('info', 'Section changed', { section });
                      }}
                      className={styles.navButton(activeSection === section)}
                    >
                      {section.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                    </Button>
                  ))}
                </div>

                {/* Power-ups Content */}
                <div className="p-6">
                  {activeSection === 'advanced' && activePowerUp ? (
                    <PowerUpConfig powerUp={activePowerUp} />
                  ) : (
                    <div className="space-y-8">
                      {Object.entries(categories).map(([categoryName, category]) => {
                        const IconComponent = category.icon;
                        return (
                          <div key={categoryName} className="space-y-4">
                            <div className="flex items-center space-x-3">
                              <IconComponent className={styles.icon} />
                              <h2 className={`text-xl font-semibold ${styles.heading}`}>{categoryName}</h2>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                              {category.items.map((tool) => (
                                <Card
                                  key={tool.id}
                                  onClick={() => handlePowerUpClick(tool)}
                                  selected={selectedPowerups.includes(tool.id)}
                                >
                                  <div className="flex items-center space-x-3">
                                    <IconComponent className={styles.icon} />
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
                        );
                      })}
                    </div>
                  )}
                </div>
              </>
            )}
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
                onClick={() => {
                  log('info', 'Saving configuration');
                  // TODO: Implement save functionality
                }}
              >
                Save Configuration
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigWizard;