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
import { useTheme } from '../../theme/ThemeContext';
import PowerUpConfig from '../PowerUpConfig';
import ExportConfig from '../ExportConfig';

const ConfigWizard = () => {
  const { styles } = useTheme();
  const [activeSection, setActiveSection] = useState('home');
  const [selectedPowerups, setSelectedPowerups] = useState([]);
  const [activePowerUp, setActivePowerUp] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(true);

  const handlePowerUpClick = (tool) => {
    setActivePowerUp(tool);
    setActiveSection('advanced');
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  const renderHome = () => (
    <div className="space-y-8 py-12">
      <div className="text-center space-y-4">
        <h2 className={`text-3xl font-bold ${styles.heading}`}>Welcome to Claude Configuration</h2>
        <p className={styles.subheading}>Choose how you'd like to get started</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto mt-8">
        {/* Initial Setup Card */}
        <div 
          onClick={() => setActiveSection('setup')}
          className={`${styles.card} ${styles.cardHover} p-8 text-center cursor-pointer`}
        >
          <Wrench className={`w-12 h-12 ${styles.icon} mx-auto mb-4`} />
          <h3 className={`text-xl font-semibold ${styles.heading} mb-2`}>Initial Setup</h3>
          <p className={styles.text}>First time setup? Start here to install and configure Claude Desktop</p>
          <button className={`${styles.buttonPrimary} mt-4 w-full flex items-center justify-center`}>
            <span>Start Setup</span>
            <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </div>

        {/* Power-up Configuration Card */}
        <div 
          onClick={() => setActiveSection('quick-start')}
          className={`${styles.card} ${styles.cardHover} p-8 text-center cursor-pointer`}
        >
          <Settings className={`w-12 h-12 ${styles.icon} mx-auto mb-4`} />
          <h3 className={`text-xl font-semibold ${styles.heading} mb-2`}>Configure Power-ups</h3>
          <p className={styles.text}>Already installed? Customize and manage your Claude power-ups</p>
          <button className={`${styles.buttonPrimary} mt-4 w-full flex items-center justify-center`}>
            <span>Configure</span>
            <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </div>
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
                <button 
                  onClick={() => setActiveSection('home')}
                  className={styles.buttonSecondary}
                >
                  Back to Home
                </button>
              )}
              <button 
                onClick={toggleDarkMode}
                className="p-2 rounded-full hover:bg-concept-brown-dark/20"
              >
                {isDarkMode ? 
                  <Sun className="w-5 h-5 text-concept-yellow" /> : 
                  <Moon className="w-5 h-5 text-concept-brown-dark" />
                }
              </button>
            </div>
          </div>

          {/* Content Area */}
          <div className="min-h-[600px]">
            {activeSection === 'home' && renderHome()}
            
            {activeSection === 'setup' && (
              <div className="p-6">
                <ExportConfig config={selectedPowerups} />
              </div>
            )}

            {(activeSection === 'quick-start' || activeSection === 'power-ups' || activeSection === 'advanced') && (
              <>
                {/* Navigation */}
                <div className="flex border-b border-concept-brown-dark/20">
                  {['quick-start', 'power-ups', 'advanced'].map((section) => (
                    <button
                      key={section}
                      onClick={() => setActiveSection(section)}
                      className={styles.navButton(activeSection === section)}
                    >
                      {section.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                    </button>
                  ))}
                </div>

                {/* Power-ups Content */}
                <div className="p-6">
                  {/* ... (rest of your existing power-ups configuration UI) ... */}
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
              <button className={styles.buttonSecondary}>
                Cancel
              </button>
              <button className={`${styles.buttonPrimary} flex items-center space-x-2`}>
                <Save className="w-4 h-4" />
                <span>Save Configuration</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigWizard;